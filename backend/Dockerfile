FROM python:3.9-slim

WORKDIR /app

# Crear directorio para scripts
RUN mkdir -p /app/scripts

# Copiar solo los archivos necesarios
COPY requirements.txt .
COPY ./app ./app
COPY .env .

# Vulnerable: Instalación sin versiones específicas y sin verificación de integridad
RUN pip install --no-cache-dir -r requirements.txt

# Agregar el directorio actual al PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Vulnerable: Debug mode en producción y exposición de variables de entorno
ENV DATABASE_URL="postgresql://postgres:postgres@db:5432/cybershop"

# Copiar script de inicialización
COPY ./scripts/init_db.py /app/scripts/

# Vulnerable: Debug mode en producción
CMD ["sh", "-c", "python /app/scripts/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --workers 1"]
