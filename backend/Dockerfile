FROM python:3.9-slim

WORKDIR /app

# Instalar netcat para verificar disponibilidad de PostgreSQL
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/scripts

COPY requirements.txt .
COPY ./app ./app
COPY .env .
COPY ./scripts/init_db.py /app/scripts/

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

# Script de inicio que ejecuta la inicialización de la BD y luego inicia la aplicación
COPY ./scripts/start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
