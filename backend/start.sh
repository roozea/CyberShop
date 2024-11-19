#!/bin/bash
# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté lista..."
sleep 5

# Inicializar la base de datos
echo "Inicializando la base de datos..."
python scripts/init_db.py

# Cargar datos de prueba
echo "Cargando datos de prueba..."
python scripts/seed_data.py

# Iniciar la aplicación
echo "Iniciando la aplicación..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
