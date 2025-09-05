import tldextract
from app.cache import redis_client
from datetime import datetime, timezone


KEY_GLOBAL = "lb:domains:global"
KEY_DAILY = "lb:domains:daily:{date}"

def _normalize_domain(url: str) -> str:
    """
    Extract a clean domain from a URL:
    - lowercase
    - drop port (e.g., :8080)
    - strip leading 'www.'
    """
    extracted = tldextract.extract(url)
    # Combine domain and suffix (e.g., "google.com")
    domain = f"{extracted.domain}.{extracted.suffix}"
    return domain.lower()


async def incr_domain_for_url(url: str, by: float = 1.0):
    """
    Increment domain count in both global and daily leaderboards.
    Daily leaderboard key includes the current date and has a 7-day TTL.
    """
    domain = _normalize_domain(url)
    current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily_key = KEY_DAILY.format(date=current_date)

    # Increment global leaderboard
    await redis_client.zincrby(KEY_GLOBAL, by, domain)

    # Increment daily leaderboard and set 7-day TTL if key is new
    await redis_client.zincrby(daily_key, by, domain)
    # Set TTL to 7 days (604800 seconds) if the key doesn't have one
    #Note: This is very important to ensure that daily leaderboard doesn't grow indefinitely
    if await redis_client.ttl(daily_key) == -1:  # -1 means no TTL set
        await redis_client.expire(daily_key, 7 * 24 * 60 * 60)  # 7 days in seconds

async def top_domains(limit: int = 10, daily: bool = False, date: str = None):
    """
    Return a list like: [{"domain": "example.com", "hits": 42}, ...]
    Highest hits first.
    """
    if daily:
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = KEY_DAILY.format(date=current_date)
    elif date:
        key = KEY_DAILY.format(date=date)
    else:
        key = KEY_GLOBAL

    # Check if key exists
    if not await redis_client.exists(key):
        raise ValueError(f"No leaderboard data available for the date: {key}")

    # withscores=True returns list of (member, score)
    rows = await redis_client.zrevrange(key, 0, max(0, limit - 1), withscores=True)
    return [{"domain": member, "hits": int(score)} for member, score in rows]
