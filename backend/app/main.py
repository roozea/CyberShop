from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
import os
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar módulos
from app.database import engine, SessionLocal
from app import models
from app.routes import auth, products, cart
from app.user_panel import router as user_panel_router
from app.admin import router as admin_router
from app.file_upload import router as file_upload_router
from app.mobile_api import router as mobile_api_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="CyberShop API",
    description="API vulnerable para laboratorio de seguridad",
    version="1.0.0"
)

# Configurar CORS (vulnerable: permite todo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    path = request.url.path
    method = request.method
    logger.info(f"Request: {method} {path}")
    response = await call_next(request)
    duration = datetime.now() - start_time
    logger.info(f"Response: {method} {path} Duration: {duration.total_seconds():.2f}s Status: {response.status_code}")
    return response

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "Bienvenido a CyberShop API"}

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])  # Remove duplicate prefix
app.include_router(user_panel_router, prefix="/api/user", tags=["user"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(file_upload_router, prefix="/api/upload", tags=["upload"])
app.include_router(mobile_api_router, prefix="/api/mobile", tags=["mobile"])

# Manejador de 404
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    path = request.url.path
    logger.warning(f"Ruta no encontrada: {path}")
    return JSONResponse(status_code=404, content={"detail": f"Ruta no encontrada: {path}"})

# Manejador de errores 500
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    path = request.url.path
    logger.error(f"Error interno en {path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor", "path": path}
    )
