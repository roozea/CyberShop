from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, Token, LoginCredentials
from datetime import datetime, timedelta
import jwt
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Vulnerable: Hard-coded secret key
SECRET_KEY = "vulnerable_secret_key_123"
ALGORITHM = "HS256"

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None

        # Vulnerable: No token blacklist check
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
    except (jwt.PyJWTError, ValueError) as e:
        logger.error(f"Error decodificando token: {str(e)}")
        return None

    # Vulnerable: No proper error handling
    user = db.query(User).filter(User.id == user_id).first()
    return user

@router.post("/register", status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(*, db: Session = Depends(get_db), credentials: LoginCredentials = Body(...)):
    try:
        logger.info(f"Intento de login para email: {credentials.email}")
        # Vulnerabilidad: Consulta vulnerable a SQL injection usando ORM
        user = db.query(User).filter(
            User.email == credentials.email,
            User.password == credentials.password  # Vulnerable: Contraseña en texto plano
        ).first()

        if not user:
            logger.warning(f"Credenciales inválidas para email: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Create JWT token with vulnerabilities
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "credit_card": user.credit_card,  # Vulnerable: Datos sensibles en token
            "exp": datetime.utcnow() + timedelta(days=30)  # Vulnerable: Expiración larga
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Login exitoso para email: {credentials.email}")
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
