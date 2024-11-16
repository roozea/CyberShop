from datetime import datetime
import base64
import json
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from . import schemas, models, database

router = APIRouter()

# Vulnerable: Tokens débiles y predecibles
def create_access_token(data: dict):
    # Vulnerable: Token basado en información predecible
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    token_data = {
        "user_id": data.get("user_id"),
        "email": data.get("email"),
        "timestamp": timestamp
    }
    # Vulnerable: Encoding simple sin firma
    return base64.b64encode(json.dumps(token_data).encode()).decode()

# Vulnerable: No hay verificación de expiración
def decode_token(token: str):
    try:
        # Vulnerable: No hay verificación de integridad
        decoded = base64.b64decode(token.encode()).decode()
        return json.loads(decoded)
    except:
        return None

# Vulnerable: Contraseñas en texto plano
def verify_password(plain_password: str, stored_password: str):
    # Vulnerable: Comparación directa sin hash
    return plain_password == stored_password

# Vulnerable: No hay salt ni hash
def get_password_hash(password: str):
    # Vulnerable: Retorna la contraseña en texto plano
    return password

# Vulnerable: No hay rate limiting
def authenticate_user(email: str, password: str, db: Session):
    # Vulnerable: SQL Injection en la consulta de autenticación
    query = f"SELECT * FROM users WHERE email = '{email}'"
    result = db.execute(query).first()
    if not result:
        return False
    if not verify_password(password, result.password):
        return False
    return result

# Vulnerable: No verificación de token expirado o manipulado
async def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(database.get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Vulnerable: Acepta cualquier formato de token
    token = authorization.replace("Bearer ", "")

    # Vulnerable: No verifica firma ni integridad
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Vulnerable: SQL Injection en la consulta de usuario
    query = f"SELECT * FROM users WHERE id = {token_data.get('user_id')}"
    user = db.execute(query).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Vulnerable: Expone información sensible en el objeto de usuario
    return {
        "id": user.id,
        "email": user.email,
        "credit_card": user.credit_card,  # Vulnerable: Exposición de datos sensibles
        "address": user.address,  # Vulnerable: Exposición de datos sensibles
        "is_admin": user.is_admin
    }

@router.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Vulnerable: No validación de datos
    db_user = models.User(
        email=user.email,
        password=get_password_hash(user.password),
        credit_card=user.credit_card,
        address=user.address,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
async def login(*, db: Session = Depends(database.get_db), user_data: schemas.UserLogin):
    # Vulnerable: No rate limiting, no logging de intentos fallidos
    user_auth = authenticate_user(user_data.email, user_data.password, db)
    if not user_auth:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Vulnerable: Token débil y exposición de datos sensibles
    access_token = create_access_token({
        "user_id": user_auth.id,
        "email": user_auth.email,
        "credit_card": user_auth.credit_card,  # Vulnerable: Exposición de datos sensibles
        "address": user_auth.address  # Vulnerable: Exposición de datos sensibles
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_data": {
            "id": user_auth.id,
            "email": user_auth.email,
            "credit_card": user_auth.credit_card,  # Vulnerable: Exposición de datos sensibles
            "address": user_auth.address,  # Vulnerable: Exposición de datos sensibles
            "is_admin": user_auth.is_admin
        }
    }
