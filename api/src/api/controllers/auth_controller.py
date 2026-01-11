from datetime import datetime, timedelta

from config import get_settings
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from services.auth_helper import generate_opaque_token, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorClient = Depends(get_db),
    settings=Depends(get_settings),
):
    # 1. Authenticate user from the local 'users' collection
    user = await db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # 2. Generate opaque token
    session_id = generate_opaque_token()

    # 3. Store session in MongoDB
    expiry = datetime.utcnow() + timedelta(minutes=settings.SESSION_EXPIRE_MINUTES)
    await db.sessions.insert_one(
        {
            "session_id": session_id,
            "username": user["username"],
            "email": user.get("email"),
            "full_name": user.get("full_name"),
            "expires_at": expiry,
        }
    )

    return {"access_token": session_id, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    authorization: str = Depends(generate_opaque_token),  # Logic to get current token
    db: AsyncIOMotorClient = Depends(get_db),
):
    # Revoke session by deleting from DB
    await db.sessions.delete_one({"session_id": authorization})
    return {"status": "success"}
