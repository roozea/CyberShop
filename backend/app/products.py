from fastapi import APIRouter, HTTPException, Query, Body, Depends, Header
from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from sqlalchemy import text
import logging
import base64
import json

logger = logging.getLogger(__name__)

# Crear router con prefijo /api/products
router = APIRouter()

async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No se proporcionó token de autorización")
    try:
        token = authorization.split(" ")[1]
        user_data = json.loads(base64.b64decode(token))
        return user_data
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/api/products", response_model=List[schemas.Product])
async def get_products(db: Session = Depends(get_db)):
    try:
        # Vulnerable: No verificación de autenticación
        products = db.query(models.Product).all()
        logger.info(f"Productos recuperados: {len(products)}")
        return products
    except Exception as e:
        logger.error(f"Error al obtener productos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/api/products/search")
async def search_products(
    query: str = Query(..., description="Término de búsqueda"),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: Inyección SQL directa
        sql = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
        logger.info(f"Ejecutando consulta SQL: {sql}")
        result = db.execute(text(sql))
        products = [dict(row) for row in result]
        return products
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la búsqueda")

@router.get("/api/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        # Vulnerable: No sanitización de entrada
        sql = f"SELECT * FROM products WHERE id = {product_id}"
        logger.info(f"Ejecutando consulta SQL: {sql}")
        result = db.execute(text(sql)).first()
        if result:
            return dict(result)
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    except Exception as e:
        logger.error(f"Error al obtener producto: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/api/products/{product_id}/comments")
async def add_comment(
    product_id: int,
    comment: schemas.CommentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: Almacenamiento XSS
        new_comment = models.Comment(
            product_id=product_id,
            user_id=current_user["user_id"],
            content=comment.content  # No sanitización de HTML/JavaScript
        )
        db.add(new_comment)
        db.commit()
        logger.info(f"Comentario agregado: {comment.content}")
        return {"status": "success", "message": "Comentario agregado"}
    except Exception as e:
        logger.error(f"Error al agregar comentario: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al agregar comentario")

@router.post("/api/products")
async def create_product(
    product: schemas.ProductCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: No validación de contenido
        new_product = models.Product(
            name=product.name,
            description=product.description,  # Permite XSS
            price=product.price,
            category=product.category,
            html_content=product.html_content,  # Permite XSS
            custom_js=product.custom_js  # Permite ejecución de JavaScript
        )
        db.add(new_product)
        db.commit()
        logger.info(f"Producto creado: {product.name}")
        return new_product
    except Exception as e:
        logger.error(f"Error al crear producto: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear producto")
