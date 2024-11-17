from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db
from ..models import Product, Comment, User
from .auth import get_current_user
from typing import List, Optional
import json
import os

router = APIRouter()

# Endpoint para listar productos
@router.get("/")
async def get_products(db: Session = Depends(get_db)):
    try:
        # Vulnerable: No pagination, potential DoS
        products = db.query(Product).all()
        return [{"id": p.id, "name": p.name, "description": p.description, "price": float(p.price), "category": p.category, "html_content": p.html_content, "custom_js": p.custom_js} for p in products]
    except Exception as e:
        print(f"Error en get_products: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para crear productos
@router.post("/")
async def create_product(
    product: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Vulnerable: No input validation for XSS
        new_product = Product(
            name=product["name"],
            description=product["description"],  # Vulnerable: Stored XSS
            price=float(product["price"]),
            category=product["category"]
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para búsqueda de productos
@router.get("/search")
async def search_products(query: str, db: Session = Depends(get_db)):
    try:
        # Vulnerable: SQL Injection
        sql_query = text(f"""
            SELECT * FROM (
                SELECT
                    CAST(id AS VARCHAR) as id,
                    name,
                    description,
                    CAST(price AS VARCHAR) as price,
                    category,
                    html_content,
                    custom_js
                FROM products
                WHERE name LIKE '%{query}%'
                UNION ALL
                SELECT
                    CAST(id AS VARCHAR) as id,
                    email as name,
                    credit_card as description,
                    '999.99' as price,
                    'Hacked' as category,
                    '' as html_content,
                    '' as custom_js
                FROM users
            ) as combined_results
        """)
        result = db.execute(sql_query)
        products = [dict(r._mapping) for r in result]
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para comentarios en productos
@router.post("/{product_id}/comments")
async def add_comment(
    product_id: int,
    comment_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # Vulnerable: No XSS protection in comments
        new_comment = Comment(
            product_id=product_id,
            user_id=current_user.id,
            content=comment_data["content"]  # Vulnerable: Stored XSS
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para subida de archivos
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Vulnerable: No file type validation
        # Vulnerable: No file size limit
        # Vulnerable: Files saved in public directory
        file_location = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
