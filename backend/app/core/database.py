from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

user_collection = db["users"]

