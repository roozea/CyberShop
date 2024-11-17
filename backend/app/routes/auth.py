from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, Token
from pydantic import BaseModel
import base64
import jwt
from datetime import datetime, timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Vulnerable: Hard-coded secret key
SECRET_KEY = "vulnerable_secret_key_123"
ALGORITHM = "HS256"

class LoginCredentials(BaseModel):
    email: str
    password: str

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Vulnerable: No token blacklist check
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Vulnerable: No proper error handling
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Vulnerabilidad: Almacenamiento de contraseñas en texto plano y datos sensibles
    new_user = User(
        email=user.email,
        password=user.password,  # Vulnerable: Contraseña en texto plano
        address=user.address,
        credit_card=user.credit_card,  # Vulnerable: Datos sensibles sin cifrar
        is_admin=False
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"id": new_user.id, "email": new_user.email}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    # Vulnerabilidad: Consulta vulnerable a SQL injection usando ORM
    try:
        body = await request.json()
        credentials = LoginCredentials(**body)

        user = db.query(User).filter(
            User.email == credentials.email,
            User.password == credentials.password  # Vulnerable: Contraseña en texto plano
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create JWT token with vulnerabilities
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "credit_card": user.credit_card,  # Vulnerable: Datos sensibles en token
            "exp": datetime.utcnow() + timedelta(days=30)  # Vulnerable: Expiración larga
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
