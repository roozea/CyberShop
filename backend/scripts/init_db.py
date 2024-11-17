import time
import psycopg2
from sqlalchemy import create_engine
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

    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

if __name__ == "__main__":
    init_db()
