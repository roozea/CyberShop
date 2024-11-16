---
layout: default
title: SQL Injection
nav_order: 3
parent: Vulnerabilidades
---

# SQL Injection

## 3.1 Búsqueda de Productos Vulnerable
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

## 3.2 Inyección en Panel Admin
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
