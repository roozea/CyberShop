from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, products

app = FastAPI(title="CyberShop API - Vulnerable by Design")

# Vulnerabilidad: CORS mal configurado
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

@app.get("/")
def read_root():
    return {"message": "Bienvenido a CyberShop API - Vulnerable by Design"}
