import string,copy
import random
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from fastapi.responses import RedirectResponse
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl
from app.db import db,init_db
from app.cache import redis_client
from app.leaderboard import incr_domain_for_url, top_domains, _normalize_domain
from app.search import ensure_index, health_ok, close_es, index_url, update_url, es, INDEX
from typing import Optional


app = FastAPI()
RESERVED_ALIASES = {"ping", "shorten", "analytics", "leaderboard", "docs", "openapi.json", "redoc", "favicon.ico","search"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    await init_db()
    await ensure_index()
    yield
    await close_es()
    # Shutdown: No cleanup needed for this example, but you can add it here if required

app = FastAPI(lifespan=lifespan)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/search/health")
async def search_health():
    return {"elasticsearch_ok": await health_ok()}

# ----------- MODELS -------------
class URLRequest(BaseModel):
    original_url: HttpUrl
    custom_alias: str | None = None
    ttl: int | None = 7  # days (default: 7 days)


# ----------- HELPERS -------------
def generate_short_id(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        if short_id not in RESERVED_ALIASES:  # ensure not colliding with endpoints
            return short_id

# --- helper: record analytics + leaderboard ---
async def record_hit(short_id: str, original_url: str):
    current_time = datetime.now(timezone.utc)
    # DB analytics
    await db.urls.update_one(
        {"short_id": short_id},
        {
            "$inc": {"click_count": 1},
            "$set": {"last_accessed": current_time}
        }
    )

    # Redis leaderboard
    await incr_domain_for_url(original_url)

    # Update ES (click_count, last_accessed)
    await update_url(short_id, {"click_count": 1, "last_accessed": current_time})

# ----------- ENDPOINTS -------------
@app.post("/shorten")
async def shorten_url(req: URLRequest):
    short_id = req.custom_alias if req.custom_alias else generate_short_id()

    if short_id in RESERVED_ALIASES:
        raise HTTPException(status_code=400, detail="This alias is reserved and cannot be used")

    # check collision if custom alias exists
    existing = await db.urls.find_one({"short_id": short_id})
    if existing:
        raise HTTPException(status_code=400, detail="Alias already taken")

    doc = {
        "short_id": short_id,
        "original_url": str(req.original_url),
        "created_at": datetime.now(timezone.utc),
        "expire_at": datetime.now(timezone.utc) + timedelta(days=req.ttl),
        "click_count": 0,
        "last_accessed": None,
    }

    await db.urls.insert_one(doc)
    es_doc = copy.deepcopy(doc)
    domain = urlparse(doc["original_url"]).netloc
    complete_domain = _normalize_domain(doc["original_url"])
    del es_doc["_id"]  # remove MongoDB-specific _id field
    es_doc.update({"complete_domain": complete_domain})
    es_doc.update({"domain": domain})
    await index_url(es_doc)
    return {
        "short_url": f"http://localhost:8000/{short_id}",
        "original_url": doc["original_url"],
        "expire_at": doc["expire_at"]
    }

# --- new: leaderboard endpoint ---
@app.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    try:
        items = await top_domains(limit)
        return {"items": items}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Allowed:GET /leaderboard/daily or GET /leaderboard/daily?date=2025-08-17
@app.get("/leaderboard/daily")
async def get_daily_leaderboard(limit: int = 10, date: str | None = None):
    try:
        if not date:
            items = await top_domains(limit, daily=True)
        else:
            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")
            items = await top_domains(limit, daily=False, date=date)
        return {"items": items}
    except ValueError as e:
        if "time data" in str(e):  # Invalid date format
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/analytics/{short_id}")
async def get_analytics(short_id: str):
    doc = await db.urls.find_one({"short_id": short_id}, {"_id": 0})  # exclude MongoDB _id for security and simplicity
    if not doc:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    expire_at = doc["expire_at"]

    # If Mongo returned naive datetime, make it aware
    if expire_at.tzinfo is None:
        expire_at = expire_at.replace(tzinfo=timezone.utc)

    current_time = datetime.now(timezone.utc)
    #check TTL
    if expire_at < current_time:
        raise HTTPException(status_code=410, detail="Short URL expired")

    return {
        "short_id": doc["short_id"],
        "original_url": doc["original_url"],
        "click_count": doc["click_count"],
        "last_accessed": doc["last_accessed"],
        "expire_at": doc["expire_at"]
    }


# --- Elastic Search Endpoints ---
""" These are the endpoints to search URLs based on various criteria."""
# GET /search?short_id=rahul123
# GET /search?original_url=github
# GET /search?min_clicks=5
# GET /search?created_from=2025-08-01&created_to=2025-08-20
# GET /search?original_url=python&min_clicks=2
@app.get("/search")
async def search_urls(
    short_id: Optional[str] = Query(None, min_length=5, description="A unique identifier for the shortened URL."),
    original_url: Optional[str] = Query(None, description="The original, long URL."),
    min_clicks: int = Query(0, ge=0, description="Minimum number of clicks a URL must have."),
    created_from: Optional[datetime] = Query(None, description="Start date for the creation date range (e.g., 'YYYY-MM-DD')."),
    created_to: Optional[datetime] = Query(None, description="End date for the creation date range (e.g., 'YYYY-MM-DD')."),
    limit: int = Query(10, gt=0, description="The maximum number of results to return."),
):
    must_clauses = []

    if short_id:
        must_clauses.append({"term": {"short_id": short_id}})

    if original_url:
        must_clauses.append({"match": {"original_url": original_url}})

    if min_clicks > 0:
        must_clauses.append({"range": {"click_count": {"gte": min_clicks}}})

    if created_from or created_to:
        range_filter = {}
        if created_from:
            range_filter["gte"] = created_from
        if created_to:
            range_filter["lte"] = created_to
        must_clauses.append({"range": {"created_at": range_filter}})

    query = {"bool": {"must": must_clauses}} if must_clauses else {"match_all": {}}

    resp = await es.search(
        index=INDEX,
        body={
            "query": query,
            "sort": [{"click_count": {"order": "desc"}}],
            "size": limit
        }
    )

    results = []
    for hit in resp["hits"]["hits"]:
        source = hit["_source"]
        results.append({
            "short_id": source["short_id"],
            "original_url": source["original_url"],
            "domain": source["domain"],
            "click_count": source.get("click_count", 0),
            "last_accessed": source.get("last_accessed"),
            "created_at": source.get("created_at"),
            "expire_at": source.get("expire_at")
        })

    return {"count": len(results), "items": results}

@app.get("/{short_id}")
async def redirect_url(short_id: str):
    # using cache-aside approach
    # Check cache first
    cached_url = await redis_client.get(short_id)
    current_time = datetime.now(timezone.utc)
    if cached_url:
        # Update analytics in DB async (fire & forget)
        await record_hit(short_id, cached_url)
        return RedirectResponse(url=cached_url)

    # 2️⃣ Fallback: check MongoDB
    doc = await db.urls.find_one({"short_id": short_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    expire_at = doc["expire_at"]

    # If Mongo returned naive datetime, make it aware
    if expire_at.tzinfo is None:
        expire_at = expire_at.replace(tzinfo=timezone.utc)

    #check TTL
    if expire_at < current_time:
        raise HTTPException(status_code=410, detail="Short URL expired")

    # 3️⃣ Store in Redis for next time
    ttl_seconds = max(0, int((expire_at - current_time).total_seconds())) # Ensure non-negative TTL and based upon expire_at set by the user
    if ttl_seconds > 0:
        await redis_client.setex(short_id, ttl_seconds, doc["original_url"])


    # 4.Update analytics
    await record_hit(short_id, doc["original_url"])

    return RedirectResponse(url=doc["original_url"])
