from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

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
