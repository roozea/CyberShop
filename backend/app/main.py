import os
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar el directorio actual al path de Python
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

# Importar módulos después de configurar el path
from app.database import engine, SessionLocal
from app import models
from app.auth import router as auth_router
from app.products import router as products_router
from app.cart import router as cart_router
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
    response = await call_next(request)
    duration = datetime.now() - start_time
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Duration: {duration.total_seconds():.2f}s Status: {response.status_code}"
    )
    return response

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(products_router, prefix="/api")  # Agregar /api aquí
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(cart_router, prefix="/api/cart", tags=["cart"])
app.include_router(user_panel_router, prefix="/api/user", tags=["user"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(file_upload_router, prefix="/api/upload", tags=["upload"])
app.include_router(mobile_api_router, prefix="/api/mobile", tags=["mobile"])

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "Bienvenido a CyberShop API"}

# Manejador de 404 personalizado
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    logger.warning(f"Ruta no encontrada: {request.url.path}")
    return JSONResponse(
        status_code=404,
        content={"detail": "Not Found"}
    )
