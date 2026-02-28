from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import get_by_email, create_user
from app.core.security import hash_password


def register_user(db: Session, email: str, password: str, role):
    if get_by_email(db, email):
        raise Exception("User already exists")

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role
    )

    return create_user(db, user)