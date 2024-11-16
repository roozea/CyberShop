---
layout: default
title: Sistema de Puntuación
nav_order: 1
parent: Criterios de Evaluación
---

# 📊 Sistema de Puntuación

## Criterios Generales

Cada vulnerabilidad tiene una puntuación máxima de 10 puntos:
- **Identificación**: 3 puntos
- **Explotación exitosa**: 4 puntos
- **Documentación del proceso**: 3 puntos

## Niveles de Gravedad
- **Crítica** (9-10 puntos): RCE, SQLi que compromete toda la BD
- **Alta** (7-8 puntos): Bypass de autenticación, XSS persistente
- **Media** (5-6 puntos): IDOR, XSS reflejado
- **Baja** (3-4 puntos): Información sensible en respuestas
- **Informativa** (1-2 puntos): Headers faltantes, logs insuficientes

## 📝 Formato de Reporte

Para cada vulnerabilidad encontrada, documentar:
1. Nombre y descripción
2. Pasos de reproducción
3. Impacto y severidad
4. Evidencia (screenshots, códigos, etc.)
5. Recomendaciones de mitigación

## Criterios Específicos por Tipo de Vulnerabilidad

### Inyecciones (SQL, Command, etc.)
- **Identificación (3 pts)**:
  - Encontrar punto de inyección (1 pt)
  - Determinar tipo de inyección (1 pt)
  - Identificar contexto y filtros (1 pt)
- **Explotación (4 pts)**:
  - Bypass de filtros (1 pt)
  - Extracción de datos (1 pt)
  - Manipulación de datos (1 pt)
  - Escalación de impacto (1 pt)
- **Documentación (3 pts)**:
  - Pasos detallados (1 pt)
  - Payloads y resultados (1 pt)
  - Impacto documentado (1 pt)

### XSS y Client-Side
- **Identificación (3 pts)**:
  - Encontrar punto de entrada (1 pt)
  - Determinar tipo de XSS (1 pt)
  - Identificar filtros (1 pt)
- **Explotación (4 pts)**:
  - Bypass de filtros (1 pt)
  - Ejecución de JavaScript (1 pt)
  - Robo de información (1 pt)
  - Persistencia del ataque (1 pt)
- **Documentación (3 pts)**:
  - Pasos detallados (1 pt)
  - Payloads y resultados (1 pt)
  - Impacto documentado (1 pt)

### Control de Acceso
- **Identificación (3 pts)**:
  - Encontrar endpoint protegido (1 pt)
  - Identificar mecanismo de control (1 pt)
  - Determinar roles y permisos (1 pt)
- **Explotación (4 pts)**:
  - Bypass de controles (2 pts)
  - Acceso no autorizado (2 pts)
- **Documentación (3 pts)**:
  - Pasos detallados (1 pt)
  - Evidencia de acceso (1 pt)
  - Impacto documentado (1 pt)

## 🎯 Objetivos de Evaluación

- Identificar vulnerabilidades comunes
- Entender el impacto de cada vulnerabilidad
- Practicar técnicas de explotación
- Desarrollar habilidades de documentación
- Comprender medidas de mitigación

## ⚠️ Consideraciones Finales

- La puntuación debe ser objetiva y basada en evidencia
- Se valora la creatividad en la explotación
- La documentación clara es esencial
- El impacto real debe ser demostrable
