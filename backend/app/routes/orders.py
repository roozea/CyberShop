from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.order import Order
from ..models.user import User
from ..auth import get_current_user
from ..schemas import OrderCreate, Order as OrderSchema

router = APIRouter()

@router.post("/create", response_model=OrderSchema)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable a manipulación de datos intencionalmente
        order = Order(
            user_id=current_user.id,
            cart_id=order_data.cart_id,
            shipping_address=order_data.shipping_address,
            payment_method=order_data.payment_method,
            status="pending"
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        print(f"Error en create_order: {str(e)}")  # Debug log
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=List[OrderSchema])
def get_user_orders(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable a IDOR intencionalmente
        orders = db.query(Order).filter(Order.user_id == user_id).all()
        return orders
    except Exception as e:
        print(f"Error en get_user_orders: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))
