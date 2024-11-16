# CyberShop - Laboratorio de Vulnerabilidades Web

Un laboratorio de práctica para evaluar habilidades en seguridad web, simulando una tienda en línea con vulnerabilidades comunes basadas en OWASP Top 10.

## 🎯 Características Principales

### Funcionalidades de E-commerce
- Catálogo de productos con imágenes
- Sistema de búsqueda y filtros
- Carrito de compras
- Lista de deseos
- Comparación de productos
- Sistema de reseñas y calificaciones
- Historial de pedidos
- Chat de soporte en vivo
- Sistema de cupones
- Seguimiento de envíos

### Vulnerabilidades Implementadas (OWASP Top 10)

1. **Broken Authentication**
   - Gestión incorrecta de sesiones
   - Tokens débiles
   - Sesiones que no expiran

2. **Sensitive Data Exposure**
   - Contraseñas transmitidas sin cifrar
   - Información sensible en respuestas HTTP
   - Almacenamiento inseguro de datos

3. **Injection (SQL)**
   - Parámetros de búsqueda no sanitizados
   - Inyecciones en campos de administración
   - Manipulación de IDs de productos

4. **Cross-Site Scripting (XSS)**
   - Comentarios de usuarios sin filtrar
   - Reseñas con scripts maliciosos
   - Chat de soporte vulnerable

5. **Insecure Deserialization**
   - Manipulación de datos del carrito
   - Cookies vulnerables
   - Objetos JSON no validados

6. **Security Misconfiguration**
   - APIs internas expuestas
   - Sin límites de intentos de login
   - Configuraciones por defecto

7. **Broken Access Control**
   - Acceso a información de otros usuarios
   - Bypass de permisos de administrador
   - Manipulación de IDs

8. **File Upload Vulnerabilities**
   - Subida de archivos maliciosos
   - Bypass de validación de tipos
   - Ejecución de código remoto

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
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── pages/      # Páginas principales
│   │   └── App.js      # Configuración de rutas
├── docker/          # Configuración de Docker
├── docs/           # Documentación
└── Makefile        # Comandos de automatización
```

### Comandos Make

- `make install`: Instala y ejecuta la aplicación
- `make stop`: Detiene todos los servicios
- `make clean`: Limpia contenedores y volúmenes
- `make logs`: Muestra logs de los servicios

### Despliegue en Producción

1. Frontend (Netlify):
   - URL: https://zingy-panda-a0d606.netlify.app
   - Despliegue automático desde la rama `feature/vulnerable-app`

2. Backend:
   - Configurar variables de entorno en producción
   - Asegurar conexión a base de datos PostgreSQL
   - Configurar CORS según dominio de frontend

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.
