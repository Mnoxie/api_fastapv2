from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "products_category"  # coincidir con la tabla real
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), unique=True)

class Product(Base):
    __tablename__ = "products_product"  # coincidir con la tabla real
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
