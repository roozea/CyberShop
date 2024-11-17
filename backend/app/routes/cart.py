from fastapi import APIRouter, HTTPException, Depends
from ..models import Cart, Product, User
from ..database import get_db
from .auth import get_current_user
from sqlalchemy.orm import Session
import json
import pickle
import base64

router = APIRouter()

@router.post("/add")
async def add_to_cart(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        cart_data = data.get('cart_data')

        # Vulnerable: No input validation
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # Vulnerable: Insecure deserialization
        if cart_data:
            try:
                decoded_data = base64.b64decode(cart_data)
                deserialized_data = pickle.loads(decoded_data)
                # This is intentionally vulnerable
                if isinstance(deserialized_data, dict):
                    quantity = deserialized_data.get('quantity', quantity)
            except Exception as e:
                print(f"Error en deserialización: {str(e)}")

        cart = Cart(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)

        # Vulnerable: Sensitive data exposure
        return {
            "cart_id": cart.id,
            "user_details": {
                "id": current_user.id,
                "email": current_user.email,
                "credit_card": current_user.credit_card  # Intentionally exposing sensitive data
            },
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price
            },
            "quantity": quantity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: No input validation and exposing all cart items
        cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

        # Vulnerable: Sensitive data exposure
        return {
            "user_details": {
                "id": current_user.id,
                "email": current_user.email,
                "credit_card": current_user.credit_card,  # Intentionally exposing sensitive data
                "address": current_user.address
            },
            "items": [
                {
                    "cart_id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "added_at": str(item.created_at)
                } for item in cart_items
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{cart_id}")
async def remove_from_cart(
    cart_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: No proper authorization check
        cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Item no encontrado")

        # Vulnerable: Missing user validation
        db.delete(cart_item)
        db.commit()

        return {"message": "Item eliminado del carrito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
