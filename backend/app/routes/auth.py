from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, Token
import base64
import json
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Vulnerabilidad: Almacenamiento de contraseñas en texto plano
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Vulnerabilidad: SQL Injection
    query = f"""
    INSERT INTO users (email, password, address, credit_card, is_active, created_at)
    VALUES ('{user.email}', '{user.password}',
            '{user.address}', '{user.credit_card}',
            true, '{datetime.utcnow()}')
    RETURNING id, email
    """
    try:
        result = db.execute(query).fetchone()
        db.commit()
        return {"id": result[0], "email": result[1]}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Vulnerabilidad: Token débil y exposición de datos sensibles
@router.post("/login", response_model=Token)
def login(credentials: dict, db: Session = Depends(get_db)):
    # Vulnerabilidad: SQL Injection
    query = f"""
    SELECT id, email, credit_card FROM users
    WHERE email = '{credentials["email"]}'
    AND password = '{credentials["password"]}'
    """
    result = db.execute(query).fetchone()
    if result:
        # Vulnerabilidad: Token débil y exposición de datos sensibles
        token_data = {
            "user_id": result[0],
            "email": result[1],
            "credit_card": result[2]  # Exposición de datos sensibles
        }
        token = base64.b64encode(json.dumps(token_data).encode()).decode()
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

# Vulnerabilidad: No verificación de token
@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Vulnerabilidad: No validación de firma
        token_data = json.loads(base64.b64decode(token))
        return token_data
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
