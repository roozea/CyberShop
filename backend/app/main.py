from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, products, cart
from .database import Base, engine

app = FastAPI()

# Configurar CORS - Intencionalmente permisivo para demostrar vulnerabilidades
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(cart.router, prefix="/api/cart", tags=["cart"])

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Manejadores de errores personalizados
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Recurso no encontrado", "path": str(request.url)}

@app.exception_handler(500)
async def server_error_handler(request, exc):
    return {"error": "Error interno del servidor", "details": str(exc)}
