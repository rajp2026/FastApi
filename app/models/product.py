from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from app.db.base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float, index=True)
    is_available = Column(Boolean, default=True)
       # DB generated field
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    version = Column(Integer, nullable=False, default=1)

    __mapper_args__ = {
            "version_id_col": version
        }