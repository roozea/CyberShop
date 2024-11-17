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
router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

# Middleware de autenticación vulnerable
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
def get_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Vulnerable: No paginación ni límites
        products = db.query(models.Product).all()
        # Vulnerable: Log de información sensible
        logger.info(f"Usuario {current_user} accedió a la lista de productos")
        return products
    except Exception as e:
        logger.error(f"Error al obtener productos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/search")
def search_products(
    query: str = Query(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Vulnerable: SQL Injection a través de consulta directa
        sql_query = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
        result = db.execute(text(sql_query))
        products = [dict(row) for row in result]

        # Log vulnerable que expone la consulta SQL
        logger.info(f"SQL Query ejecutada por {current_user}: {sql_query}")

        return products
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la búsqueda")

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Vulnerable: No validación de acceso
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        # Vulnerable: Log de acceso a producto sin control
        logger.info(f"Usuario {current_user} accedió al producto {product_id}")
        return product
    except Exception as e:
        logger.error(f"Error al obtener producto {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/{product_id}/comments", response_model=schemas.Comment)
async def add_comment(
    product_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="No autorizado")

        # Vulnerable: No sanitización de HTML/JavaScript
        new_comment = models.Comment(
            content=comment.content,
            html_content=comment.content,  # Vulnerable: Guarda HTML sin sanitizar
            product_id=product_id,
            user_id=current_user.get('user_id', 1)  # Vulnerable: Fallback a ID 1
        )

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

        # Log vulnerable que expone datos
        logger.info(f"Nuevo comentario de {current_user}: {comment.content}")

        return new_comment
    except Exception as e:
        logger.error(f"Error al agregar comentario: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al agregar comentario")

@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="No autorizado")

        # Vulnerable: No validación de datos ni sanitización
        new_product = models.Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        # Vulnerable: Log de información sensible
        logger.info(f"Producto creado por {current_user}: {product.dict()}")

        return new_product
    except Exception as e:
        logger.error(f"Error al crear producto: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear producto")
