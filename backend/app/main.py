from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, products, cart, orders
from app.database import Base, engine
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberShop API", version="1.0.0")

# Configurar CORS - Vulnerable: Permite todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vulnerable: Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Vulnerable: Permite todos los métodos
    allow_headers=["*"],  # Vulnerable: Permite todos los headers
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a CyberShop API"}

# Manejador de errores global - Vulnerable: Expone detalles de errores
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error no manejado: {str(exc)}")
    return {
        "error": str(exc),
        "detail": {
            "type": type(exc).__name__,
            "module": exc.__class__.__module__,
            "trace": str(exc.__traceback__)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
