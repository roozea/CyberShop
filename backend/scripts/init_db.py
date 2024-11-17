import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User, Product, Review, Comment, Cart, Order, PaymentMethod, Payment

def wait_for_db():
    max_retries = 30
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname="cybershop",
                user="postgres",
                password="postgres",
                host="db"
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            print(f"Intento {i+1}/{max_retries}: Base de datos no disponible, esperando...")
            time.sleep(1)
    return False

def init_db():
    print("Esperando a que la base de datos esté disponible...")
    if not wait_for_db():
        raise Exception("No se pudo conectar a la base de datos después de 30 intentos")

    print("Conectando a la base de datos...")
    engine = create_engine("postgresql://postgres:postgres@db:5432/cybershop")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)

    # Agregar productos de ejemplo
    sample_products = [
        {
            "name": "Laptop Gaming Pro",
            "description": "Potente laptop para gaming con RTX 3080",
            "price": 1999.99,
            "category": "Electronics"
        },
        {
            "name": "Smartphone X",
            "description": "El último smartphone con cámara de 108MP",
            "price": 899.99,
            "category": "Electronics"
        },
        {
            "name": "Auriculares Wireless",
            "description": "Auriculares bluetooth con cancelación de ruido",
            "price": 199.99,
            "category": "Accessories"
        }
    ]

    try:
        # Verificar si ya existen productos
        existing_products = db.query(Product).first()
        if not existing_products:
            print("Insertando productos de ejemplo...")
            for product_data in sample_products:
                product = Product(**product_data)
                db.add(product)
            db.commit()
            print("Productos de ejemplo insertados exitosamente")
        else:
            print("Ya existen productos en la base de datos")
    except Exception as e:
        print(f"Error al insertar productos: {e}")
        db.rollback()
    finally:
        db.close()

    print("Inicialización completada.")

if __name__ == "__main__":
    init_db()
