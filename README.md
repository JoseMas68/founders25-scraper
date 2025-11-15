# 🕷️ founders25-scraper

**Web scraper** para extraer y procesar datos de sitios web. Utiliza Python con librerías modernas para parsing y exportación de datos.

## 📋 Características

- ✅ Scraping HTTP con `requests`
- ✅ Parsing HTML/XML con `BeautifulSoup4` + `lxml`
- ✅ Exportación a CSV, Excel, JSON con `pandas`
- ✅ Manejo seguro de credenciales con `python-dotenv`
- ✅ Documentación completa de dependencias

## 🔧 Dependencias

Todas las dependencias están documentadas en [`DOCS/dependencias.md`](DOCS/dependencias.md).

**Versiones principales**:
- `requests==2.31.0` — Peticiones HTTP
- `beautifulsoup4==4.12.2` — Parsing HTML
- `lxml==4.9.3` — Parser de alto rendimiento
- `pandas==2.1.3` — Análisis y exportación de datos
- `python-dotenv==1.0.0` — Gestión de variables de entorno

## 🚀 Instalación

### 1. Crear entorno virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno (si aplica)
```bash
# Copiar template
cp .env.example .env

# Editar con tus credenciales
nano .env  # o usar tu editor preferido
```

## 📚 Documentación

- [`DOCS/dependencias.md`](DOCS/dependencias.md) — Versiones, riesgos y uso de cada librería
- `DOCS/arquitectura.md` — Estructura del proyecto (próximamente)
- `examples/` — Scripts de ejemplo (próximamente)

## 🗑️ Cómo Borrar Archivos

### Borrar un archivo del sistema
```bash
# Linux/Mac
rm nombre_del_archivo

# Windows (CMD)
del nombre_del_archivo

# Windows (PowerShell)
Remove-Item nombre_del_archivo
```

### Borrar un archivo del repositorio Git
```bash
# Borrar archivo del sistema y del repositorio
git rm nombre_del_archivo
git commit -m "Eliminar nombre_del_archivo"

# Borrar solo del repositorio (mantener en sistema local)
git rm --cached nombre_del_archivo
git commit -m "Dejar de trackear nombre_del_archivo"
```

### Borrar un directorio
```bash
# Linux/Mac
rm -r nombre_directorio

# Windows (CMD)
rmdir /s nombre_directorio

# Windows (PowerShell)
Remove-Item -Recurse nombre_directorio

# Git (directorio completo)
git rm -r nombre_directorio
git commit -m "Eliminar directorio nombre_directorio"
```

## ⚠️ Notas Importantes

1. **No instalar en clase**: Las dependencias están documentadas pero no pre-instaladas
2. **Seguridad**: Nunca comitear `.env` — siempre usar `.env.example` como template
3. **Riesgos legales**: Verificar `robots.txt` y Términos de Servicio antes de scrapear
4. **Rate limiting**: Agregar delays entre requests para no sobrecargar servidores

## 📝 Licencia

Este proyecto está disponible para uso educativo.

---

**Última actualización**: 15 de noviembre de 2025
