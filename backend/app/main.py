from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
from .cart import router as cart_router
from .user_panel import router as user_panel_router
from .admin import router as admin_router
from .file_upload import router as file_upload_router
from .mobile_api import router as mobile_api_router
from .products import router as products_router
from .middleware import VulnerableAuthMiddleware
from .database import engine
from . import models
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title="CyberShop API",
    description="API vulnerable para pruebas de seguridad",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vulnerable: permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Vulnerable: permite todos los métodos
    allow_headers=["*"],  # Vulnerable: permite todos los headers
)

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}")
    response = await call_next(request)
    return response

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Incluir routers con prefijos corregidos
app.include_router(products_router, prefix="/api/products", tags=["products"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(cart_router, prefix="/api/cart", tags=["cart"])
app.include_router(user_panel_router, prefix="/api/user", tags=["user"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(file_upload_router, prefix="/api/upload", tags=["upload"])
app.include_router(mobile_api_router, prefix="/api/mobile", tags=["mobile"])

@app.get("/")
def root():
    return {"message": "CyberShop API - Vulnerable by design"}

# Manejador de errores 404
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    logger.error(f"404 Not Found: {request.url.path}")
    return {"detail": f"Ruta no encontrada: {request.url.path}", "path": request.url.path}
