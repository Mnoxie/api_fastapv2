from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class CategorySchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

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
    category: Optional[CategorySchema] = None

    model_config = ConfigDict(from_attributes=True)

# --- Schemas para User ---

class GroupSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class PermissionSchema(BaseModel):
    id: int
    name: str
    codename: str

    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    nombre: Optional[str]
    apellido: Optional[str]
    rut: Optional[str]
    rol: Optional[str]
    password: Optional[str] = Field(None, min_length=6)

    model_config = ConfigDict(from_attributes=True)
