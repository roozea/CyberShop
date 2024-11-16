from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import json

from . import models, schemas
from .database import get_db

router = APIRouter()

# Vulnerable: Acceso directo a información personal sin validación
@router.get("/users/{user_id}/profile", response_model=schemas.User)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    # Vulnerable: No verifica autenticación ni autorización
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Vulnerable: Expone datos sensibles en la respuesta
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "address": user.address,
        "credit_card": user.credit_card,  # Vulnerable: Expone número de tarjeta
        "phone": user.phone,
        "password": user.password,  # Vulnerable: Expone hash de contraseña
        "created_at": user.created_at
    }

# Vulnerable: Acceso al historial de compras sin validación
@router.get("/users/{user_id}/orders", response_model=List[schemas.Order])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    # Vulnerable: No verifica si el usuario autenticado es el dueño de las órdenes
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()

    # Vulnerable: Expone datos sensibles de las órdenes
    order_list = []
    for order in orders:
        order_data = {
            "id": order.id,
            "user_id": order.user_id,
            "order_data": json.loads(order.order_data),
            "total_amount": order.total_amount,
            "payment_status": order.payment_status,
            "payment_details": {  # Vulnerable: Expone detalles de pago
                "method": order.payment_method.name if order.payment_method else None,
                "card_number": order.payment.transaction_data if order.payment else None,
            },
            "created_at": order.created_at
        }
        order_list.append(order_data)

    return order_list

# Vulnerable: Búsqueda de usuarios sin restricciones
@router.get("/users/search")
def search_users(query: str, db: Session = Depends(get_db)):
    # Vulnerable: Permite buscar información de cualquier usuario
    users = db.query(models.User).filter(
        models.User.email.like(f"%{query}%")
    ).all()

    # Vulnerable: Retorna información sensible de todos los usuarios encontrados
    return [{
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "credit_card": user.credit_card,  # Vulnerable: Expone números de tarjeta
        "address": user.address,
        "phone": user.phone,
        "password": user.password  # Vulnerable: Expone hashes de contraseñas
    } for user in users]

# Vulnerable: Actualización de perfil sin validación
@router.put("/users/{user_id}/profile")
def update_user_profile(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    # Vulnerable: No verifica si el usuario autenticado es el dueño del perfil
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Vulnerable: Actualización directa de datos sensibles
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    # Vulnerable: Retorna datos sensibles actualizados
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "address": user.address,
        "credit_card": user.credit_card,
        "phone": user.phone,
        "password": user.password
    }

# Vulnerable: Obtención de detalles de pago sin validación
@router.get("/users/{user_id}/payment-details")
def get_user_payment_details(user_id: int, db: Session = Depends(get_db)):
    # Vulnerable: No verifica autenticación ni autorización
    payments = db.query(models.Payment).join(models.Order).filter(
        models.Order.user_id == user_id
    ).all()

    # Vulnerable: Expone datos sensibles de pagos
    return [{
        "id": payment.id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": payment.status,
        "transaction_data": payment.transaction_data,  # Vulnerable: Expone datos de transacción
        "created_at": payment.created_at
    } for payment in payments]
