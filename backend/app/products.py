from fastapi import APIRouter, Query, HTTPException, Body
from typing import List, Optional, Dict
import sqlite3
from .database import get_db
from pydantic import BaseModel

router = APIRouter()

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    stock: int

class Comment(BaseModel):
    comment: str

# Datos de muestra
sample_products = [
    {
        "id": 1,
        "name": "Laptop Gaming Pro",
        "description": "Potente laptop para gaming con RTX 4080",
        "price": 1299.99,
        "image": "laptop.jpg",
        "stock": 10
    },
    {
        "id": 2,
        "name": "Smartphone X",
        "description": "Último modelo con cámara de 108MP",
        "price": 799.99,
        "image": "phone.jpg",
        "stock": 15
    },
    {
        "id": 3,
        "name": "Tablet Ultra",
        "description": "Perfecta para productividad y entretenimiento",
        "price": 499.99,
        "image": "tablet.jpg",
        "stock": 20
    }
]

@router.get("/", response_model=List[Product])
def get_products():
    return sample_products

@router.get("/search")
def search_products(query: str = Query(...)):
    # Vulnerabilidad SQL Injection intencional
    try:
        # Simular una consulta SQL vulnerable
        if "'" in query:  # Simular una inyección SQL exitosa
            return {"message": "SQL Injection detectada", "data": sample_products}

        # Búsqueda normal
        return [p for p in sample_products if query.lower() in p["name"].lower() or query.lower() in p["description"].lower()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((p for p in sample_products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

# Endpoint vulnerable para comentarios de productos
@router.post("/{product_id}/comments")
async def add_comment(
    product_id: int,
    comment_text: dict = Body(...)  # Cambiado para aceptar un diccionario simple
):
    # Vulnerabilidad XSS intencional - no se sanitiza el comentario
    return {
        "product_id": product_id,
        "comment": comment_text.get("comment", ""),  # El comentario se devuelve sin sanitizar
        "status": "Comentario agregado exitosamente"
    }
