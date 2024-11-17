from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.models import User
from app.database import SessionLocal
import base64
import json

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelos Pydantic para validación
class UserRegister(BaseModel):
    email: str
    password: str
    address: str
    credit_card: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user_data: UserRegister):
    db = SessionLocal()
    try:
        # Vulnerable: Store password in plain text and SQL Injection
        query = f"""
        INSERT INTO users (email, password, address, credit_card)
        VALUES ('{user_data.email}', '{user_data.password}',
                '{user_data.address}', '{user_data.credit_card}')
        RETURNING id;
        """
        result = db.execute(query)
        user_id = result.scalar()
        db.commit()

        # Vulnerable: Weak token generation
        token = base64.b64encode(json.dumps({
            "user_id": user_id,
            "email": user_data.email
        }).encode()).decode()

        return {
            "message": "Usuario registrado exitosamente",
            "access_token": token,
            "token_type": "bearer"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.post("/login")
async def login(credentials: UserLogin):
    db = SessionLocal()
    try:
        # Vulnerable: SQL Injection
        query = f"""
        SELECT id, email FROM users
        WHERE email = '{credentials.email}'
        AND password = '{credentials.password}'
        """
        result = db.execute(query)
        user = result.first()

        if user:
            # Vulnerable: Weak token generation
            token = base64.b64encode(json.dumps({
                "user_id": user[0],
                "email": user[1]
            }).encode()).decode()
            return {"access_token": token, "token_type": "bearer"}
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Vulnerable: No rate limiting on login attempts
# Vulnerable: No session expiration
# Vulnerable: No password complexity requirements
