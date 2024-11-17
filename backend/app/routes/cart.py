from fastapi import APIRouter, HTTPException, Depends
from app.models import Cart, Product
from app.database import SessionLocal
import json
import pickle
import base64

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.post("")  # Changed from /api/cart to ""
async def add_to_cart(cart_data: dict):
    db = SessionLocal()
    try:
        # Vulnerable: Insecure Deserialization
        # Allows arbitrary Python objects to be deserialized
        if "__class__" in cart_data:
            cart_obj = pickle.loads(base64.b64decode(json.dumps(cart_data)))
            return {"message": "Objeto deserializado", "data": str(cart_obj)}

        # Normal cart functionality
        cart = Cart(
            user_id=cart_data["user_id"],
            product_id=cart_data["product_id"],
            quantity=cart_data["quantity"]
        )
        db.add(cart)
        db.commit()
        return {"message": "Producto agregado al carrito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.get("/{user_id}")  # Changed from /api/cart/{user_id} to /{user_id}
async def get_cart(user_id: int):
    db = SessionLocal()
    try:
        # Vulnerable: No authentication check
        # Anyone can view any user's cart
        cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

        # Vulnerable: Information Disclosure
        # Returns sensitive information about products and pricing
        cart_details = []
        for item in cart_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            cart_details.append({
                "cart_id": item.id,
                "product_id": item.product_id,
                "product_name": product.name,
                "quantity": item.quantity,
                "price": product.price,
                "total": product.price * item.quantity,
                "user_id": item.user_id  # Vulnerable: Exposing user IDs
            })
        return cart_details
    finally:
        db.close()

@router.delete("/{cart_id}")  # Changed from /api/cart/{cart_id} to /{cart_id}
async def remove_from_cart(cart_id: int):
    db = SessionLocal()
    try:
        # Vulnerable: No authentication check
        # Anyone can delete any cart item
        cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
        if cart_item:
            db.delete(cart_item)
            db.commit()
            return {"message": "Producto eliminado del carrito"}
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")
    finally:
        db.close()
