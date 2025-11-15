# Dependencias del Proyecto - founders25-scraper

## Resumen
Este documento describe todas las dependencias requeridas para ejecutar **founders25-scraper**, un web scraper desarrollado en Python. Las versiones sugeridas están optimizadas para estabilidad y compatibilidad.

---

## Dependencias Principales

### 1. **requests** — Librería HTTP
- **Versión sugerida**: `2.31.0` (última estable)
- **Función**: Realizar peticiones HTTP GET/POST a sitios web
- **Instalación**: `pip install requests==2.31.0`
- **Riesgos**:
  - ⚠️ Versiones antiguas (<2.25.0) tienen vulnerabilidades de seguridad en SSL/TLS
  - ⚠️ Si el servidor rechaza peticiones, puede ser necesario agregar headers (`User-Agent`, etc.)
  - ⚠️ Timeouts predeterminados pueden causar cuelgues; siempre usar `timeout=10`
- **Uso típico**:
  ```python
  import requests
  response = requests.get('https://ejemplo.com', timeout=10)
  ```

---

### 2. **beautifulsoup4** — Parser HTML/XML
- **Versión sugerida**: `4.12.2` (última estable)
- **Función**: Parsear y extraer datos de HTML/XML
- **Instalación**: `pip install beautifulsoup4==4.12.2`
- **Dependencias indirectas**: 
  - Requiere un parser (ver sección 3: `lxml`)
- **Riesgos**:
  - ⚠️ Sin parser especificado, usa `html.parser` de Python (lento)
  - ⚠️ Cambios en la estructura HTML del sitio rompen selectores CSS
  - ⚠️ Selektores muy específicos son frágiles; mejor usar clases genéricas
- **Uso típico**:
  ```python
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(html, 'lxml')
  datos = soup.find_all('div', class_='item')
  ```

---

### 3. **lxml** — Parser HTML/XML (alto rendimiento)
- **Versión sugerida**: `4.9.3` (última estable)
- **Función**: Parser rápido y eficiente para BeautifulSoup
- **Instalación**: `pip install lxml==4.9.3`
- **Riesgos**:
  - ⚠️ Requiere compilar código C; necesita compilador (`gcc` en Linux, Visual C++ en Windows)
  - ⚠️ En Windows, si falla la instalación, usar: `pip install lxml --only-binary :all:`
  - ⚠️ Vulnerable a ataques XXE (XML External Entity); usar con cuidado en inputs no validados
  - ⚠️ Más pesado en memoria que `html.parser`
- **Ventajas**: 10x más rápido que `html.parser`
- **Uso recomendado**:
  ```python
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(html, 'lxml')  # Especificar 'lxml' como parser
  ```

---

### 4. **pandas** — Análisis y exportación de datos
- **Versión sugerida**: `2.1.3` (última estable)
- **Función**: Organizar datos en DataFrames y exportar a CSV, Excel, JSON
- **Instalación**: `pip install pandas==2.1.3`
- **Riesgos**:
  - ⚠️ Muy pesado en memoria; con datasets > 100k filas, considerar chunking
  - ⚠️ Si exportas a Excel sin límite, puede corrupciones (máx ~1M filas por hoja)
  - ⚠️ Encoding problemas con caracteres especiales (ñ, acentos); usar `encoding='utf-8'`
  - ⚠️ Depende de NumPy; asegúrate de versiones compatibles
- **Uso típico**:
  ```python
  import pandas as pd
  df = pd.DataFrame(datos)
  df.to_csv('salida.csv', index=False, encoding='utf-8')
  df.to_excel('salida.xlsx', sheet_name='Datos')
  ```

---

### 5. **python-dotenv** — Gestión de variables de entorno
- **Versión sugerida**: `1.0.0` (última estable)
- **Función**: Cargar variables de entorno desde archivo `.env`
- **Instalación**: `pip install python-dotenv==1.0.0`
- **¿Cuándo usar?**
  - Si el scraper usa credenciales (API keys, contraseñas, tokens)
  - Si necesitas diferentes configuraciones por entorno (dev, prod)
  - Para no exponer secretos en el código
- **Riesgos**:
  - ⚠️ El archivo `.env` **NUNCA** debe estar en Git (agregar a `.gitignore`)
  - ⚠️ Si se filtra `.env`, todos tus secretos están comprometidos
  - ⚠️ Solo carga al iniciarse; cambios en `.env` requieren reiniciar la app
- **Uso típico**:
  ```python
  from dotenv import load_dotenv
  import os
  
  load_dotenv()  # Cargar desde .env
  api_key = os.getenv('API_KEY')
  ```
- **Ejemplo `.env`**:
  ```
  API_KEY=tu_clave_secreta_aqui
  PROXY=http://proxy.empresa.com:8080
  DEBUG=True
  ```

---

## Requisitos del Sistema

### Python
- **Versión mínima**: Python 3.8+
- **Versión recomendada**: Python 3.11+ (mejor rendimiento)
- **Verificar**: `python --version`

### Entorno Virtual (recomendado)
Siempre usar un entorno virtual para aislar dependencias:
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar todas las dependencias
pip install -r requirements.txt
```

---

## Archivo `requirements.txt`

Crear archivo `requirements.txt` en la raíz del proyecto:

```
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
pandas==2.1.3
python-dotenv==1.0.0
```

**Instalar todas**: `pip install -r requirements.txt`

---

## Riesgos Generales de Web Scraping

### 1. **Legal**
- ⚠️ Algunos sitios prohíben scraping en su ToS (Términos de Servicio)
- ⚠️ Respetar `robots.txt` y limitar frecuencia de requests
- ⚠️ No agredir servidores con rate-limiting

### 2. **Técnico**
- ⚠️ Cambios en HTML rompen selectores (usar tests automatizados)
- ⚠️ Protecciones: captchas, CloudFlare, headers de User-Agent
- ⚠️ IP baneada si haces requests demasiado rápido

### 3. **De Datos**
- ⚠️ Datos incompletos o inconsistentes
- ⚠️ Validar y limpiar datos antes de usar
- ⚠️ Caracteres especiales pueden causar encoding issues

---

## Recomendaciones de Instalación

### Instalación sin interacción (automatizada)
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Si alguna librería falla
1. Limpiar caché: `pip cache purge`
2. Reinstalar: `pip install --force-reinstall --no-cache-dir requests==2.31.0`
3. En Windows con `lxml`: `pip install lxml --only-binary :all:`

### Verificar instalación
```python
# Ejecutar script de verificación
import requests, bs4, lxml, pandas, dotenv
print("✅ Todas las dependencias están instaladas correctamente")
```

---

## Versionado y Seguridad

- **Versiones pinned** (`==2.31.0`): Garantizan reproducibilidad
- **Actualizaciones**: Revisar mensualmente cambios en dependencias
- **Vulnerabilidades**: Usar `pip-audit` para detectar issues de seguridad
  ```bash
  pip install pip-audit
  pip-audit
  ```

---

## Próximos Pasos

1. Crear `requirements.txt` en la raíz del proyecto
2. Documentar estructura del scraper en `DOCS/arquitectura.md`
3. Crear ejemplos de uso en `examples/`
4. Agregar tests en `tests/`

---

**Última actualización**: 15 de noviembre de 2025
**Autor**: Equipo de Desarrollo
