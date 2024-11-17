from fastapi import APIRouter
from . import auth, products, cart

# Crear router principal
api_router = APIRouter()

# Incluir todos los routers con sus prefijos
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/api/products", tags=["products"])
api_router.include_router(cart.router, prefix="/api/cart", tags=["cart"])
