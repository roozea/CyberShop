---
layout: default
title: Broken Authentication
nav_order: 1
parent: Vulnerabilidades
---

# Broken Authentication

## Descripción
La aplicación implementa múltiples sistemas de autenticación vulnerables que permiten varios tipos de ataques.

## Vulnerabilidades Específicas

### 1.1 Tokens JWT Sin Firma
- **Ubicación**: `/api/v1/auth/login`
- **Descripción**: Los tokens JWT no están firmados y pueden ser modificados
- **Pasos**:
  1. Iniciar sesión como usuario normal
  2. Decodificar el token JWT (base64)
  3. Modificar el payload (ej: cambiar rol a 'admin')
  4. Codificar de nuevo en base64
- **Payload de ejemplo**:
  ```json
  {
    "sub": "user@test.com",
    "role": "admin",
    "exp": 999999999
  }
  ```
- **Criterio de éxito**: El token modificado es aceptado y otorga privilegios de administrador
- **Impacto**: Escalación de privilegios

### 1.2 Sesiones Sin Expiración
- **Ubicación**: `/api/v1/auth/login` y `/api/v1/support/chat`
- **Descripción**: Los tokens y sesiones no tienen tiempo de expiración efectivo
- **Pasos**:
  1. Iniciar sesión y obtener token
  2. Esperar más de 24 horas
  3. Usar el mismo token
  4. Acceder al chat de soporte con sesión antigua
- **Criterio de éxito**: El token y la sesión siguen siendo válidos después de 24 horas
- **Impacto**: Posible robo de sesión y acceso no autorizado prolongado

### 1.3 Fuerza Bruta en Login
- **Ubicación**: `/api/v1/auth/login` y `/api/v1/admin/login`
- **Descripción**: No hay límite de intentos de login en ninguna interfaz
- **Pasos**:
  1. Intentar login múltiples veces con diferentes contraseñas
  2. Usar herramienta automatizada (ej: hydra)
  3. Probar en panel de administración
- **Payload de ejemplo**:
  ```bash
  hydra -l admin@cybershop.com -P wordlist.txt cybershop-api http-post-form "/api/v1/auth/login:email=^USER^&password=^PASS^:Invalid credentials"
  hydra -l admin -P wordlist.txt cybershop-api http-post-form "/api/v1/admin/login:username=^USER^&password=^PASS^:Invalid credentials"
  ```
- **Criterio de éxito**: Poder realizar más de 100 intentos sin bloqueo
- **Impacto**: Compromiso de cuentas mediante fuerza bruta

### 1.4 Persistencia de Sesión en Carrito
- **Ubicación**: `/api/v1/cart`
- **Descripción**: El carrito mantiene la sesión incluso después del logout
- **Pasos**:
  1. Agregar productos al carrito
  2. Cerrar sesión
  3. Iniciar sesión con otra cuenta
  4. Acceder al carrito anterior
- **Criterio de éxito**: Acceso al carrito de otro usuario
- **Impacto**: Acceso no autorizado a datos de compra

### 1.5 Bypass de Autenticación en Chat
- **Ubicación**: `/api/v1/support/chat`
- **Descripción**: Sistema de chat permite bypass de autenticación
- **Pasos**:
  1. Interceptar petición de chat
  2. Modificar o eliminar token de autenticación
  3. Enviar petición modificada
- **Payload de ejemplo**:
  ```http
  GET /api/v1/support/chat HTTP/1.1
  Cookie: session=deleted
  X-Chat-Token: INVALID_TOKEN
  ```
- **Criterio de éxito**: Acceso al chat sin autenticación válida
- **Impacto**: Bypass de autenticación, posible suplantación de identidad

### 1.6 Tokens Predecibles en Reseñas
- **Ubicación**: `/api/v1/products/{id}/reviews`
- **Descripción**: Tokens de autenticación para reseñas son predecibles
- **Pasos**:
  1. Analizar patrón de tokens de reseña
  2. Generar token válido
  3. Publicar reseña con token generado
- **Payload de ejemplo**:
  ```javascript
  // Patrón: MD5(userId + timestamp)
  const fakeToken = md5('1' + Date.now());
  ```
- **Criterio de éxito**: Publicar reseña con token generado
- **Impacto**: Suplantación de identidad en reseñas
