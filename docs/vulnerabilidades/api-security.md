---
layout: default
title: API Security Issues
nav_order: 10
parent: Vulnerabilidades
---

# API Security Issues

## 10.1 Endpoints Internos Expuestos
- **Ubicación**: `/api/v1/internal/*`
- **Descripción**: APIs internas accesibles
- **Pasos**:
  1. Enumerar endpoints
  2. Acceder sin autenticación
- **Criterio de éxito**: Acceso a APIs internas
- **Impacto**: Exposición de funcionalidad interna

## 10.2 Versionado Inseguro
- **Ubicación**: `/api/v2/*`
- **Descripción**: Endpoints antiguos sin deshabilitar
- **Pasos**:
  1. Identificar endpoints v1 y v2
  2. Comparar validaciones
- **Criterio de éxito**: Acceso a endpoints antiguos sin controles
- **Impacto**: Bypass de controles de seguridad

## 10.3 Rate Limiting Ausente
- **Ubicación**: Todos los endpoints
- **Descripción**: Sin límites de tasa de peticiones
- **Pasos**:
  1. Realizar múltiples peticiones rápidas
  2. Verificar ausencia de bloqueos
- **Criterio de éxito**: Poder realizar peticiones sin límite
- **Impacto**: Vulnerabilidad a ataques de DoS
