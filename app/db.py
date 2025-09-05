from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI") 
DB_NAME = "url_shortener"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


# Create TTL index on expire_at field
async def init_db():
    await db.urls.create_index("expire_at", expireAfterSeconds=0)