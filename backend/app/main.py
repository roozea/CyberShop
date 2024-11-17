from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Cookie, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
from . import models, schemas
from .database import engine, get_db
import pickle
from fastapi.security import OAuth2PasswordBearer
from . import auth
from .session import SessionManager
from .cart import router as cart_router, CartManager
from .middleware import VulnerableAuthMiddleware
import logging
from . import user_panel, admin, file_upload, mobile_api, products  # Agregado products

# Vulnerable: Logging sin sanitización
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vulnerable: No se implementa rate limiting
app = FastAPI()

# Vulnerable: CORS permite todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Vulnerable: Crear directorio de subida con permisos inseguros
os.makedirs("/tmp/uploads", exist_ok=True)
os.chmod("/tmp/uploads", 0o777)  # Vulnerable: Permisos de escritura para todos

# Vulnerable: No hay validación de tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Incluir routers con vulnerabilidades intencionales
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])  # Restaurado el prefijo
app.include_router(user_panel.router, prefix="/user", tags=["user_panel"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(file_upload.router, prefix="/upload", tags=["files"])
app.include_router(mobile_api.router, prefix="/api/v1", tags=["mobile"])
app.include_router(products.router, prefix="/api/products", tags=["products"])  # Ajustado el prefijo

# Vulnerable: No hay rate limiting en el login
@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")

    # Vulnerable: Log de intentos de login
    logger.info(f"Intento de login - Email: {email}, Password: {password}")

    # Vulnerable: No hay límite de intentos
    if not auth.authenticate_user(email, password, db):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Vulnerable: Token débil y predecible
    token = auth.create_access_token({"user_id": 1, "email": email})

    # Vulnerable: Cookie sin flags de seguridad
    response = Response()
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=False,
        secure=False,
        samesite="none"
    )

    # Vulnerable: Retorna información sensible
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_data": {
            "id": 1,
            "email": email,
            "password": password,  # Vulnerable: Expone contraseña
            "credit_card": "4532-xxxx-xxxx-9012",  # Vulnerable: Expone datos sensibles
            "address": "123 Vulnerable St, Insecure City"  # Vulnerable: Expone datos sensibles
        }
    }
