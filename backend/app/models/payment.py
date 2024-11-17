from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

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
