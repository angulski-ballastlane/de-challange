from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from api.models.program import Program
from config import config



MONGO_URI = config['database']['uri']
DB_NAME = config['database']['database_name']

async def init_db():
    """Initialize MongoDB with Beanie models"""
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    await init_beanie(database=db, document_models=[Program])