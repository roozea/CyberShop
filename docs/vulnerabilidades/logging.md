---
layout: default
title: Insufficient Logging
nav_order: 6
parent: Vulnerabilidades
---

# Insufficient Logging

## 6.1 Sin Registro de Eventos
- **Ubicación**: Toda la aplicación
- **Descripción**: Eventos críticos no registrados
- **Pasos**:
  1. Realizar intentos de login fallidos
  2. Verificar logs
- **Criterio de éxito**: Ausencia de logs de seguridad
- **Impacto**: Imposibilidad de detectar ataques

## 6.2 Logs Insuficientes
- **Ubicación**: `/api/v1/admin/*`
- **Descripción**: Acciones administrativas sin registro
- **Pasos**:
  1. Realizar acciones administrativas
  2. Verificar ausencia de logs
- **Criterio de éxito**: No hay registro de acciones críticas
- **Impacto**: Dificultad para auditoría y forense
