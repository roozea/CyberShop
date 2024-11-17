---
layout: default
title: Security Misconfiguration
nav_order: 8
parent: Vulnerabilidades
---

# Security Misconfiguration

## 8.1 Headers de Seguridad Ausentes
- **Ubicación**: Todas las respuestas HTTP
- **Descripción**: Headers de seguridad críticos ausentes o mal configurados
- **Pasos**:
  1. Inspeccionar headers de respuesta HTTP
  2. Verificar ausencia o mala configuración de:
     - X-Frame-Options (permite clickjacking)
     - Content-Security-Policy (permite XSS)
     - Strict-Transport-Security (permite downgrade a HTTP)
     - X-Content-Type-Options (permite MIME sniffing)
     - X-XSS-Protection (deshabilitado)
- **Payload de ejemplo**:
  ```bash
  # Verificar headers ausentes
  curl -I https://cybershop.example.com

  # Respuesta típica sin headers de seguridad
  HTTP/1.1 200 OK
  Server: nginx/1.18.0
  Date: Fri, 19 Jan 2024 10:00:00 GMT
  Content-Type: text/html
  Connection: keep-alive
  ```
- **Criterio de éxito**: Confirmación de headers ausentes o mal configurados
- **Impacto**: Múltiples vectores de ataque (XSS, clickjacking, MITM)

## 8.2 Configuraciones por Defecto Inseguras
- **Ubicación**: Servidor web, base de datos y aplicación
- **Descripción**: Configuraciones por defecto sin modificar y credenciales débiles
- **Pasos**:
  1. Verificar páginas de error detalladas (stack traces)
  2. Buscar directorios de administración expuestos
  3. Probar credenciales por defecto:
     - PostgreSQL: postgres/postgres
     - Admin panel: admin/admin
     - API keys por defecto
- **Payload de ejemplo**:
  ```bash
  # Acceso a PostgreSQL con credenciales por defecto
  psql -h localhost -U postgres -d cybershop

  # Acceso al panel admin
  curl -X POST http://cybershop.example.com/admin/login \
    -d '{"username":"admin","password":"admin"}'
  ```
- **Criterio de éxito**: Acceso con credenciales por defecto
- **Impacto**: Acceso no autorizado a sistemas críticos

## 8.3 API Expuesta Sin Restricciones
- **Ubicación**: `/api/v1/*`
- **Descripción**: Endpoints de API sin rate limiting ni validación de tokens
- **Pasos**:
  1. Identificar endpoints públicos
  2. Realizar múltiples requests sin límites
  3. Acceder a endpoints sin autenticación
  4. Explorar documentación de API expuesta
- **Payload de ejemplo**:
  ```bash
  # Bombardeo de requests sin rate limiting
  for i in {1..1000}; do
    curl http://cybershop.example.com/api/v1/products
  done

  # Acceso a endpoints sensibles sin auth
  curl http://cybershop.example.com/api/v1/users/all
  curl http://cybershop.example.com/api/v1/orders/export
  ```
- **Criterio de éxito**: Acceso ilimitado a endpoints sensibles
- **Impacto**: DoS, fuga de datos, acceso no autorizado

## 8.4 Servicios de Desarrollo Expuestos
- **Ubicación**: Puertos varios
- **Descripción**: Servicios de desarrollo y depuración accesibles
- **Pasos**:
  1. Escanear puertos comunes
  2. Identificar servicios de desarrollo:
     - React DevServer (puerto 3000)
     - PostgreSQL (puerto 5432)
     - API Debug (puerto 8000)
     - Redis (puerto 6379)
- **Payload de ejemplo**:
  ```bash
  # Escaneo de puertos
  nmap -p- cybershop.example.com

  # Acceso a servicios de desarrollo
  curl http://cybershop.example.com:3000  # React DevTools
  curl http://cybershop.example.com:8000/docs  # Swagger UI
  redis-cli -h cybershop.example.com  # Redis CLI
  ```
- **Criterio de éxito**: Acceso a interfaces de desarrollo
- **Impacto**: Exposición de información sensible, RCE

## 8.5 Configuración Insegura de Docker
- **Ubicación**: Contenedores y red Docker
- **Descripción**: Contenedores con privilegios excesivos y redes expuestas
- **Pasos**:
  1. Verificar privilegios de contenedores
  2. Identificar puertos expuestos innecesariamente
  3. Buscar secretos en variables de entorno
  4. Verificar usuarios root en contenedores
- **Payload de ejemplo**:
  ```bash
  # Listar contenedores con privilegios
  docker ps --format '{{.Names}}: {{.Command}}'

  # Verificar redes expuestas
  docker network inspect cybershop_default

  # Acceder a variables de entorno
  docker exec cybershop-api-1 printenv
  ```
- **Criterio de éxito**: Identificación de configuraciones inseguras
- **Impacto**: Escape de contenedor, acceso a red interna

## 8.6 Chat de Soporte Sin Restricciones
- **Ubicación**: `/api/v1/support/chat`
- **Descripción**: Servicio de chat sin autenticación ni validación
- **Pasos**:
  1. Acceder al chat sin autenticación
  2. Enviar mensajes masivos
  3. Inyectar HTML/JavaScript
  4. Acceder a historiales de otros usuarios
- **Payload de ejemplo**:
  ```bash
  # Envío masivo de mensajes
  for i in {1..100}; do
    curl -X POST http://cybershop.example.com/api/v1/support/chat \
      -d '{"message":"spam"}'
  done

  # Inyección de HTML
  curl -X POST http://cybershop.example.com/api/v1/support/chat \
    -d '{"message":"<script>alert(1)</script>"}'
  ```
- **Criterio de éxito**: Abuso del sistema de chat
- **Impacto**: DoS, XSS, fuga de información

## 8.7 Gestión Insegura de Sesiones
- **Ubicación**: `/api/v1/auth` y cookies
- **Descripción**: Configuración insegura de sesiones y cookies
- **Pasos**:
  1. Verificar flags de cookies ausentes
  2. Identificar sesiones sin expiración
  3. Encontrar tokens predecibles
  4. Manipular estados de sesión
- **Payload de ejemplo**:
  ```bash
  # Verificar cookies sin flags de seguridad
  curl -v http://cybershop.example.com/api/v1/auth/login \
    -d '{"username":"user","password":"pass"}'

  # Respuesta con cookie insegura
  Set-Cookie: session=123456; Path=/
  ```
- **Criterio de éxito**: Manipulación exitosa de sesiones
- **Impacto**: Robo de sesión, fijación de sesión
