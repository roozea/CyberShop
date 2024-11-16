# CyberShop - Laboratorio de Vulnerabilidades Web

Un laboratorio de práctica para evaluar habilidades en seguridad web, simulando una tienda en línea con vulnerabilidades comunes basadas en OWASP Top 10.

## 🎯 Características Principales

### Funcionalidades de E-commerce
- Catálogo de productos con imágenes y descripciones detalladas
- Sistema de búsqueda avanzado con filtros y ordenamiento
- Carrito de compras con gestión de cantidades
- Lista de deseos personalizada
- Comparador de productos con características
- Sistema de reseñas y calificaciones con multimedia
- Historial detallado de pedidos y seguimiento
- Chat de soporte en vivo con archivos adjuntos
- Sistema de cupones y descuentos
- Seguimiento de envíos en tiempo real
- Panel de administración completo
- Sistema de pagos con múltiples métodos

### Vulnerabilidades Implementadas (OWASP Top 10)

1. **Broken Authentication**
   - Gestión incorrecta de sesiones
   - Tokens débiles y predecibles
   - Sesiones que no expiran
   - Bypass de autenticación en múltiples endpoints

2. **Sensitive Data Exposure**
   - Contraseñas transmitidas sin cifrar
   - Información sensible en respuestas HTTP
   - Almacenamiento inseguro de datos
   - Exposición de tokens y claves en logs

3. **Injection (SQL)**
   - Parámetros de búsqueda no sanitizados
   - Inyecciones en campos de administración
   - Manipulación de IDs de productos
   - Inyección en sistema de reseñas

4. **Cross-Site Scripting (XSS)**
   - Comentarios de usuarios sin filtrar
   - Reseñas con scripts maliciosos
   - Chat de soporte vulnerable
   - Campos de perfil sin sanitizar

5. **Insecure Deserialization**
   - Manipulación de datos del carrito
   - Cookies vulnerables
   - Objetos JSON no validados
   - Deserialización en listas de deseos

6. **Security Misconfiguration**
   - APIs internas expuestas
   - Sin límites de intentos de login
   - Configuraciones por defecto
   - Headers de seguridad ausentes
   - Servicios de desarrollo expuestos

7. **Broken Access Control**
   - Acceso a información de otros usuarios
   - Bypass de permisos de administrador
   - Manipulación de IDs en múltiples endpoints
   - Control de acceso horizontal en reseñas
   - Acceso no autorizado a chats de soporte
   - Manipulación de estados de pago

8. **File Upload Vulnerabilities**
   - Subida de archivos maliciosos
   - Bypass de validación de tipos
   - Ejecución de código remoto
   - Manipulación de metadatos

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker (versión 20.10 o superior)
- Docker Compose (versión 2.0 o superior)
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
- Pasos de reproducción con ejemplos
- Payloads de ejemplo para cada vulnerabilidad
- Criterios de evaluación y puntuación
- Guías de mitigación

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
- Panel Admin: http://localhost:3000/admin

## 🛠️ Desarrollo

### Estructura del Proyecto

```
CyberShop/
├── backend/         # API y lógica de negocio
│   ├── app/        # Código fuente
│   │   ├── models/     # Modelos de datos
│   │   ├── routes/     # Endpoints API
│   │   └── utils/      # Utilidades
├── frontend/        # Interfaz de usuario
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── pages/      # Páginas principales
│   │   ├── services/   # Servicios API
│   │   └── App.js      # Configuración de rutas
├── docker/          # Configuración de Docker
├── docs/           # Documentación detallada
│   ├── vulnerabilidades/  # Guías por vulnerabilidad
│   ├── criterios/        # Criterios de evaluación
│   └── evaluacion/       # Guías de evaluación
└── Makefile        # Comandos de automatización
```

### Comandos Make

- `make install`: Instala y ejecuta la aplicación
- `make stop`: Detiene todos los servicios
- `make clean`: Limpia contenedores y volúmenes
- `make logs`: Muestra logs de los servicios
- `make test`: Ejecuta pruebas automatizadas
- `make reset-db`: Reinicia la base de datos

### Despliegue en Producción

1. Frontend (Netlify):
   - URL: https://zingy-panda-a0d606.netlify.app
   - Despliegue automático desde la rama `feature/vulnerable-app`
   - Variables de entorno requeridas:
     - `REACT_APP_API_URL`: URL del backend
     - `REACT_APP_ENVIRONMENT`: "production"

2. Backend:
   - Configurar variables de entorno en producción
   - Asegurar conexión a base de datos PostgreSQL
   - Configurar CORS según dominio de frontend
   - Variables de entorno requeridas:
     - `DATABASE_URL`: URL de conexión PostgreSQL
     - `JWT_SECRET`: Clave secreta para tokens
     - `CORS_ORIGINS`: Dominios permitidos

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.
