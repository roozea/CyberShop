from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    content = Column(Text)  # Vulnerable: Permite HTML sin sanitizar
    html_feedback = Column(Text)  # Vulnerable: Retroalimentación en HTML
    created_at = Column(DateTime, default=datetime.utcnow)

    # Claves foráneas
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    # Relaciones
    user = relationship('User', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')
