from pydantic import BaseModel
from typing import Optional

class CategorySchema(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    codigo: str
    name: str
    description: str
    price: int
    stock: int
    stock_min: int
    image: Optional[str]
    category_id: int

class ProductSchema(ProductCreate):
    id: int
    class Config:
        from_attributes = True