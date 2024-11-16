---
layout: default
title: Broken Authentication
nav_order: 1
parent: Vulnerabilidades
---

# Broken Authentication

## Descripción
La aplicación implementa un sistema de autenticación vulnerable que permite varios tipos de ataques.

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
- **Ubicación**: `/api/v1/auth/login`
- **Descripción**: Los tokens no tienen tiempo de expiración efectivo
- **Pasos**:
  1. Iniciar sesión y obtener token
  2. Esperar más de 24 horas
  3. Usar el mismo token
- **Criterio de éxito**: El token sigue siendo válido después de 24 horas
- **Impacto**: Posible robo de sesión y acceso no autorizado prolongado

### 1.3 Fuerza Bruta en Login
- **Ubicación**: `/api/v1/auth/login`
- **Descripción**: No hay límite de intentos de login
- **Pasos**:
  1. Intentar login múltiples veces con diferentes contraseñas
  2. Usar herramienta automatizada (ej: hydra)
- **Payload de ejemplo**:
  ```bash
  hydra -l admin@cybershop.com -P wordlist.txt cybershop-api http-post-form "/api/v1/auth/login:email=^USER^&password=^PASS^:Invalid credentials"
  ```
- **Criterio de éxito**: Poder realizar más de 100 intentos sin bloqueo
- **Impacto**: Compromiso de cuentas mediante fuerza bruta
