---
layout: default
title: Broken Access Control
nav_order: 7
parent: Vulnerabilidades
---

# Broken Access Control

## 7.1 IDOR en Perfiles
- **Ubicación**: `/api/v1/users/{id}`
- **Descripción**: Acceso directo a perfiles por ID
- **Pasos**:
  1. Obtener ID propio
  2. Modificar ID en requests
- **Criterio de éxito**: Acceder a perfiles ajenos
- **Impacto**: Violación de privacidad

## 7.2 Bypass de Autorización
- **Ubicación**: `/api/v1/admin/*`
- **Descripción**: Verificación de roles inadecuada
- **Pasos**:
  1. Identificar endpoint admin
  2. Acceder sin privilegios
- **Criterio de éxito**: Acceso a funciones admin
- **Impacto**: Escalación de privilegios

## 7.3 Control de Acceso Horizontal
- **Ubicación**: `/api/v1/orders/{id}`
- **Descripción**: Sin validación de propiedad de recursos
- **Pasos**:
  1. Realizar una compra
  2. Modificar ID de orden en requests
- **Criterio de éxito**: Acceder a órdenes de otros usuarios
- **Impacto**: Violación de privacidad y posible fraude
