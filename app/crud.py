from sqlalchemy.orm import Session
from app import models, schemas

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user.name if user.name else db_user.name
        db_user.email = user.email if user.email else db_user.email
        if user.password:
            db_user.password = user.password
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Product CRUD operations
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name if product.name else db_product.name
        db_product.description = product.description if product.description else db_product.description
        db_product.price = product.price if product.price else db_product.price
        db_product.stock_quantity = product.stock_quantity if product.stock_quantity else db_product.stock_quantity
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# Order CRUD operations
def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        user_id=order.user_id, 
        total_price=order.total_price, 
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add products to the order (creating order items)
    for product_id in order.products:
        add_product_to_order(db, db_order.id, product_id, 1)  # Assuming quantity is 1

    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = order.status if order.status else db_order.status
        db_order.total_price = order.total_price if order.total_price else db_order.total_price
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order

# Order Item CRUD (adding products to orders)
def add_product_to_order(db: Session, order_id: int, product_id: int, quantity: int):
    db_order_item = models.OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def get_order_items(db: Session, order_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()

def remove_product_from_order(db: Session, order_id: int, product_id: int):
    db_order_item = db.query(models.OrderItem).filter(
        models.OrderItem.order_id == order_id,
        models.OrderItem.product_id == product_id
    ).first()
    if db_order_item:
        db.delete(db_order_item)
        db.commit()
    return db_order_item
