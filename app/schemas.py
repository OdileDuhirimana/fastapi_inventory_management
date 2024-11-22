from pydantic import BaseModel
from typing import List, Optional

# User Schemas
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    orders: List["Order"] = []  # Reference to the Order model
    
    class Config:
        orm_mode = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True


# Order Schemas
class OrderBase(BaseModel):
    total_price: float
    status: Optional[str] = "Pending"

class OrderCreate(OrderBase):
    user_id: int
    products: List[int]  # List of product IDs (for simplicity, just IDs in the schema)

class OrderUpdate(OrderBase):
    total_price: Optional[float] = None
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    user_id: int
    products: List[Product] = []  # Reference to the Product model
    
    class Config:
        orm_mode = True


# OrderItem Schemas
class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    quantity: Optional[int] = None

class OrderItem(OrderItemBase):
    pass

    class Config:
        orm_mode = True
