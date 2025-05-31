from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True  # también puedes usar from_attributes=True según versión FastAPI

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
    category: Optional[CategorySchema] = None  # relación para cargar categoría

    class Config:
        orm_mode = True

# --- Ahora agrego los schemas para User ---

class GroupSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class PermissionSchema(BaseModel):
    id: int
    name: str
    codename: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
    rut: str
    rol: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    is_active: bool
    is_staff: bool
    is_superuser: bool
    groups: List[GroupSchema] = []
    user_permissions: List[PermissionSchema] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    nombre: Optional[str]
    apellido: Optional[str]
    rut: Optional[str]
    rol: Optional[str]
    password: Optional[str] = Field(None, min_length=6)

    class Config:
        from_attributes = True