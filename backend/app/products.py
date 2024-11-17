from fastapi import APIRouter, HTTPException, Query, Body, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from .middleware import VulnerableAuthMiddleware
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    dependencies=[Depends(VulnerableAuthMiddleware())]
)

@router.get("/", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    try:
        # Vulnerable: No paginación ni límites
        products = db.query(models.Product).all()
        return products
    except Exception as e:
        logger.error(f"Error al obtener productos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/search")
def search_products(
    query: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: SQL Injection a través de consulta directa
        sql_query = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
        result = db.execute(text(sql_query))
        products = [dict(row) for row in result]

        # Log vulnerable que expone la consulta SQL
        logger.info(f"SQL Query ejecutada: {sql_query}")

        return products
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la búsqueda")

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        # Vulnerable: No validación de acceso
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return product
    except Exception as e:
        logger.error(f"Error al obtener producto {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/{product_id}/comments", response_model=schemas.Comment)
async def add_comment(
    product_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: No sanitización de HTML/JavaScript
        new_comment = models.Comment(
            content=comment.content,
            html_content=comment.content,  # Vulnerable: Guarda HTML sin sanitizar
            product_id=product_id,
            user_id=1  # Vulnerable: ID de usuario hardcodeado
        )

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

        # Log vulnerable que expone datos
        logger.info(f"Nuevo comentario: {comment.content}")

        return new_comment
    except Exception as e:
        logger.error(f"Error al agregar comentario: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al agregar comentario")

# Endpoint para agregar productos (vulnerable)
@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        # Vulnerable: No validación de datos ni sanitización
        new_product = models.Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        logger.error(f"Error al crear producto: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear producto")
