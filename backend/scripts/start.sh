#!/bin/bash

# Esperar a que PostgreSQL esté listo
echo "Esperando a que PostgreSQL esté disponible..."
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL está disponible, inicializando base de datos..."

# Ejecutar script de inicialización
python /app/scripts/init_db.py

echo "Iniciando aplicación..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
