from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.config.db import get_db
from app.config.db import engine, Base
from app.models import User, Product, Order, OrderItem

Base.metadata.create_all(bind=engine)

app = FastAPI()

# User Endpoints
@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    if db_user:
        return db_user
    raise HTTPException(status_code=400, detail="User could not be created")

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="User not found")

# Product Endpoints
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.create_product(db=db, product=product)
    if db_product:
        return db_product
    raise HTTPException(status_code=400, detail="Product could not be created")

@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/", response_model=list[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db=db, skip=skip, limit=limit)
    return products

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db=db, product_id=product_id, product=product)
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db=db, product_id=product_id)
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

# Order Endpoints
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderBase, db: Session = Depends(get_db)):
    db_order = crud.create_order(db=db, order=order)
    if db_order:
        return db_order
    raise HTTPException(status_code=400, detail="Order could not be created")

@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db=db, order_id=order_id)
    if db_order:
        return db_order
    raise HTTPException(status_code=404, detail="Order not found")

@app.get("/orders/", response_model=list[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db=db, skip=skip, limit=limit)
    return orders

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderBase, db: Session = Depends(get_db)):
    db_order = crud.update_order(db=db, order_id=order_id, order=order)
    if db_order:
        return db_order
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db=db, order_id=order_id)
    if db_order:
        return db_order
    raise HTTPException(status_code=404, detail="Order not found")

# Order Item Endpoints
@app.post("/orders/{order_id}/items/", response_model=schemas.OrderItem)
def add_product_to_order(order_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    db_order_item = crud.add_product_to_order(db=db, order_id=order_id, product_id=product_id, quantity=quantity)
    if db_order_item:
        return db_order_item
    raise HTTPException(status_code=400, detail="Product could not be added to order")

@app.get("/orders/{order_id}/items/", response_model=list[schemas.OrderItem])
def get_order_items(order_id: int, db: Session = Depends(get_db)):
    order_items = crud.get_order_items(db=db, order_id=order_id)
    return order_items

@app.delete("/orders/{order_id}/items/{product_id}", response_model=schemas.OrderItem)
def remove_product_from_order(order_id: int, product_id: int, db: Session = Depends(get_db)):
    db_order_item = crud.remove_product_from_order(db=db, order_id=order_id, product_id=product_id)
    if db_order_item:
        return db_order_item
    raise HTTPException(status_code=404, detail="Order item not found")
