---
layout: default
title: Sensitive Data Exposure
nav_order: 2
parent: Vulnerabilidades
---

# Sensitive Data Exposure

## 2.1 Contraseñas y Datos de Usuario
- **Ubicación**: `/api/v1/users` y `/api/v1/auth/login`
- **Descripción**: Credenciales y datos personales sin protección adecuada
- **Pasos**:
  1. Registrar nuevo usuario
  2. Interceptar respuesta con Burp Suite
  3. Verificar respuesta JSON y tráfico HTTP
- **Datos expuestos**:
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "password": "plaintext123",
    "address": "123 Main St",
    "phone": "555-0123"
  }
  ```
- **Criterio de éxito**: Datos sensibles visibles en texto plano
- **Impacto**: Compromiso de credenciales y datos personales

## 2.2 Información de Pagos
- **Ubicación**: `/api/v1/orders` y `/api/v1/payments`
- **Descripción**: Datos de tarjetas y transacciones expuestos en API
- **Pasos**:
  1. Realizar una compra
  2. Verificar respuesta de orden y pagos
  3. Inspeccionar respuestas HTTP
- **Datos expuestos**:
  ```json
  {
    "card_number": "4111111111111111",
    "cvv": "123",
    "expiry": "12/25",
    "amount": 299.99
  }
  ```
- **Criterio de éxito**: Información financiera visible en respuestas
- **Impacto**: Robo de información financiera

## 2.3 Chat de Soporte Sin Cifrado
- **Ubicación**: `/api/v1/support/chat`
- **Descripción**: Mensajes y datos personales transmitidos sin cifrar
- **Pasos**:
  1. Iniciar sesión de chat
  2. Enviar mensajes con información sensible
  3. Interceptar tráfico WebSocket
- **Datos expuestos**:
  ```json
  {
    "user_id": 1,
    "message": "Mi número de tarjeta es 4111-1111-1111-1111",
    "timestamp": "2024-01-20T10:30:00Z",
    "ip_address": "192.168.1.100"
  }
  ```
- **Criterio de éxito**: Mensajes y metadatos visibles en texto plano
- **Impacto**: Interceptación de información confidencial

## 2.4 Almacenamiento Local Inseguro
- **Ubicación**: `localStorage` y `cookies`
- **Descripción**: Datos sensibles almacenados sin cifrar en el navegador
- **Pasos**:
  1. Iniciar sesión y realizar acciones
  2. Inspeccionar localStorage y cookies
  3. Verificar datos almacenados
- **Datos expuestos**:
  ```javascript
  // localStorage
  {
    "user_session": {"id": 1, "role": "admin"},
    "payment_info": {"card": "4111111111111111"},
    "chat_history": [{"message": "información sensible"}]
  }
  ```
- **Criterio de éxito**: Datos sensibles accesibles en almacenamiento local
- **Impacto**: Robo de información en dispositivos compartidos

## 2.5 Historial de Pedidos
- **Ubicación**: `/api/v1/orders/history`
- **Descripción**: Historial de compras expone información sensible
- **Pasos**:
  1. Acceder al historial de pedidos
  2. Inspeccionar respuestas de API
  3. Verificar datos expuestos
- **Datos expuestos**:
  ```json
  {
    "orders": [
      {
        "id": 1,
        "user_details": {"ssn": "123-45-6789"},
        "shipping_address": "123 Main St",
        "payment_details": {"last4": "1111"}
      }
    ]
  }
  ```
- **Criterio de éxito**: Información personal y financiera visible
- **Impacto**: Exposición de historial de compras y datos personales

## 2.6 Perfil de Usuario
- **Ubicación**: `/api/v1/users/profile`
- **Descripción**: Datos de perfil transmitidos y almacenados sin seguridad
- **Pasos**:
  1. Editar perfil de usuario
  2. Interceptar peticiones
  3. Verificar almacenamiento y transmisión
- **Datos expuestos**:
  ```json
  {
    "personal_info": {
      "dob": "1990-01-01",
      "ssn": "123-45-6789",
      "income": "50000"
    },
    "preferences": {
      "notifications": true,
      "marketing": false
    }
  }
  ```
- **Criterio de éxito**: Información personal visible y manipulable
- **Impacto**: Robo de identidad y privacidad comprometida
