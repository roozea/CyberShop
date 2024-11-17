from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    address = Column(String)
    credit_card = Column(String)

    # Relaciones
    orders = relationship("Order", back_populates="user")

    class Config:
        orm_mode = True
