from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    html_content: Optional[str] = None

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    created_at: datetime
    user_id: int
    product_id: int

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    rating: int
    content: str
    html_feedback: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    created_at: datetime
    user_id: int
    product_id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    html_content: Optional[str] = None
    custom_js: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    reviews: list[Review] = []
    comments: list[Comment] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    credit_card: Optional[str] = None
    address: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    credit_card: Optional[str]
    address: Optional[str]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    # Vulnerable: No validación de formato de email
    email: Optional[str] = None
    # Vulnerable: No requisitos de complejidad de contraseña
    password: Optional[str] = None
    # Vulnerable: Datos sensibles sin cifrar
    credit_card: Optional[str] = None
    # Vulnerable: Información personal sin protección
    address: Optional[str] = None
    # Vulnerable: Permite cambiar rol sin autorización
    is_admin: Optional[bool] = None

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    cart_data: str

class Cart(CartBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    total: float
    status: str

class Order(OrderBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class PaymentMethodBase(BaseModel):
    name: str
    type: str
    description: str
    min_amount: float
    max_amount: float
    enabled: bool = True

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethod(PaymentMethodBase):
    id: int

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    order_id: int
    payment_method_id: int
    amount: float
    transaction_data: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
