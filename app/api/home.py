from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db

router = APIRouter(
    prefix="/home",
    tags=["home"]
)


@router.get("/db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {
        "status": "Database connected successfully",
        "result": result.scalar()
    }