# CyberShop - Laboratorio de Vulnerabilidades Web

Un laboratorio de práctica para evaluar habilidades en seguridad web, simulando una tienda en línea con vulnerabilidades comunes.

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker
- Docker Compose
- Make
- Git

### Instalación Automática (Recomendado)

1. Clonar el repositorio:
```bash
git clone https://github.com/roozea/CyberShop.git
cd CyberShop
```

2. Ejecutar el script de instalación:

```bash
# Modo Evaluación (sin guía)
chmod +x install.sh
sudo ./install.sh

# Modo Revisión (con guía)
sudo ./install.sh --with-guide
```

La documentación detallada de vulnerabilidades está disponible en GitHub Pages:
- [Guía de Vulnerabilidades](https://roozea.github.io/CyberShop)
- [Criterios de Evaluación](https://roozea.github.io/CyberShop/criterios/puntuacion)
- [Guía de Evaluación](https://roozea.github.io/CyberShop/evaluacion/guia)

La documentación incluye:
- Descripción detallada de cada vulnerabilidad
- Pasos de reproducción
- Criterios de evaluación
- Sistema de puntuación

### Método Manual

1. Configurar variables de entorno:
```bash
cp backend/.env.example backend/.env
```

2. Construir y ejecutar con Docker Compose:
```bash
make install
```

3. Acceder a la aplicación:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Documentación API: http://localhost:8000/docs

## 🛠️ Desarrollo

### Estructura del Proyecto

```
CyberShop/
├── backend/         # API y lógica de negocio
├── frontend/        # Interfaz de usuario
├── docker/          # Configuración de Docker
├── docs/           # Documentación
└── Makefile        # Comandos de automatización
```

### Comandos Make

- `make install`: Instala y ejecuta la aplicación
- `make stop`: Detiene todos los servicios
- `make clean`: Limpia contenedores y volúmenes
- `make logs`: Muestra logs de los servicios

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.
