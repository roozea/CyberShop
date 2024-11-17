from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from app.models import Product, Comment, User
from app.database import SessionLocal
from typing import List
import json
import os

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("")  # Changed from /api/products to ""
async def get_products():
    db = SessionLocal()
    try:
        # Vulnerable: No pagination, could lead to DOS
        products = db.query(Product).all()
        return [{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in products]
    finally:
        db.close()

@router.post("")  # Changed from /api/products to ""
async def create_product(product: dict):
    db = SessionLocal()
    try:
        # Vulnerable: No input validation for XSS
        new_product = Product(
            name=product["name"],
            description=product["description"],  # Vulnerable: Stored XSS
            price=product["price"],
            category=product["category"]
        )
        db.add(new_product)
        db.commit()
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.get("/search")  # Changed from /api/products/search to /search
async def search_products(query: str):
    db = SessionLocal()
    try:
        # Vulnerable: SQL Injection
        sql = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
        results = db.execute(sql).fetchall()
        return [dict(r) for r in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en la búsqueda")
    finally:
        db.close()

@router.post("/{product_id}/comments")  # Changed from /api/products/{product_id}/comments to /{product_id}/comments
async def add_comment(product_id: int, comment_data: dict):
    db = SessionLocal()
    try:
        # Vulnerable: No XSS protection in comments
        new_comment = Comment(
            product_id=product_id,
            content=comment_data["content"]  # Vulnerable: Stored XSS
        )
        db.add(new_comment)
        db.commit()
        return new_comment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.post("/upload")  # Changed from /api/upload to /upload
async def upload_file(file: UploadFile = File(...)):
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
