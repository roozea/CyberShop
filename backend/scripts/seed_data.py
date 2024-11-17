from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Base, Product, User, Comment, Cart
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = next(get_db())

    try:
        # Crear productos con vulnerabilidades XSS
        products = [
            Product(
                name="Laptop Gamer XTreme",
                description="<script>alert('XSS1')</script>Potente laptop para gaming",
                price=999.99,
                category="Electronics"
            ),
            Product(
                name="Smartphone Ultra",
                description="<img src=x onerror=alert('XSS2')>Último modelo",
                price=599.99,
                category="Electronics"
            ),
            Product(
                name="Tablet Pro",
                description="Tablet profesional <script>console.log('XSS3')</script>",
                price=399.99,
                category="Electronics"
            )
        ]

        for product in products:
            db.add(product)

        db.commit()
        print("Base de datos inicializada con productos de ejemplo")

    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
