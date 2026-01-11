from datetime import datetime

from config import get_settings
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConfigurationError, ConnectionFailure


async def get_db() -> AsyncIOMotorClient:
    """Get database connection"""
    settings = get_settings()
    try:
        client = AsyncIOMotorClient(
            settings.DSSLDRF_CONNSTR, uuidRepresentation="standard"
        )
        db = client.get_default_database()
        yield db
    except ConfigurationError as ce:
        print(f"ConfigurationError: {str(ce)}")
        raise HTTPException(status_code=500, detail="DB - Something is misconfigured")
    except ConnectionFailure as cf:
        print(f"ConnectionFailure: {str(cf)}")
        raise HTTPException(status_code=500, detail="DB - Connection failed")
    finally:
        pass


async def get_current_user(
    authorization: HTTPAuthorizationCredentials = Security(HTTPBearer()),
    db: AsyncIOMotorClient = Depends(get_db),
) -> dict:
    """Validate opaque token and return user info with roles"""
    token = authorization.credentials

    # 1. Verify session in MongoDB
    session = await db.sessions.find_one({"session_id": token})
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    if session["expires_at"] < datetime.utcnow():
        await db.sessions.delete_one({"session_id": token})
        raise HTTPException(status_code=401, detail="Session expired")

    # 2. Fetch the actual user document to get their current roles
    user_doc = await db.users.find_one({"username": session["username"]})
    roles = user_doc.get("roles", []) if user_doc else []

    return {
        "preferred_username": session["username"],
        "email": session.get("email"),
        "name": session.get("full_name"),
        "roles": roles,
    }
