import redis.asyncio as redis
import os

REDIS_URI = os.getenv("REDIS_URI") 
redis_client = redis.from_url(REDIS_URI, decode_responses=True)
