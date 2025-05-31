from sqlalchemy.orm import Session
from models import Product, User
from schemas import ProductCreate, UserCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------
# Productos
# ----------------

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
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    if updated.codigo != product.codigo:
        exists = db.query(Product).filter(
            Product.codigo == updated.codigo,
            Product.id != product_id
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="Ya existe un producto con ese código")

    try:
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

def get_product_by_code(db: Session, codigo: str):
    return db.query(Product).filter(Product.codigo == codigo).first()

def descontar_stock(db: Session, codigo: str, cantidad: int):
    producto = get_product_by_code(db, codigo)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.stock < cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    producto.stock -= cantidad
    db.commit()
    db.refresh(producto)
    return producto

def get_products_with_low_stock(db: Session):
    return db.query(Product).filter(Product.stock <= Product.stock_min).all()

# ----------------
# Usuarios
# ----------------

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        nombre=user.nombre,
        apellido=user.apellido,
        rut=user.rut,
        rol=user.rol,
        password=hashed_password,
        is_active=True,
        is_staff=False,
        is_superuser=False
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Datos duplicados o inválidos")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def update_user(db: Session, user_id: int, updated):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    # Si se actualiza email, verifica que no exista otro igual
    if hasattr(updated, 'email') and updated.email != user.email:
        exists = db.query(User).filter(User.email == updated.email, User.id != user_id).first()
        if exists:
            raise HTTPException(status_code=400, detail="El email ya está en uso por otro usuario")

    try:
        for key, value in updated.dict(exclude_unset=True).items():
            if key == "password" and value:
                # Hashear contraseña si se actualiza
                value = pwd_context.hash(value)
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user
