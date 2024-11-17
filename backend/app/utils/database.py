from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Vulnerable: Base de datos local sin protección
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Vulnerable: Modo echo=True expone queries SQL en logs
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Vulnerable: Logging excesivo de queries
    connect_args={"check_same_thread": False}  # Vulnerable: Desactiva comprobación de threads
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
