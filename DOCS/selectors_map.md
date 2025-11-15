# Mapa de Selectores CSS - Extracción de Datos

## Objetivo del Documento
Este documento define los selectores CSS específicos para extraer datos de cada sitio web objetivo. Incluye selectores principales, alternativas de respaldo, y notas sobre fragilidad de cada selector.

---

## Tabla de Selectores por Sitio

### 1. **Crunchbase** - Perfiles de Startups

| Campo | Selector Principal | Selector Fallback | Fragilidad | Notas |
|-------|-------------------|-------------------|------------|-------|
| **Company Name** | `h1[class*="profile"]` | `.profile-header h1` | 🟡 Media | Cambió en 2024 |
| **Website** | `a[href*="website"]` | `[data-test="company-website"]` | 🟢 Baja | Muy estable |
| **Description** | `.description` | `.about-company` | 🟡 Media | Puede estar truncado |
| **Founded** | `.founded` | `.established-date` | 🟢 Baja | Formato consistente |
| **Location** | `.location` | `[data-test="company-location"]` | 🟡 Media | Puede ser múltiple |
| **Industry** | `.categories` | `.industries` | 🟡 Media | Múltiples valores |
| **Funding Rounds** | `.funding-rounds` | `.investment-rounds` | 🔴 Alta | Muy dinámico |
| **Employees** | `.employee-count` | `.company-size` | 🟡 Media | Estimado |
| **Logo URL** | `img[class*="logo"]` | `.company-logo img` | 🟢 Baja | Muy estable |

```python
# Selectores Crunchbase
CRUNCHBASE_SELECTORS = {
    'company_name': [
        'h1[class*="profile"]',
        '.profile-header h1',
        'h1.company-name'
    ],
    'website': [
        'a[href*="website"]',
        '[data-test="company-website"]',
        '.company-link a'
    ],
    'description': [
        '.description',
        '.about-company',
        '.company-summary'
    ],
    'founded': [
        '.founded',
        '.established-date',
        'span:contains("Founded")'
    ],
    'location': [
        '.location',
        '[data-test="company-location"]',
        '.headquarters'
    ],
    'industry': [
        '.categories',
        '.industries',
        '.sectors'
    ],
    'funding_rounds': [
        '.funding-rounds',
        '.investment-rounds',
        '.funding-info'
    ],
    'employees': [
        '.employee-count',
        '.company-size',
        '.team-size'
    ],
    'logo_url': [
        'img[class*="logo"]',
        '.company-logo img',
        '.profile-logo img'
    ]
}
```

### 2. **AngelList** - Perfiles de Startups

| Campo | Selector Principal | Selector Fallback | Fragilidad | Notas |
|-------|-------------------|-------------------|------------|-------|
| **Company Name** | `.startup-name` | `h1[class*="name"]` | 🟢 Baja | Muy estable |
| **Website** | `.company-url` | `a[href^="http"]` | 🟢 Baja | Excelente estabilidad |
| **Tagline** | `.tagline` | `.company-tagline` | 🟡 Media | No siempre presente |
| **Company Size** | `.company-size` | `.team-size` | 🟡 Media | Rangos vs números |
| **Founded Year** | `.founded` | `.established-year` | 🟢 Baja | Formato numérico |
| **Location** | `.location` | `.hq-location` | 🟡 Media | Puede ser múltiple |
| **Market** | `.market` | `.industry` | 🟡 Media | Múltiples valores |
| **Investors** | `.investors` | `.backers` | 🔴 Alta | Acceso limitado |
| **Jobs** | `.jobs` | `.open-positions` | 🟡 Media | Filtrado activo |

```python
# Selectores AngelList
ANGELLIST_SELECTORS = {
    'company_name': [
        '.startup-name',
        'h1[class*="name"]',
        '.profile-title'
    ],
    'website': [
        '.company-url',
        'a[href^="http"]',
        '.website-link'
    ],
    'tagline': [
        '.tagline',
        '.company-tagline',
        '.profile-tagline'
    ],
    'company_size': [
        '.company-size',
        '.team-size',
        '.employees'
    ],
    'founded_year': [
        '.founded',
        '.established-year',
        'span:contains("Founded")'
    ],
    'location': [
        '.location',
        '.hq-location',
        '.office-location'
    ],
    'market': [
        '.market',
        '.industry',
        '.sector'
    ],
    'investors': [
        '.investors',
        '.backers',
        '.funding-sources'
    ],
    'jobs': [
        '.jobs',
        '.open-positions',
        '.hiring'
    ]
}
```

### 3. **Product Hunt** - Catálogo de Productos

| Campo | Selector Principal | Selector Fallback | Fragilidad | Notas |
|-------|-------------------|-------------------|------------|-------|
| **Product Name** | `h1[class*="name"]` | `.product-title` | 🟢 Baja | Muy estable |
| **Tagline** | `.tagline` | `.product-tagline` | 🟡 Media | Puede estar vacío |
| **Website** | `.website-link` | `a[href^="http"]` | 🟢 Baja | Excelente |
| **Description** | `.description` | `.product-description` | 🟡 Media | HTML formatting |
| **Category** | `.category` | `.product-category` | 🟡 Media | Taxonomía cambiante |
| **Votes** | `.votes-count` | `.upvotes` | 🟡 Media | Puede ser "Today" |
| **Maker** | `.maker-name` | `.creator-name` | 🟡 Media | Múltiples makers |
| **Launch Date** | `.launch-date` | `.published-date` | 🟢 Baja | Formato ISO |
| **Screenshots** | `.screenshots` | `.product-images` | 🟡 Media | Carrusel dinámico |

```python
# Selectores Product Hunt
PRODUCTHUNT_SELECTORS = {
    'product_name': [
        'h1[class*="name"]',
        '.product-title',
        '.item-title'
    ],
    'tagline': [
        '.tagline',
        '.product-tagline',
        '.summary'
    ],
    'website': [
        '.website-link',
        'a[href^="http"]',
        '.product-link'
    ],
    'description': [
        '.description',
        '.product-description',
        '.content'
    ],
    'category': [
        '.category',
        '.product-category',
        '.topic'
    ],
    'votes': [
        '.votes-count',
        '.upvotes',
        '.score'
    ],
    'maker': [
        '.maker-name',
        '.creator-name',
        '.submitted-by'
    ],
    'launch_date': [
        '.launch-date',
        '.published-date',
        '.created-date'
    ],
    'screenshots': [
        '.screenshots',
        '.product-images',
        '.gallery img'
    ]
}
```

### 4. **GitHub Trending** - Repositorios Populares

| Campo | Selector Principal | Selector Fallback | Fragilidad | Notas |
|-------|-------------------|-------------------|------------|-------|
| **Repo Name** | `h2 a` | `.repo-name` | 🟢 Baja | Muy estable |
| **Description** | `.repo-description` | `p` | 🟡 Media | Puede estar vacío |
| **Language** | `[itemprop="programmingLanguage"]` | `.language` | 🟢 Baja | Códigos ISO |
| **Stars** | `.stargazers` | `.star-count` | 🟢 Baja | Números formateados |
| **Forks** | `.forks` | `.fork-count` | 🟢 Baja | Menos confiable |
| **Today Stars** | `.stars-today` | `span:contains("stars today")` | 🟡 Media | Solo trending diario |
| **Owner** | `.owner` | `.username` | 🟢 Baja | Formato @usuario |
| **URL** | `h2 a[href]` | `.repo-link` | 🟢 Baja | Siempre presente |
| **Topics** | `.topics` | `.repository-topics` | 🟡 Media | Variable length |

```python
# Selectores GitHub Trending
GITHUB_SELECTORS = {
    'repo_name': [
        'h2 a',
        '.repo-name',
        '.repo-title a'
    ],
    'description': [
        '.repo-description',
        'p.description',
        '.item-description'
    ],
    'language': [
        '[itemprop="programmingLanguage"]',
        '.language',
        '.repo-language'
    ],
    'stars': [
        '.stargazers',
        '.star-count',
        '.stars'
    ],
    'forks': [
        '.forks',
        '.fork-count',
        '.forks-count'
    ],
    'today_stars': [
        '.stars-today',
        'span:contains("stars today")',
        '.daily-stars'
    ],
    'owner': [
        '.owner',
        '.username',
        '.author'
    ],
    'url': [
        'h2 a[href]',
        '.repo-link',
        '.repository-link'
    ],
    'topics': [
        '.topics',
        '.repository-topics',
        '.tags'
    ]
}
```

---

## Notas de Fragilidad por Sitio

### 🔴 **Alto Riesgo** (Revisar Semanalmente)
- **Crunchbase Funding**: Estructura cambia frecuentemente
- **AngelList Investors**: Acceso restringido, captchas
- **Product Hunt Screenshots**: Carrusel dinámico, lazy loading

### 🟡 **Riesgo Medio** (Revisar Mensualmente)
- **Todos los Taglines**: No siempre presentes
- **Descriptions**: HTML formatting inconsistente
- **Categories/Industries**: Taxonomías cambiante
- **Employee Counts**: Estimaciones vs datos reales

### 🟢 **Bajo Riesgo** (Revisar Trimestralmente)
- **Names y Websites**: Muy estables
- **Founded Dates**: Formato consistente
- **Languages**: Estándares técnicos
- **Basic URLs**: Estructura fija

---

## Pruebas Manuales y Validación

### Script de Prueba de Selectores
```python
import requests
from bs4 import BeautifulSoup
import time

def test_selector_stability():
    """Prueba la estabilidad de selectores en sitios conocidos"""
    
    test_sites = {
        'crunchbase': 'https://www.crunchbase.com/organization/airbnb',
        'angellist': 'https://angel.co/company/airbnb',
        'producthunt': 'https://www.producthunt.com/products/airbnb',
        'github': 'https://github.com/trending'
    }
    
    results = {}
    
    for site, url in test_sites.items():
        print(f"\n🧪 Probando selectores de {site}...")
        
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Test Bot'})
            soup = BeautifulSoup(response.content, 'lxml')
            
            site_selectors = globals()[f"{site.upper()}_SELECTORS"]
            site_results = {}
            
            for field, selectors in site_selectors.items():
                found = False
                for selector in selectors:
                    try:
                        elements = soup.select(selector)
                        if elements:
                            site_results[field] = {
                                'status': 'found',
                                'selector': selector,
                                'count': len(elements),
                                'preview': elements[0].get_text(strip=True)[:50]
                            }
                            found = True
                            break
                    except Exception as e:
                        continue
                
                if not found:
                    site_results[field] = {
                        'status': 'not_found',
                        'selectors_tested': selectors
                    }
            
            results[site] = site_results
            
        except Exception as e:
            print(f"❌ Error probando {site}: {e}")
            results[site] = {'error': str(e)}
        
        time.sleep(2)  # Rate limiting
    
    return results

def generate_selector_report(results):
    """Genera reporte de estabilidad de selectores"""
    
    report = "# Reporte de Estabilidad de Selectores\n\n"
    report += f"**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for site, data in results.items():
        report += f"## {site.title()}\n\n"
        
        if 'error' in data:
            report += f"❌ **Error**: {data['error']}\n\n"
            continue
        
        for field, result in data.items():
            if result['status'] == 'found':
                report += f"✅ **{field}**: `{result['selector']}` ({result['count']} elementos)\n"
                report += f"   *Ejemplo*: {result['preview']}...\n\n"
            else:
                report += f"❌ **{field}**: No encontrado\n"
                report += f"   *Probados*: {result['selectors_tested']}\n\n"
    
    return report

# Ejecutar pruebas
if __name__ == "__main__":
    print("🚀 Iniciando pruebas de selectores...")
    results = test_selector_stability()
    report = generate_selector_report(results)
    
    # Guardar reporte
    with open('docs/selector_test_report.md', 'w') as f:
        f.write(report)
    
    print("✅ Pruebas completadas. Ver reporte en docs/selector_test_report.md")
```

### Checklist de Validación Manual

#### **Al Iniciar Testing**
- [ ] Verificar acceso al sitio objetivo
- [ ] Confirmar que no hay captchas activos
- [ ] Validar estructura básica de la página

#### **Para Cada Campo**
- [ ] ✅ Selector principal funciona
- [ ] ✅ Selector fallback funciona
- [ ] ✅ Datos extraídos son coherentes
- [ ] ✅ No hay false positives
- [ ] ✅ Performance es aceptable (<100ms)

#### **Reporte de Issues**
```markdown
## Issue: [Descripción breve]

**Sitio**: [crunchbase|angellist|producthunt|github]
**Campo**: [nombre del campo]
**Selector usado**: [CSS selector]
**Error**: [descripción del problema]
**Impacto**: [alta|media|baja]
**Solución propuesta**: [nuevo selector o estrategia]
```

---

## Estrategias de Fallback

### 1. **Fallback Secuencial**
```python
def extract_with_fallback(soup, selectors, field_name):
    """Intenta múltiples selectores hasta encontrar datos"""
    
    for i, selector in enumerate(selectors):
        try:
            elements = soup.select(selector)
            if elements:
                value = extract_value_from_elements(elements)
                if value:
                    logger.debug(f"✅ {field_name} extraído con selector {i}: {selector}")
                    return value
        except Exception as e:
            logger.warning(f"⚠️ Error con selector {i} para {field_name}: {e}")
            continue
    
    logger.warning(f"❌ No se pudo extraer {field_name} con ningún selector")
    return None

def extract_value_from_elements(elements):
    """Extrae valor limpio de elementos HTML"""
    
    if len(elements) == 1:
        # Campo único
        element = elements[0]
        
        # Diferentes tipos de extracción
        if element.name == 'a':
            return element.get('href') or element.get_text(strip=True)
        elif element.name == 'img':
            return element.get('src') or element.get('alt', '')
        else:
            return element.get_text(strip=True)
    
    else:
        # Múltiples valores (tags, categorías, etc.)
        return [elem.get_text(strip=True) for elem in elements]
```

### 2. **Extracción por Tipo de Datos**
```python
# URLs
def extract_url(element):
    return element.get('href') if element.name == 'a' else element.get_text(strip=True)

# Fechas
def extract_date(element):
    text = element.get_text(strip=True)
    # Parsear diferentes formatos
    date_formats = ['%Y-%m-%d', '%B %Y', '%Y']
    for fmt in date_formats:
        try:
            return datetime.strptime(text, fmt).isoformat()
        except ValueError:
            continue
    return text  # Devolver como string si no se puede parsear

# Números
def extract_number(element):
    text = element.get_text(strip=True)
    # Remover separadores de miles, "k", "m", etc.
    import re
    number = re.sub(r'[^\d.]', '', text)
    try:
        return float(number)
    except ValueError:
        return text

# Texto multilínea
def extract_multiline(element):
    return ' '.join(element.get_text(strip=True).split())
```

### 3. **Validación Post-Extracción**
```python
def validate_extracted_data(field_name, value, site):
    """Valida que los datos extraídos sean coherentes"""
    
    validation_rules = {
        'url': lambda x: x.startswith(('http://', 'https://')) if x else False,
        'email': lambda x: '@' in x if x else False,
        'founded_year': lambda x: 1990 <= int(x) <= 2025 if x and x.isdigit() else False,
        'company_name': lambda x: len(x) >= 2 and len(x) <= 100 if x else False,
        'description': lambda x: len(x) >= 10 if x else False
    }
    
    if field_name in validation_rules:
        is_valid = validation_rules[field_name](value)
        if not is_valid:
            logger.warning(f"⚠️ Datos inválidos para {field_name}: {value}")
            return False
    
    return True
```

---

## Mantenimiento y Actualizaciones

### **Frecuencia de Revisión**
- **Selectores críticos**: Semanal
- **Selectores secundarios**: Mensual  
- **Selectores estables**: Trimestral

### **Monitoreo Automático**
```python
# Cron job para detectar cambios en sitios
def monitor_selector_health():
    """Monitorea salud de selectores y alerta sobre cambios"""
    
    daily_stats = {
        'sites_checked': 0,
        'selectors_working': 0,
        'selectors_broken': 0,
        'new_selectors_needed': 0
    }
    
    # Ejecutar pruebas automáticas
    # Generar alertas si hay cambios significativos
    # Actualizar automáticamente selectores si es posible
```

### **Proceso de Actualización**
1. **Detección**: Alertas automáticas de fallos de selectores
2. **Análisis**: Revisar cambios en estructura HTML
3. **Actualización**: Modificar selectores en `selectors_map.md`
4. **Pruebas**: Validar nuevos selectores
5. **Deploy**: Actualizar en producción

---

**Última actualización**: 15 de noviembre de 2025
**Responsable**: Equipo de Desarrollo