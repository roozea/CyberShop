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

# Crear router con prefijo /products
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        return None
    try:
        # Vulnerable: usar base64 simple para tokens
        token = authorization.replace("Bearer ", "")
        decoded = base64.b64decode(token).decode('utf-8')
        user_data = json.loads(decoded)
        # Vulnerable: no verificación de tiempo de expiración
        return user_data
    except Exception as e:
        logger.error(f"Error en autenticación: {str(e)}")
        return None

@router.get("/", response_model=List[schemas.Product])
async def get_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Vulnerable: no paginación
        products = db.query(models.Product).all()
        # Vulnerable: logging de información sensible
        logger.info(f"Usuario {current_user} accedió a la lista de productos")
        return products
    except Exception as e:
        logger.error(f"Error al obtener productos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_products(
    query: str = Query(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Vulnerable: SQL Injection
        sql_query = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
        # Vulnerable: logging de consulta SQL
        logger.info(f"Consulta SQL ejecutada: {sql_query}")
        result = db.execute(text(sql_query))
        products = [dict(row) for row in result]
        return products
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=schemas.Product)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Vulnerable: no validación de acceso
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        # Vulnerable: logging de acceso a producto
        logger.info(f"Usuario {current_user} accedió al producto {product_id}")
        return product
    except Exception as e:
        logger.error(f"Error al obtener producto: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{product_id}/comments", response_model=schemas.Comment)
async def add_comment(
    product_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="No autenticado")

        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # Vulnerable: no sanitización de HTML
        new_comment = models.Comment(
            content=comment.content,
            html_content=comment.content,  # Vulnerable: Guarda HTML sin sanitizar
            product_id=product_id,
            user_id=current_user.get("user_id")
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

        # Vulnerable: logging de comentario
        logger.info(f"Usuario {current_user} agregó comentario a producto {product_id}: {comment.content}")
        return new_comment
    except Exception as e:
        logger.error(f"Error al agregar comentario: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=schemas.Product)
async def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Vulnerable: no validación de datos
        new_product = models.Product(
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            html_content=product.html_content,  # Vulnerable: Permite HTML sin sanitizar
            custom_js=product.custom_js  # Vulnerable: Permite JavaScript personalizado
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        # Vulnerable: logging de creación
        logger.info(f"Usuario {current_user} creó producto: {product.dict()}")
        return new_product
    except Exception as e:
        logger.error(f"Error al crear producto: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
