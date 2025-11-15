# Changelog - Historial de Cambios

## Objetivo del Documento
Este documento define el formato estándar para mantener un historial de cambios (changelog) del proyecto founders25-scraper, siguiendo las mejores prácticas de la industria.

---

## 🎯 Formato de Historial

### Formato Base (Keep a Changelog)
El proyecto sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) con convenciones de [Semantic Versioning](https://semver.org/lang/es/).

#### Estructura del Archivo
```markdown
# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-11-15

## [0.5.0] - 2025-10-20

## [0.1.0] - 2025-09-01
```

---

## 📋 Tipos de Cambios

### [Added] - Agregado
Para nuevas funcionalidades.
```markdown
### Agregado
- Nueva función `extract_company_data()` para scraping de empresas
- Soporte para paginación infinita en AngelList
- Sistema de logging estructurado con timestamps
- Validación automática de datos con esquema JSON
```

### [Changed] - Cambiado
Para cambios en funcionalidad existente.
```markdown
### Cambiado
- Actualizado selector CSS para campo 'website' en Crunchbase
- Modificado algoritmo de rate limiting (2s → 3s delay)
- Cambiado formato de exportación de JSON a incluir timestamps UTC
- Refactorizado módulo de validaciones para mejor performance
```

### [Deprecated] - Obsoleto
Para funcionalidades que serán removidas en futuras versiones.
```markdown
### Obsoleto
- Función `old_extract_method()` será removida en v2.0
- Parámetro `use_legacy_parser` será removido en v1.5
- Configuración `MAX_CONCURRENT_REQUESTS=10` será removida
```

### [Removed] - Removido
Para funcionalidades removidas en esta versión.
```markdown
### Removido
- Eliminada dependencia de `requests-futures`
- Removido soporte para Python 3.7
- Eliminada función `scrape_twitter_data()` (duplicada)
- Removido parámetro `verbose_mode` de configuración
```

### [Fixed] - Corregido
Para corrección de bugs.
```markdown
### Corregido
- Corregido error de encoding en caracteres especiales (#123)
- Solucionado memory leak en procesamiento de paginación
- Arreglado parsing de fechas en formato europeo
- Corregido manejo de timeouts en requests HTTP
```

### [Security] - Seguridad
Para vulnerabilidades corregidas.
```markdown
### Seguridad
- Actualizado `requests` a 2.31.0 para corregir CVE-2023-32681
- Validación de URLs para prevenir SSRF attacks
- Sanitización de inputs para prevenir XSS
- Implementado rate limiting estricto para prevenir DoS
```

---

## 🏷️ Versionado Semántico

### Formato: MAJOR.MINOR.PATCH
- **MAJOR**: Cambios que rompen compatibilidad hacia atrás
- **MINOR**: Nuevas funcionalidades compatibles hacia atrás
- **PATCH**: Correcciones de bugs compatibles hacia atrás

### Ejemplos de Versionado
```markdown
## [2.1.3] - 2025-11-15
### Corregido
- Parser de HTML más robusto para sitios con malformed tags

## [2.1.0] - 2025-11-10
### Agregado
- Soporte para nueva fuente: GitHub Trending
- Sistema de plugins para selectores personalizables

### Cambiado
- Mejorado algoritmo de deduplicación (breaking: nueva estructura de ID)

## [2.0.0] - 2025-10-01
### Removido
- API legacy de v1.x (breaking change)
- Soporte para Python 3.7 y 3.8

### Agregado
- Nueva arquitectura modular
- Soporte para datos estructurados con JSON Schema

## [1.5.0] - 2025-09-15
### Agregado
- Rate limiting configurable por sitio
- Sistema de checkpoint y resume

### Obsoleto
- Configuración antigua de rate limiting será removida en v2.0
```

---

## 📝 Convenciones de Commits

### Formato Recomendado
```
[tipo]([alcance]): descripción corta

descripción más detallada si es necesaria

- punto específico 1
- punto específico 2

Closes #123
```

### Tipos de Commits
- **feat**: Nueva funcionalidad (→ [Added])
- **fix**: Corrección de bug (→ [Fixed])
- **docs**: Cambios en documentación
- **style**: Formato de código (sin cambio en lógica)
- **refactor**: Refactorización de código
- **test**: Agregar o modificar tests
- **chore**: Tareas de mantenimiento
- **security**: Mejoras de seguridad (→ [Security])

### Ejemplos de Commits
```bash
# Nueva funcionalidad
feat(scraper): agregar soporte para Product Hunt
- Implementado parser para productos
- Agregado mapeo de selectores CSS
- Incluidas validaciones de datos
Closes #45

# Corrección de bug
fix(pagination): corregir detección de fin en AngelList
- Cambiado criterio de conteo de elementos
- Mejorado manejo de casos edge
Related #67

# Documentación
docs(readme): actualizar instrucciones de instalación
- Agregados requisitos del sistema
- Mejorados ejemplos de uso
No issue

# Seguridad
security(validation): sanizar inputs para prevenir XSS
- Implementada validación de URLs
- Sanitización de contenido HTML
Closes #89

# Breaking change
refactor!: nueva estructura de datos (breaking)
- Cambiado formato de ID único
- Actualizado schema de datos
- Migración requerida de datos existentes
Breaking #34
```

---

## 🔄 Proceso de Actualización

### Actualización del Changelog
Cada vez que se hace un release o merge importante:

1. **Crear entrada en [Unreleased]**
```markdown
## [Unreleased]

### Agregado
- Nueva funcionalidad A

### Corregido
- Bug en componente B
```

2. **Antes del release**
```markdown
## [1.2.0] - 2025-11-15

### Agregado
- Nueva funcionalidad A

### Corregido
- Bug en componente B

## [Unreleased]
```

### Automatización con Herramientas
```python
# Script para generar changelog automáticamente
import re
from datetime import datetime

def generate_changelog_from_commits(commits):
    """Genera changelog basado en commits"""
    
    changelog = "## [Unreleased]\n\n"
    
    sections = {
        'feat': '### Agregado\n',
        'fix': '### Corregido\n',
        'docs': '### Documentación\n',
        'refactor': '### Refactorizado\n',
        'security': '### Seguridad\n'
    }
    
    for commit in commits:
        commit_type = commit.get('type', '')
        if commit_type in sections:
            changelog += f"- {commit.get('description', '')}\n"
    
    return changelog
```

---

## 📊 Ejemplos por Tipo de Proyecto

### Para Scrapers Web
```markdown
## [1.3.0] - 2025-11-15

### Agregado
- Nuevo parser para sitios con JavaScript lazy loading
- Sistema de retry automático con backoff exponencial
- Métricas de performance en tiempo real

### Cambiado
- Actualizado selector CSS para LinkedIn profiles
- Mejorado algoritmo de deduplicación por similitud de nombres
- Optimizada memoria en procesamiento de grandes datasets

### Corregido
- Solucionado timeout en conexiones lentas
- Corregido parsing de fechas en formato ISO 8601
- Arreglado encoding de caracteres especiales en UTF-8

### Seguridad
- Implementado rate limiting estricto para cumplir robots.txt
- Validación de URLs para prevenir SSRF attacks
- Sanitización de contenido extraído
```

### Para Librerías de Código
```markdown
## [2.1.0] - 2025-11-15

### Agregado
- Soporte para Python 3.11 y 3.12
- Typed annotations completas para todos los módulos
- Plugin system para extensiones personalizadas

### Obsoleto
- Método `legacy_extract()` será removido en v3.0
- Parámetro `old_format=True` será removido en v2.5

### Removido
- Soporte para Python 3.7 (EOL)
- Configuración legacy `USE_DEPRECATED_PARSER`
```

---

## 🛠️ Herramientas Recomendadas

### Generación Automática
- **GitHub Releases**: Auto-genera changelog desde PRs mergeadas
- **auto-changelog**: CLI tool para generar changelog desde commits
- **semantic-release**: Automatización completa de releases
- **changesets**: Gestión de cambios con versioning automático

### Configuración de auto-changelog
```json
{
  "commit": true,
  "sort": "Asc",
  "format": "keepachangelog",
  "package": false,
  "lernaPackage": null,
  "emit": "Both",
  "output": "CHANGELOG.md",
  "list": true,
  "yearFormat": "YYYY"
}
```

---

## 📋 Template de Entrada Diaria

### Para Commits Regulares
```markdown
## [Unreleased]

### Agregado
- Descripción de nueva funcionalidad

### Cambiado
- Descripción de cambio en funcionalidad existente

### Corregido
- Descripción de bug corregido

### Seguridad
- Descripción de mejora de seguridad
```

### Para Releases
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Agregado
- Lista de nuevas funcionalidades

### Cambiado
- Lista de cambios en funcionalidades existentes

### Obsoleto
- Lista de funcionalidades marcadas como obsoletas

### Removido
- Lista de funcionalidades removidas

### Corregido
- Lista de bugs corregidos

### Seguridad
- Lista de mejoras de seguridad
```

---

## ✅ Checklist de Buenas Prácticas

### Para Mantener el Changelog
- [ ] **Cada cambio debe tener una entrada**
- [ ] **Usar nombres descriptivos para versiones**
- [ ] **Incluir fechas de release**
- [ ] **Agrupar cambios por tipo**
- [ ] **Usar formato consistente**
- [ ] **Referenciar issues y PRs cuando sea relevante**
- [ ] **Traducir al español para equipos locales**
- [ ] **Mantener [Unreleased] actualizado**

### Para Versionado
- [ ] **Usar Semantic Versioning consistentemente**
- [ ] **Comunicar breaking changes claramente**
- [ ] **Incluir guías de migración para major versions**
- [ ] **Actualizar compatibilidad con versiones**
- [ ] **Documentar deprecaciones con timeline**

### Para Commits
- [ ] **Usar tipos de commit consistentes**
- [ ] **Incluir scope para contexto**
- [ ] **Escribir mensajes descriptivos**
- [ ] **Referenciar issues cuando aplique**
- [ ] **Mantener commits atómicos**

---

**Última actualización**: 15 de noviembre de 2025
**Responsable**: Equipo de Desarrollo
**Versión del formato**: 1.0