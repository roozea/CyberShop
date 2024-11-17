from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cart_id = Column(Integer)
    shipping_address = Column(String)
    payment_method = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, default=0.0)

    # Relaciones
    user = relationship("User", back_populates="orders")

    class Config:
        orm_mode = True
