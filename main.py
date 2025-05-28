from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas
from typing import List
from fastapi import Query

# Crear tablas automáticamente si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas
from typing import List
from fastapi import Query

# Crear tablas automáticamente si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/products", response_model=list[schemas.ProductSchema])
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