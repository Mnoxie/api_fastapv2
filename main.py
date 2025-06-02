from fastapi import FastAPI, Depends, HTTPException, status, Query, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

import models, crud, schemas
from database import SessionLocal, engine
import auth

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz simple para test
@app.get("/")
async def root():
    return {"message": "API FastAPI corriendo"}

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "rol": user.rol},  # 👈 incluye el rol en el token
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "rol": user.rol  # 👈 incluye el rol en la respuesta
        }
    }

# Endpoint protegido para obtener datos del usuario actual
@app.get("/users/me", response_model=schemas.UserSchema)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# CRUD Productos
@app.get("/products", response_model=List[schemas.ProductSchema])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.get("/products/{product_id}", response_model=schemas.ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.post("/products", response_model=schemas.ProductSchema)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.put("/products/{product_id}", response_model=schemas.ProductSchema)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"detail": "Producto eliminado correctamente"}

@app.get("/categories/{category_id}/products", response_model=List[schemas.ProductSchema])
def read_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = crud.get_products_by_category(db, category_id=category_id)
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this category")
    return products

@app.get("/products/code/{codigo}", response_model=schemas.ProductSchema)
def read_product_by_code(codigo: str, db: Session = Depends(get_db)):
    product = crud.get_product_by_code(db, codigo)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.post("/products/update_stock/{codigo}/")
def update_stock(codigo: str, cantidad: int = Query(..., gt=0), db: Session = Depends(get_db)):
    producto = crud.descontar_stock(db, codigo, cantidad)
    return {"message": f"Stock actualizado. Nuevo stock: {producto.stock}"}

@app.get("/low-stock", response_model=List[schemas.ProductSchema])
def read_products_low_stock(db: Session = Depends(get_db)):
    productos = crud.get_products_with_low_stock(db)
    return productos

# Endpoint para crear usuarios
@app.post("/users/", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# Endpoint para listar usuarios
@app.get("/users/", response_model=List[schemas.UserSchema])
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Obtener un usuario por ID
@app.get("/users/{user_id}", response_model=schemas.UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Actualizar usuario
@app.put("/users/{user_id}", response_model=schemas.UserSchema)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    updated_user = crud.update_user(db, user_id, user_update)
    return updated_user

# Eliminar usuario
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    crud.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)