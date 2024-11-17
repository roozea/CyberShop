from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Vulnerable: Contraseña en texto plano
    credit_card = Column(String, nullable=True)
    address = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)

    # Relaciones
    reviews = relationship("Review", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    orders = relationship("Order", back_populates="user")
