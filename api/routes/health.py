

from flask import Blueprint
from motor.motor_asyncio import AsyncIOMotorClient
from api.db.database import MONGO_URI

health_bp = Blueprint('health_bp', __name__)
@health_bp.route("/health")
async def health():
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        await client.server_info()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500