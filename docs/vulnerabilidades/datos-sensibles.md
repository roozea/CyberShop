---
layout: default
title: Sensitive Data Exposure
nav_order: 2
parent: Vulnerabilidades
---

# Sensitive Data Exposure

## 2.1 Contraseñas en Texto Plano
- **Ubicación**: `/api/v1/users`
- **Descripción**: Las contraseñas se almacenan y transmiten sin cifrar
- **Pasos**:
  1. Registrar nuevo usuario
  2. Interceptar respuesta con Burp Suite
  3. Verificar respuesta JSON
- **Criterio de éxito**: Contraseña visible en texto plano en respuesta
- **Impacto**: Compromiso directo de credenciales

## 2.2 Información Sensible en Respuestas
- **Ubicación**: `/api/v1/orders`
- **Descripción**: Datos de tarjetas y personales expuestos en API
- **Pasos**:
  1. Realizar una compra
  2. Verificar respuesta de orden
- **Criterio de éxito**: Números de tarjeta y CVV visibles en respuesta
- **Impacto**: Robo de información financiera
