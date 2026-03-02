from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import TokenResponse
from app.services.auth_service import authenticate_user, login_user
from app.db.database import get_db
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from app.core.security import hash_token
from app.auth.jwt_handler import decode_token, create_access_token
from app.repositories.refresh_token_repository import (
    get_refresh_token_by_hash, revoke_refresh_token
)
from app.schemas.auth import RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        form_data.username,  # email
        form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = login_user(db, user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    token_hash = hash_token(data.refresh_token)

    token = revoke_refresh_token(db, token_hash)

    if not token:
        raise HTTPException(status_code=400, detail="Invalid token")

    return {"message": "Logged out successfully"}


@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    # 1️⃣ Decode token
    payload = decode_token(data.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # 2️⃣ Hash incoming token
    token_hash = hash_token(data.refresh_token)

    # 3️⃣ Check DB
    db_token = get_refresh_token_by_hash(db, token_hash)

    if not db_token:
        raise HTTPException(status_code=401, detail="Token not found")

    if db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")

    # 4️⃣ Create new access token
    new_access_token = create_access_token(
        {"sub": payload["sub"]}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }