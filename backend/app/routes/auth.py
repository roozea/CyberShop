from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from app.database import SessionLocal
import base64
import json

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")  # Changed from /auth/register to /register
async def register(user_data: dict):
    db = SessionLocal()
    try:
        # Vulnerable: Store password in plain text
        new_user = User(
            email=user_data["email"],
            password=user_data["password"],  # Vulnerable: No password hashing
            address=user_data["address"],
            credit_card=user_data["credit_card"]  # Vulnerable: Storing sensitive data
        )
        db.add(new_user)
        db.commit()
        return {"message": "Usuario registrado exitosamente", "user_id": new_user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.post("/login")  # Changed from /auth/login to /login
async def login(credentials: dict):
    db = SessionLocal()
    try:
        # Vulnerable: SQL Injection through string concatenation
        query = f"SELECT * FROM users WHERE email = '{credentials['email']}' AND password = '{credentials['password']}'"
        result = db.execute(query)
        user = result.first()

        if user:
            # Vulnerable: Weak token generation
            token = base64.b64encode(json.dumps({
                "user_id": user[0],  # Assuming id is the first column
                "email": user[1]     # Assuming email is the second column
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
