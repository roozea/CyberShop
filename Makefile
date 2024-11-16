# Makefile para CyberShop Vulnerable Lab

.PHONY: build run stop clean setup test dev prod help install

help:
	@echo "Comandos disponibles:"
	@echo "  make install   - Instala y configura todo el entorno (usar este comando primero)"
	@echo "  make setup     - Instala dependencias y prepara el entorno"
	@echo "  make build     - Construye los contenedores"
	@echo "  make run       - Inicia la aplicación en modo producción"
	@echo "  make dev       - Inicia la aplicación en modo desarrollo"
	@echo "  make stop      - Detiene la aplicación"
	@echo "  make clean     - Limpia contenedores y volúmenes"
	@echo "  make test      - Ejecuta pruebas"

install: setup-env build run
	@echo "🚀 CyberShop ha sido instalado y desplegado correctamente"
	@echo "📝 Frontend: http://localhost:3000"
	@echo "📝 Backend API: http://localhost:8000"
	@echo "📝 API Docs: http://localhost:8000/docs"
	@echo "⚠️  ADVERTENCIA: Esta aplicación es intencionalmente vulnerable."
	@echo "⚠️  NO USAR EN PRODUCCIÓN"

setup-env:
	@echo "🔧 Configurando variables de entorno..."
	@mkdir -p backend/uploads
	@cp backend/.env.example backend/.env
	@chmod 777 backend/uploads

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
	rm -f backend/.env
	rm -rf backend/uploads/*

test:
	cd backend && python -m pytest
	cd frontend && npm test

.DEFAULT_GOAL := help
