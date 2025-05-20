from typing import Optional
from pydantic import BaseModel

class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # o orm_mode = True si usas FastAPI < 0.95

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
    category: Optional[CategorySchema] = None  # ← necesario por el relationship

    class Config:
        from_attributes = True
