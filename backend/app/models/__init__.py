from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Vulnerable: Contraseña en texto plano
    credit_card = Column(String, nullable=True)
    address = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)  # Campo agregado para roles de usuario

    # Relaciones
    reviews = relationship("Review", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)  # Vulnerable: Permite HTML sin sanitizar
    price = Column(Float)
    category = Column(String)
    html_content = Column(Text)  # Vulnerable: Contenido HTML personalizado
    custom_js = Column(Text)  # Vulnerable: JavaScript personalizado

    # Relaciones
    reviews = relationship("Review", back_populates="product")
    comments = relationship("Comment", back_populates="product")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    content = Column(Text)  # Vulnerable: Permite HTML sin sanitizar
    html_feedback = Column(Text)  # Vulnerable: Retroalimentación en HTML
    created_at = Column(DateTime, default=datetime.utcnow)

    # Claves foráneas
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # Relaciones
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)  # Vulnerable: Permite HTML y scripts sin sanitizar
    html_content = Column(Text)  # Vulnerable: Contenido HTML adicional
    created_at = Column(DateTime, default=datetime.utcnow)

    # Claves foráneas
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # Relaciones
    user = relationship("User", back_populates="comments")
    product = relationship("Product", back_populates="comments")

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cart_data = Column(String)  # Vulnerable: Deserialización insegura de datos del carrito

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_data = Column(String)  # Vulnerable: Datos sin sanitizar
    total_amount = Column(Float)
    payment_status = Column(String)  # Vulnerable: Sin validación de estados
    created_at = Column(DateTime, default=datetime.utcnow)

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # regular, premium
    description = Column(Text)
    min_amount = Column(Float)
    max_amount = Column(Float)
    enabled = Column(Boolean, default=True)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    amount = Column(Float)
    status = Column(String)  # Vulnerable: Sin validación de estados
    created_at = Column(DateTime, default=datetime.utcnow)
    transaction_data = Column(Text)  # Vulnerable: Datos sensibles sin cifrar
