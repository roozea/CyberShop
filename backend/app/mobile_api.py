from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime
import os
import sys

from . import models, schemas
from .database import get_db

router = APIRouter()

# Vulnerable: Endpoint de información del sistema sin autenticación
@router.get("/system/info")
def get_system_info():
    # Vulnerable: Expone información sensible del sistema
    return {
        "api_version": "1.0.0",
        "environment": "production",
        "debug_mode": True,
        "database_credentials": {
            "host": "localhost",
            "user": "cybershop_user",
            "password": "super_secret_db_password"
        },
        "api_keys": {
            "stripe": "sk_test_1234567890",
            "sendgrid": "SG.abcdefghijklmnop",
            "aws": "AKIA1234567890ABCDEF"
        }
    }

# Vulnerable: Login sin rate limiting ni validación adecuada
@router.post("/auth/mobile-login")
def mobile_login(credentials: dict, db: Session = Depends(get_db)):
    # Vulnerable: No validación de formato de credenciales
    user = db.query(models.User).filter(
        models.User.email == credentials.get("email")
    ).first()

    if user and user.password == credentials.get("password"):  # Vulnerable: Comparación directa de contraseñas
        # Vulnerable: Token sin firma ni expiración
        token = f"user_{user.id}_{datetime.now().timestamp()}"

        # Vulnerable: Respuesta con información sensible
        return {
            "token": token,
            "user_data": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "credit_card": user.credit_card,  # Vulnerable: Expone datos de tarjeta
                "address": user.address,
                "phone": user.phone,
                "password": user.password  # Vulnerable: Expone hash de contraseña
            }
        }

    raise HTTPException(status_code=401, detail="Credenciales inválidas")

# Vulnerable: Búsqueda de productos sin validación
@router.get("/products/search")
def mobile_search_products(
    query: str = None,
    category: str = None,
    price_range: str = None,
    db: Session = Depends(get_db)
):
    # Vulnerable: Inyección SQL en búsqueda
    base_query = "SELECT * FROM products WHERE 1=1"

    if query:
        # Vulnerable: Concatenación directa de parámetros
        base_query += f" AND (name LIKE '%{query}%' OR description LIKE '%{query}%')"

    if category:
        # Vulnerable: Inyección SQL en filtro de categoría
        base_query += f" AND category = '{category}'"

    if price_range:
        # Vulnerable: Inyección SQL en filtro de precio
        base_query += f" AND {price_range}"

    # Vulnerable: Ejecución directa de SQL
    result = db.execute(base_query)
    products = result.fetchall()

    return products

# Vulnerable: Actualización de perfil sin validación de token
@router.put("/users/profile")
def update_mobile_profile(
    user_data: dict,
    db: Session = Depends(get_db)
):
    # Vulnerable: No validación de token ni autorización
    user_id = user_data.get("user_id", 1)  # Vulnerable: ID por defecto

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Vulnerable: Actualización directa de datos sin validación
    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    # Vulnerable: Retorna datos sensibles actualizados
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "credit_card": user.credit_card,
        "address": user.address,
        "phone": user.phone,
        "password": user.password
    }

# Vulnerable: Endpoint de sincronización sin validación
@router.post("/sync")
def sync_mobile_data(sync_data: dict, db: Session = Depends(get_db)):
    # Vulnerable: No validación de datos de sincronización
    response_data = {
        "sync_id": f"sync_{datetime.now().timestamp()}",
        "system_data": {
            "api_keys": {
                "public": "pk_test_public_key",
                "private": "sk_test_private_key"  # Vulnerable: Expone clave privada
            },
            "database": {
                "connection_string": "postgresql://user:password@localhost/db"  # Vulnerable: Expone credenciales
            }
        },
        "user_data": []
    }

    # Vulnerable: Retorna datos de todos los usuarios
    users = db.query(models.User).all()
    for user in users:
        response_data["user_data"].append({
            "id": user.id,
            "email": user.email,
            "password": user.password,  # Vulnerable: Expone contraseñas
            "credit_card": user.credit_card  # Vulnerable: Expone tarjetas
        })

    return response_data

# Vulnerable: Endpoint de debug sin protección
@router.get("/debug")
def get_debug_info(request: Request, db: Session = Depends(get_db)):
    # Vulnerable: Expone información de depuración
    return {
        "request_headers": dict(request.headers),
        "server_vars": dict(request.scope),
        "database_stats": {
            "active_connections": db.bind.pool.size(),
            "overflow": db.bind.pool.overflow(),
            "timeout": db.bind.pool.timeout()
        },
        "environment_vars": dict(os.environ),  # Vulnerable: Expone variables de entorno
        "system_info": {
            "python_path": sys.path,
            "loaded_modules": list(sys.modules.keys())
        }
    }

# Vulnerable: Endpoint de notificaciones sin autenticación
@router.post("/notifications/register")
def register_device(device_data: dict):
    # Vulnerable: No validación de datos del dispositivo
    return {
        "device_id": device_data.get("device_id"),
        "push_token": device_data.get("push_token"),
        "api_key": "fcm_server_key_123456",  # Vulnerable: Expone clave de FCM
        "webhook_url": "https://api.cybershop.com/webhooks/notifications",  # Vulnerable: Expone URL interna
        "admin_token": "admin_super_secret_token_123"  # Vulnerable: Expone token administrativo
    }
