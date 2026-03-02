from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role")
    refresh_tokens = relationship("RefreshToken",back_populates="user",cascade="all, delete-orphan")