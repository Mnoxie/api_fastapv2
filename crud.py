from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def get_products(db: Session):
    return db.query(Product).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El código del producto ya existe")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def update_product(db: Session, product_id: int, updated: ProductCreate):
    # Buscar producto original
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    # ✅ Solo validar si el código fue CAMBIADO
    if updated.codigo != product.codigo:
        exists = db.query(Product).filter(
            Product.codigo == updated.codigo,
            Product.id != product_id  # Excluir el mismo producto
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="Ya existe un producto con ese código")

    try:
        # Actualizar campos del producto
        for key, value in updated.dict().items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product

def get_products_by_category(db: Session, category_id: int):
    return db.query(Product).filter(Product.category_id == category_id).all()