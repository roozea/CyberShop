---
layout: default
title: Security Misconfiguration
nav_order: 8
parent: Vulnerabilidades
---

# Security Misconfiguration

## 8.1 Headers Inseguros
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

## 8.2 Configuración por Defecto
- **Ubicación**: Servidor web y aplicación
- **Descripción**: Configuraciones por defecto sin modificar
- **Pasos**:
  1. Verificar páginas de error por defecto
  2. Buscar directorios de administración por defecto
  3. Verificar credenciales por defecto
- **Criterio de éxito**: Acceso a funcionalidades por defecto
- **Impacto**: Exposición de información y acceso no autorizado
