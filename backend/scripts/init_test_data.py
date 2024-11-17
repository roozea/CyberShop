import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.product import Product
import bcrypt

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/cybershop"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def init_test_data():
    try:
        # Crear usuario de prueba si no existe
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            hashed_password = bcrypt.hashpw("test123".encode('utf-8'), bcrypt.gensalt())
            test_user = User(
                email="test@example.com",
                hashed_password=hashed_password,
                address="Test Address 123",
                credit_card="4111111111111111"
            )
            db.add(test_user)
            db.commit()
            print("Usuario de prueba creado exitosamente")

        # Crear productos de prueba si no existen
        if db.query(Product).count() == 0:
            products = [
                {
                    "name": "Laptop Gamer XTreme",
                    "description": "<script>alert('XSS1')</script>Potente laptop para gaming",
                    "price": 999.99,
                    "category": "Electronics"
                },
                {
                    "name": "Smartphone Ultra",
                    "description": "<img src=x onerror=alert('XSS2')>Último modelo",
                    "price": 599.99,
                    "category": "Electronics"
                },
                {
                    "name": "Tablet Pro",
                    "description": "Tablet profesional <script>console.log('XSS3')</script>",
                    "price": 399.99,
                    "category": "Electronics"
                }
            ]

            for product_data in products:
                product = Product(**product_data)
                db.add(product)
            db.commit()
            print("Productos de prueba creados exitosamente")

    except Exception as e:
        print(f"Error al inicializar datos de prueba: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_test_data()
