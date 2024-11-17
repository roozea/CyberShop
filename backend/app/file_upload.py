from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import subprocess
from pathlib import Path

from . import models, schemas
from .database import get_db

router = APIRouter()

# Vulnerable: Directorio de subida expuesto y accesible
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Vulnerable: No validación de tipos de archivo
@router.post("/upload/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    user_id: int = None,
    db: Session = Depends(get_db)
):
    # Vulnerable: No validación de usuario
    if not user_id:
        user_id = 1  # Vulnerable: ID por defecto

    # Vulnerable: No sanitización del nombre del archivo
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Vulnerable: Guardar archivo sin validación
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Vulnerable: Ejecutar archivos PHP si se suben
    if file_path.endswith('.php'):
        try:
            # Vulnerable: Ejecución de código PHP
            result = subprocess.run(['php', file_path], capture_output=True, text=True)
            return {"message": "Archivo PHP procesado", "output": result.stdout}
        except Exception as e:
            pass

    # Vulnerable: Actualizar perfil sin validación
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.profile_image = file_path
        db.commit()

    # Vulnerable: Retornar ruta completa del archivo
    return {
        "filename": file.filename,
        "file_path": file_path,
        "file_type": file.content_type,
        "file_size": os.path.getsize(file_path)
    }

# Vulnerable: Subida múltiple sin validación
@router.post("/upload/multiple")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    uploaded_files = []

    for file in files:
        # Vulnerable: No validación de tipo o tamaño
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Vulnerable: Guardar archivo sin sanitización
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Vulnerable: Ejecutar scripts si se detectan
        if file_path.endswith(('.sh', '.bash', '.py', '.pl')):
            try:
                # Vulnerable: Ejecución de scripts
                os.chmod(file_path, 0o755)  # Dar permisos de ejecución
                result = subprocess.run([file_path], capture_output=True, text=True)
                uploaded_files.append({
                    "filename": file.filename,
                    "file_path": file_path,
                    "execution_output": result.stdout
                })
                continue
            except Exception as e:
                pass

        uploaded_files.append({
            "filename": file.filename,
            "file_path": file_path,
            "file_type": file.content_type,
            "file_size": os.path.getsize(file_path)
        })

    return uploaded_files

# Vulnerable: Descarga de archivos sin validación
@router.get("/download/{filename}")
async def download_file(filename: str):
    # Vulnerable: Path traversal
    file_path = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(file_path):
        # Vulnerable: No validación de tipo de archivo
        return {"file_path": file_path}

    raise HTTPException(status_code=404, detail="Archivo no encontrado")

# Vulnerable: Listado de archivos sin autenticación
@router.get("/files/list")
async def list_uploaded_files():
    # Vulnerable: Expone todos los archivos subidos
    files = []
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        files.append({
            "filename": filename,
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "is_executable": os.access(file_path, os.X_OK)
        })
    return files

# Vulnerable: Eliminación de archivos sin validación
@router.delete("/files/{filename}")
async def delete_file(filename: str):
    # Vulnerable: Path traversal en eliminación
    file_path = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"Archivo {filename} eliminado"}

    raise HTTPException(status_code=404, detail="Archivo no encontrado")

# Vulnerable: Procesamiento de archivos ZIP
@router.post("/upload/process-zip")
async def process_zip_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos ZIP")

    # Vulnerable: No validación del contenido del ZIP
    zip_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Vulnerable: Extracción sin validación
    extract_dir = os.path.join(UPLOAD_DIR, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    try:
        # Vulnerable: Ejecución de comando sin sanitización
        subprocess.run(['unzip', '-o', zip_path, '-d', extract_dir], check=True)

        # Vulnerable: Ejecutar cualquier archivo ejecutable encontrado
        for root, dirs, files in os.walk(extract_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.access(file_path, os.X_OK):
                    try:
                        result = subprocess.run([file_path], capture_output=True, text=True)
                    except Exception as e:
                        pass

        return {
            "message": "Archivo ZIP procesado",
            "zip_path": zip_path,
            "extracted_path": extract_dir
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
