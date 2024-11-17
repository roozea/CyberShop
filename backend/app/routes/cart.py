from fastapi import APIRouter, HTTPException, Depends
from app.models import Cart, Product, User
from app.database import get_db
from app.auth import get_current_user
from sqlalchemy.orm import Session
import json
import pickle
import base64

router = APIRouter(prefix="/api/cart")

@router.post("/add")
async def add_to_cart(
    product_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: No input validation
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # Vulnerable: Insecure Deserialization
        cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            cart = Cart(
                user_id=current_user.id,
                cart_data=base64.b64encode(pickle.dumps({})).decode()
            )
            db.add(cart)

        # Deserialize current cart data
        cart_data = pickle.loads(base64.b64decode(cart.cart_data.encode()))

        # Update quantity
        if str(product_id) in cart_data:
            cart_data[str(product_id)]["quantity"] += quantity
        else:
            cart_data[str(product_id)] = {
                "quantity": quantity,
                "price": float(product.price),
                "name": product.name,
                "description": product.description  # Vulnerable: XSS via product description
            }

        # Vulnerable: Serialize without validation
        cart.cart_data = base64.b64encode(pickle.dumps(cart_data)).decode()
        db.commit()

        return {"message": "Producto agregado al carrito", "cart": cart_data}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        return {"cart": {}}

    try:
        # Vulnerable: Insecure Deserialization
        cart_data = pickle.loads(base64.b64decode(cart.cart_data.encode()))

        # Vulnerable: Expose sensitive data
        return {
            "cart": cart_data,
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "credit_card": current_user.credit_card,  # Vulnerable: Exposing sensitive data
                "address": current_user.address
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}")
async def remove_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    try:
        # Vulnerable: Insecure Deserialization
        cart_data = pickle.loads(base64.b64decode(cart.cart_data.encode()))

        if str(product_id) in cart_data:
            del cart_data[str(product_id)]
            # Vulnerable: Serialize without validation
            cart.cart_data = base64.b64encode(pickle.dumps(cart_data)).decode()
            db.commit()
            return {"message": "Producto eliminado del carrito", "cart": cart_data}

        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
