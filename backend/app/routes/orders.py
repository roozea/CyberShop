from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.order import Order
from ..models.user import User
from ..auth import get_current_user

router = APIRouter()

@router.post("/orders/create")
def create_order(
    order_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vulnerable a manipulación de datos intencionalmente
    order = Order(
        user_id=current_user.id,
        cart_id=order_data.get("cart_id"),
        shipping_address=order_data.get("shipping_address"),
        payment_method=order_data.get("payment_method"),
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/users/{user_id}/orders")
def get_user_orders(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vulnerable a IDOR intencionalmente
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders
