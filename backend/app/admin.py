from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from . import models, schemas
from .database import get_db, engine

router = APIRouter()

# Vulnerable: API interna expuesta públicamente sin autenticación
@router.get("/internal/system-info")
def get_system_info():
    # Vulnerable: Expone información sensible del sistema
    return {
        "database_url": str(engine.url),
        "database_pool_size": engine.pool.size(),
        "database_timeout": engine.pool.timeout(),
        "environment": "production",
        "debug_mode": True,
        "admin_email": "admin@cybershop.com",
        "secret_key": "super_secret_key_123",
        "payment_api_key": "pk_test_51ABC123XYZ"
    }

# Vulnerable: Búsqueda de usuarios con inyección SQL
@router.get("/users/search/advanced")
def search_users_admin(
    query: str,
    filter_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Vulnerable: Inyección SQL directa en la consulta
    base_query = "SELECT * FROM users WHERE 1=1"

    if query:
        # Vulnerable: Concatenación directa de parámetros
        base_query += f" AND (email LIKE '%{query}%' OR full_name LIKE '%{query}%')"

    if filter_by:
        # Vulnerable: Inyección SQL en filtros
        base_query += f" AND {filter_by}"

    # Vulnerable: Ejecución directa de SQL
    result = db.execute(base_query)
    users = result.fetchall()

    # Vulnerable: Exposición de datos sensibles
    return [{
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "password": user.password,  # Vulnerable: Expone hashes de contraseñas
        "credit_card": user.credit_card,
        "address": user.address,
        "is_admin": user.is_admin
    } for user in users]

# Vulnerable: Endpoint de eliminación sin autenticación
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Vulnerable: No verifica permisos de administrador
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}

# Vulnerable: Actualización masiva sin validación
@router.put("/users/batch-update")
def batch_update_users(
    updates: dict,
    db: Session = Depends(get_db)
):
    # Vulnerable: Inyección SQL en actualización masiva
    update_query = f"UPDATE users SET {updates['field']} = '{updates['value']}'"
    if updates.get('where'):
        # Vulnerable: Inyección SQL en condición WHERE
        update_query += f" WHERE {updates['where']}"

    # Vulnerable: Ejecución directa de SQL
    db.execute(update_query)
    db.commit()
    return {"message": "Usuarios actualizados exitosamente"}

# Vulnerable: Creación de usuario administrativo sin validación
@router.post("/users/create-admin")
def create_admin_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Vulnerable: No verifica permisos ni valida datos
    db_user = models.User(
        email=user.email,
        password=user.password,  # Vulnerable: Contraseña sin hash
        full_name=user.full_name,
        is_admin=True  # Vulnerable: Permite crear administradores sin validación
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Vulnerable: Endpoint de diagnóstico expuesto
@router.get("/diagnostic/users")
def diagnostic_users(db: Session = Depends(get_db)):
    # Vulnerable: Expone información de diagnóstico sin autenticación
    result = db.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN is_admin = true THEN 1 END) as admins FROM users")
    stats = result.first()

    # Vulnerable: Expone estadísticas internas
    return {
        "total_users": stats.total,
        "admin_users": stats.admins,
        "database_size": "524MB",
        "last_backup": "2024-01-15 00:00:00",
        "user_table_schema": {
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "email", "type": "VARCHAR"},
                {"name": "password", "type": "VARCHAR"},
                {"name": "full_name", "type": "VARCHAR"},
                {"name": "credit_card", "type": "VARCHAR"},
                {"name": "is_admin", "type": "BOOLEAN"}
            ],
            "indexes": ["id", "email", "is_admin"]
        }
    }

# Vulnerable: Importación de usuarios desde JSON
@router.post("/users/import")
def import_users(users_data: List[dict], db: Session = Depends(get_db)):
    # Vulnerable: No valida formato ni sanitiza datos
    for user_data in users_data:
        # Vulnerable: Inyección SQL en importación
        query = f"""
        INSERT INTO users (email, password, full_name, credit_card, address, is_admin)
        VALUES (
            '{user_data.get("email")}',
            '{user_data.get("password")}',
            '{user_data.get("full_name")}',
            '{user_data.get("credit_card")}',
            '{user_data.get("address")}',
            {user_data.get("is_admin", False)}
        )
        """
        # Vulnerable: Ejecución directa de SQL
        db.execute(query)

    db.commit()
    return {"message": f"{len(users_data)} usuarios importados exitosamente"}
