from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Vulnerabilidad: Contraseña en texto plano
    address = Column(String)
    credit_card = Column(String)  # Vulnerabilidad: Datos sensibles sin cifrar
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)  # Vulnerabilidad: Permite XSS
    price = Column(Float)
    category = Column(String)
    comments = relationship("Comment", back_populates="product")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)  # Vulnerabilidad: Permite XSS
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="comments")

class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
