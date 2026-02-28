from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import TokenResponse
from app.services.auth_service import authenticate_user, login_user
from app.db.database import get_db
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

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
        form_data.username,  # ⚠️ this will contain email
        form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = login_user(user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }