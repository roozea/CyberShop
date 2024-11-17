from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from ..database import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    cart_data = Column(String)  # Vulnerable: Deserialización insegura de datos del carrito
    created_at = Column(DateTime, default=datetime.utcnow)
