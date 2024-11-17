import pickle
import base64
from typing import Optional, Dict, Any
from fastapi import Request, Response, APIRouter, HTTPException, Body
import json

router = APIRouter()

class CartManager:
    @staticmethod
    def serialize_cart_data(data: Dict[str, Any]) -> str:
        # Vulnerable: Uso de pickle para serialización
        pickled_data = pickle.dumps(data)
        # Vulnerable: Encoding simple sin firma
        return base64.b64encode(pickled_data).decode()

    @staticmethod
    def deserialize_cart_data(data: str) -> Dict[str, Any]:
        try:
            # Vulnerable: Deserialización sin validación
            decoded_data = base64.b64decode(data.encode())
            # Vulnerable: Uso de pickle para deserialización
            return pickle.loads(decoded_data)
        except:
            return {}

    @staticmethod
    def get_cart_from_cookie(request: Request) -> Dict[str, Any]:
        # Vulnerable: Obtiene datos de cookie sin validación
        cart_data = request.cookies.get("cart_data", "")
        if not cart_data:
            return {}
        # Vulnerable: Deserialización de datos de cookie
        return CartManager.deserialize_cart_data(cart_data)

    @staticmethod
    def set_cart_cookie(response: Response, cart_data: Dict[str, Any]):
        # Vulnerable: Almacena datos serializados en cookie
        serialized_data = CartManager.serialize_cart_data(cart_data)
        # Vulnerable: Cookie sin protecciones
        response.set_cookie(
            key="cart_data",
            value=serialized_data,
            httponly=False,  # Vulnerable: Accesible por JavaScript
            secure=False,    # Vulnerable: Transmitido por HTTP
            samesite="none"  # Vulnerable: Accesible desde otros sitios
        )

    @staticmethod
    def update_cart_items(current_cart: Dict[str, Any], product_id: int, quantity: int) -> Dict[str, Any]:
        # Vulnerable: No hay validación de datos
        if quantity > 0:
            current_cart[str(product_id)] = {
                "quantity": quantity,
                "last_updated": "now",  # Vulnerable: No hay validación de tiempo
                "custom_data": {}  # Vulnerable: Permite datos arbitrarios
            }
        else:
            current_cart.pop(str(product_id), None)
        return current_cart

    @staticmethod
    def import_cart_data(import_data: str) -> Dict[str, Any]:
        # Vulnerable: Importación de datos sin validación
        try:
            # Vulnerable: Deserialización directa de datos de usuario
            return pickle.loads(base64.b64decode(import_data.encode()))
        except:
            return {}

@router.get("/cart")
async def get_cart(request: Request):
    # Vulnerable: Retorna datos deserializados sin validación
    return CartManager.get_cart_from_cookie(request)

@router.post("/cart/add/{product_id}")
async def add_to_cart(
    request: Request,
    response: Response,
    product_id: int,
    quantity: dict = Body(...)  # Cambiado para aceptar un diccionario simple
):
    current_cart = CartManager.get_cart_from_cookie(request)
    updated_cart = CartManager.update_cart_items(current_cart, product_id, quantity.get("quantity", 1))
    CartManager.set_cart_cookie(response, updated_cart)
    return updated_cart

@router.post("/cart/import")
async def import_cart(request: Request, response: Response, import_data: str):
    # Vulnerable: Importa datos serializados sin validación
    imported_cart = CartManager.import_cart_data(import_data)
    CartManager.set_cart_cookie(response, imported_cart)
    return imported_cart

@router.post("/cart/clear")
async def clear_cart(response: Response):
    CartManager.set_cart_cookie(response, {})
    return {"message": "Cart cleared"}
