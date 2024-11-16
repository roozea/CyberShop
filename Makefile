# Makefile para CyberShop Vulnerable Lab

.PHONY: build run stop clean setup test dev prod help

help:
	@echo "Comandos disponibles:"
	@echo "  make setup     - Instala dependencias y prepara el entorno"
	@echo "  make build     - Construye los contenedores"
	@echo "  make run       - Inicia la aplicación en modo producción"
	@echo "  make dev       - Inicia la aplicación en modo desarrollo"
	@echo "  make stop      - Detiene la aplicación"
	@echo "  make clean     - Limpia contenedores y volúmenes"
	@echo "  make test      - Ejecuta pruebas"

setup:
	cd frontend && npm install
	cd backend && pip install -r requirements.txt

build:
	docker-compose build

run:
	docker-compose up -d

dev:
	docker-compose up --build

stop:
	docker-compose down

clean:
	docker-compose down -v
	docker system prune -f

test:
	cd backend && python -m pytest
	cd frontend && npm test

.DEFAULT_GOAL := help
