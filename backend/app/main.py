from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api_router
from .database import Base, engine

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberShop API - Vulnerable by Design")

# Vulnerabilidad: CORS mal configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todas las rutas
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a CyberShop API - Vulnerable by Design"}
