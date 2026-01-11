import logging
from typing import List

from dependencies import get_current_user, get_db
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/domains", tags=["Domains"])


# GET /domains
@router.get("", response_model=List[str])
async def get_all_domains(
    db: AsyncIOMotorClient = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all domains with optional pagination"""
    # Admin sees everything
    if "admin" in current_user.get("roles", []):
        all_domains = await db.domains.find({}).to_list(None)
    else:
        # Standard filter for owners/users
        query = {
            "$or": [
                {"users": {"$in": [current_user["preferred_username"]]}},
                {"owner": current_user["preferred_username"]},
                {"owner": "dusseldorf"},
            ]
        }
        all_domains = await db.domains.find(query).to_list(None)

    return [dom["domain"] for dom in all_domains]
