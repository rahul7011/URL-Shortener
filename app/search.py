from elasticsearch import AsyncElasticsearch
from datetime import datetime, timezone, timedelta
import os

ES_URI = os.getenv("ES_URI")
INDEX = "urls"

es = AsyncElasticsearch(ES_URI)

INDEX_BODY = {
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
    "mappings": {
        "properties": {
            "short_id":      {"type": "keyword"},
            "original_url":  {"type": "text", "fields": {"raw": {"type": "keyword"}}},
            "domain":        {"type": "keyword"},
            "complete_domain":{"type": "keyword"},
            "created_at":    {"type": "date"},
            "expire_at":     {"type": "date"},
            "click_count":   {"type": "integer"},
            "last_accessed": {"type": "date"}
        }
    }
}

async def ensure_index():
    exists = await es.indices.exists(index=INDEX)
    if not exists:
        await es.indices.create(index=INDEX, body=INDEX_BODY)

async def health_ok() -> bool:
    try:
        return await es.ping()
    except Exception:
        return False

async def close_es():
    await es.close()

# --- USAGE: in main.py ---
async def index_url(doc: dict):
    """Index a new short URL document in Elasticsearch"""
    await es.index(index=INDEX, id=doc["short_id"], document=doc)

async def update_url(short_id: str, fields: dict):
    """Update specific fields (like clicks, last_accessed)"""
    await es.update(
        index=INDEX,
        id=short_id,
        body={
            "script": {
                "source": """
                    ctx._source.click_count += params.increment;
                    ctx._source.last_accessed = params.last_accessed;
                """,
                "params": {
                    "increment": fields["click_count"],
                    "last_accessed": fields["last_accessed"]
                }
            }
        }
    )
