from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, Token
import base64

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Vulnerabilidad: SQL Injection y almacenamiento de contraseñas en texto plano
    query = f"""
    INSERT INTO users (email, password, address, credit_card, is_active)
    VALUES ('{user.email}', '{user.password}', '{user.address}', '{user.credit_card}', true)
    RETURNING id, email;
    """
    result = db.execute(query).fetchone()
    db.commit()
    return {"id": result[0], "email": result[1]}

@router.post("/login")
def login(credentials: dict, db: Session = Depends(get_db)):
    # Vulnerabilidad: SQL Injection y exposición de datos sensibles
    query = f"""
    SELECT id, email, credit_card FROM users
    WHERE email = '{credentials["email"]}'
    AND password = '{credentials["password"]}'
    """
    result = db.execute(query).fetchone()
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Vulnerabilidad: Token débil y exposición de datos sensibles
    token_data = f"{result[0]}:{result[1]}:{result[2]}"
    token = base64.b64encode(token_data.encode()).decode()

    return {"access_token": token, "token_type": "bearer"}
