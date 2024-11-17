from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from ..database import Base

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
