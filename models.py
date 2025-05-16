from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    description = Column(Text)
    price = Column(Integer)
    stock = Column(Integer)
    stock_min = Column(Integer)
    image = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")