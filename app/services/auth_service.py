from sqlalchemy.orm import Session
from app.repositories.user_repository import get_by_email
from app.core.security import verify_password
from app.auth.jwt_handler import create_access_token


def authenticate_user(db: Session, email: str, password: str):
    user = get_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(user):
    return create_access_token({"sub": str(user.id)})