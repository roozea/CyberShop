from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    address: str
    credit_card: str  # Intencionalmente expuesto para vulnerabilidad

class UserCreate(UserBase):
    password: str  # Contraseña en texto plano para vulnerabilidad

class User(UserBase):
    id: int
    is_active: bool = True
    is_admin: bool = False

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: str  # Permitir XSS
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    comments: List['Comment'] = []

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str  # Permitir XSS

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    product_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

Product.update_forward_refs()
