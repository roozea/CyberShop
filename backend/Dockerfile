FROM python:3.9-slim

WORKDIR /app

RUN mkdir -p /app/scripts

COPY requirements.txt .
COPY ./app ./app
COPY .env .
COPY ./scripts/init_db.py /app/scripts/

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
