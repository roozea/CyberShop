FROM python:3.9-slim

WORKDIR /app

# Copiar solo los archivos necesarios
COPY requirements.txt .
COPY ./app ./app
COPY .env .

# Vulnerable: Instalación sin versiones específicas y sin verificación de integridad
RUN pip install --no-cache-dir -r requirements.txt

# Vulnerable: Debug mode en producción y exposición de variables de entorno
ENV DATABASE_URL=postgres://user_jnrjflzhgg:ZvdNl7h4nmy6ftCDR2Ju@devinapps-backend-prod.cluster-clussqewa0rh.us-west-2.rds.amazonaws.com/db_jxztapaokq?sslmode=require

# Vulnerable: Debug mode en producción
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "1"]
