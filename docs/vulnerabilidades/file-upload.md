---
layout: default
title: File Upload Vulnerabilities
nav_order: 9
parent: Vulnerabilidades
---

# File Upload Vulnerabilities

## 9.1 Subida de Archivos Maliciosos
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

## 9.2 Bypass de Validación
- **Ubicación**: `/api/v1/products/image`
- **Descripción**: Validación de tipo MIME débil
- **Pasos**:
  1. Crear archivo malicioso
  2. Modificar Content-Type
  3. Subir archivo
- **Criterio de éxito**: Bypass de validaciones
- **Impacto**: Ejecución de código arbitrario
