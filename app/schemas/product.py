from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    price: float
    is_available: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    version: int

    class Config:
        from_attribute = True