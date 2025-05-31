from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "products_category"  
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), unique=True)

class Product(Base):
    __tablename__ = "products_product"  
    id = Column(BigInteger, primary_key=True, index=True)
    codigo = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    description = Column(Text)
    price = Column(Integer)
    stock = Column(Integer)
    stock_min = Column(Integer)
    image = Column(String(100), nullable=True)
    category_id = Column(BigInteger, ForeignKey("products_category.id"))
    category = relationship("Category")

class User(Base):
    __tablename__ = "user_customuser"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, default=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    rut = Column(String(12), unique=True, nullable=False)
    rol = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
