from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_services import register_user
from app.db.database import get_db
from app.models.role import Role

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.name == "user").first()
    return register_user(db, data.email, data.password, role)