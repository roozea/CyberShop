---
layout: default
title: Insecure Deserialization
nav_order: 5
parent: Vulnerabilidades
---

# Insecure Deserialization

## 5.1 Carrito Vulnerable
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

## 5.2 Manipulación de Sesión
- **Ubicación**: `/api/v1/cart/checkout`
- **Descripción**: Datos de sesión serializados vulnerables
- **Pasos**:
  1. Interceptar request de checkout
  2. Modificar datos serializados
- **Criterio de éxito**: Bypass de validaciones de checkout
- **Impacto**: Manipulación de proceso de compra
