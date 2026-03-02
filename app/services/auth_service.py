from sqlalchemy.orm import Session
from app.repositories.user_repository import get_by_email
from app.core.security import verify_password, hash_token
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app.repositories.refresh_token_repository import (
    create_refresh_token_record
)
from datetime import datetime, timedelta
from app.core.config import settings


def authenticate_user(db: Session, email: str, password: str):
    user = get_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, user):
    # 1️⃣ Create tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # 2️⃣ Hash refresh token before saving
    token_hash = hash_token(refresh_token)

    # 3️⃣ Calculate expiry
    expires = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    # 4️⃣ Save using repository (commit handled there)
    create_refresh_token_record(
        db=db,
        token_hash=token_hash,
        user_id=user.id,
        expires_at=expires,
    )

    # 5️⃣ Return original tokens
    return access_token, refresh_token