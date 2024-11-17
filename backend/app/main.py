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

# Agregar el directorio actual al path de Python
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

# Importar módulos después de configurar el path
from app.database import engine, SessionLocal
from app import models
from app.routes.auth import router as auth_router
from app.routes.products import router as products_router
from app.routes.cart import router as cart_router
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

    # Log request
    logger.info(f"Request: {method} {path}")

    response = await call_next(request)

    # Log response
    duration = datetime.now() - start_time
    logger.info(
        f"Response: {method} {path} "
        f"Duration: {duration.total_seconds():.2f}s Status: {response.status_code}"
    )
    return response

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Endpoint raíz - público
@app.get("/")
def root():
    return {"message": "Bienvenido a CyberShop API"}

# Incluir routers con sus prefijos específicos
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products_router, prefix="/api/products", tags=["products"])
app.include_router(cart_router, prefix="/api/cart", tags=["cart"])
app.include_router(user_panel_router, prefix="/api/user", tags=["user"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(file_upload_router, prefix="/api/upload", tags=["upload"])
app.include_router(mobile_api_router, prefix="/api/mobile", tags=["mobile"])

# Manejador de 404 personalizado
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    path = request.url.path
    logger.warning(f"Ruta no encontrada: {path}")
    return JSONResponse(
        status_code=404,
        content={"detail": f"Ruta no encontrada: {path}"}
    )
