# Estrategia de Paginación - Navegación y Checkpoints

## Objetivo del Documento
Esta guía define las estrategias de paginación para navegar a través de múltiples páginas de contenido en cada sitio web objetivo, incluyendo detección de fin de datos, checkpoints y retry logic.

---

## Tipos de Paginación por Sitio

### 1. **Crunchbase** - Paginación Numérica

#### Patrón de URLs
```
Página 1: https://www.crunchbase.com/organizations
Página 2: https://www.crunchbase.com/organizations?page=2
Página 3: https://www.crunchbase.com/organizations?page=3
```

#### Señales de Fin de Datos
```python
def detect_end_crunchbase(soup):
    """Detecta si hemos llegado al final de resultados en Crunchbase"""
    
    # Señal 1: Botón "Next" deshabilitado o ausente
    next_button = soup.select('.pagination-next, [aria-label="Next"]')
    if next_button and 'disabled' in next_button[0].get('class', []):
        return True
    
    # Señal 2: Mensaje "No more results"
    no_more = soup.find(text=re.compile(r'no more results|no results found', re.I))
    if no_more:
        return True
    
    # Señal 3: Lista de resultados vacía
    results = soup.select('.organization-listing, .results-list')
    if results and len(results) == 0:
        return True
    
    return False
```

#### Estimación de Registros
```python
def estimate_crunchbase_records():
    """Estima el número total de registros en Crunchbase"""
    
    # Páginas conocidas por exploración previa
    estimates = {
        'organizations': 500000,  # Aproximadamente
        'people': 300000,
        'funding_rounds': 150000
    }
    
    return estimates
```

### 2. **AngelList** - Infinite Scroll + Load More

#### Patrón de Carga
```
Base URL: https://angel.co/companies
Carga inicial: 50 empresas
Carga adicional: ~20-30 empresas por "Load More"
```

#### Detección de Fin de Datos
```python
def detect_end_angellist(soup, previous_count):
    """Detecta fin de datos en AngelList (infinite scroll)"""
    
    # Señal 1: No hay botón "Load More"
    load_more = soup.select('.load-more, .show-more, [data-test="load-more"]')
    if not load_more:
        return True
    
    # Señal 2: El botón dice "No more results" o similar
    button_text = load_more[0].get_text(strip=True).lower()
    if any(phrase in button_text for phrase in ['no more', 'end of results', 'all loaded']):
        return True
    
    # Señal 3: Conteo de elementos no aumentó
    current_companies = soup.select('.company-listing, .startup')
    if len(current_companies) <= previous_count:
        return True
    
    return False
```

#### Implementación de Infinite Scroll
```python
def scrape_infinite_scroll(url, max_pages=100):
    """Maneja scraping con infinite scroll"""
    
    session = requests.Session()
    companies = []
    page = 1
    
    while page <= max_pages:
        # Determinar URL de la página
        if page == 1:
            current_url = url
        else:
            current_url = f"{url}?page={page}"
        
        try:
            response = session.get(current_url, timeout=10)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extraer empresas de la página
            company_elements = soup.select('.company-listing, .startup')
            if not company_elements:
                break
            
            page_companies = extract_companies_from_page(company_elements)
            companies.extend(page_companies)
            
            # Verificar si hemos terminado
            if detect_end_angellist(soup, len(companies)):
                logger.info(f"Infinite scroll ended at page {page}")
                break
            
            page += 1
            time.sleep(random.uniform(2, 4))  # Rate limiting
            
        except Exception as e:
            logger.error(f"Error in page {page}: {e}")
            break
    
    return companies
```

### 3. **Product Hunt** - Paginación Temporal

#### Patrón de URLs
```
Página 1: https://www.producthunt.com/posts?page=1
Página 2: https://www.producthunt.com/posts?page=2
Posts por página: ~30-50
```

#### Detección de Fin de Datos
```python
def detect_end_producthunt(soup):
    """Detecta fin de datos en Product Hunt"""
    
    # Señal 1: Página sin productos
    posts = soup.select('.post-listing, .product-item')
    if not posts:
        return True
    
    # Señal 2: Productos son muy antiguos (más de 30 días)
    for post in posts:
        date_element = post.select('.posted-date, [datetime]')
        if date_element:
            date_text = date_element[0].get('datetime') or date_element[0].get_text(strip=True)
            try:
                post_date = parse_date(date_text)
                if (datetime.now() - post_date).days > 365:  # Más de 1 año
                    return True
            except:
                continue
    
    # Señal 3: Link "Next" ausente o deshabilitado
    next_link = soup.select('a[rel="next"], .next-page')
    if not next_link:
        return True
    
    return False
```

### 4. **GitHub Trending** - Paginación por Período

#### Patrón de URLs
```
Diario: https://github.com/trending?since=daily
Semanal: https://github.com/trending?since=weekly
Mensual: https://github.com/trending?since=monthly
```

#### Detección de Fin de Datos
```python
def detect_end_github(soup):
    """Detecta fin de datos en GitHub Trending"""
    
    # GitHub Trending no tiene paginación tradicional
    # Se considera "fin" cuando se han procesado todos los períodos
    
    repositories = soup.select('li[data-repo]')
    if not repositories:
        return True
    
    # Verificar si los repos son duplicados o muy antiguos
    repo_names = [repo.get('data-repo') for repo in repositories]
    if len(set(repo_names)) < len(repo_names) * 0.8:  # Muchos duplicados
        return True
    
    return False
```

---

## Checkpoint y Resume Logic

### Sistema de Checkpoint
```python
import json
import os
from datetime import datetime
from pathlib import Path

class PaginationCheckpoint:
    def __init__(self, site_name, source_type='pagination'):
        self.site_name = site_name
        self.source_type = source_type
        self.checkpoint_dir = Path("logs/checkpoints")
        self.checkpoint_dir.mkdir(exist_ok=True)
        
        self.checkpoint_file = self.checkpoint_dir / f"{site_name}_{source_type}.json"
    
    def save_checkpoint(self, current_state):
        """Guarda estado actual del scraping"""
        
        checkpoint_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'site': self.site_name,
            'source_type': self.source_type,
            'current_page': current_state.get('current_page', 1),
            'processed_urls': current_state.get('processed_urls', []),
            'extracted_records': current_state.get('extracted_records', 0),
            'last_successful_page': current_state.get('current_page', 1),
            'pagination_state': current_state.get('pagination_state', {}),
            'error_count': current_state.get('error_count', 0)
        }
        
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
        
        logger.info(f"Checkpoint saved: {checkpoint_data}")
    
    def load_checkpoint(self):
        """Carga último estado guardado"""
        
        if not self.checkpoint_file.exists():
            return None
        
        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
            
            logger.info(f"Checkpoint loaded: {checkpoint_data['timestamp']}")
            return checkpoint_data
        
        except Exception as e:
            logger.error(f"Error loading checkpoint: {e}")
            return None
    
    def clear_checkpoint(self):
        """Limpia checkpoint después de completado exitoso"""
        
        if self.checkpoint_file.exists():
            os.remove(self.checkpoint_file)
            logger.info("Checkpoint cleared")
```

### Implementación de Resume
```python
def resume_scraping_with_checkpoint(site_config):
    """Reanuda scraping desde último checkpoint"""
    
    checkpoint_manager = PaginationCheckpoint(site_config['name'])
    checkpoint = checkpoint_manager.load_checkpoint()
    
    if not checkpoint:
        logger.info("No checkpoint found, starting fresh")
        return start_fresh_scraping(site_config)
    
    logger.info(f"Resuming from page {checkpoint['current_page']}")
    
    # Verificar antigüedad del checkpoint (max 24h)
    checkpoint_time = datetime.fromisoformat(checkpoint['timestamp'])
    if (datetime.utcnow() - checkpoint_time).total_seconds() > 86400:  # 24 hours
        logger.warning("Checkpoint too old, starting fresh")
        return start_fresh_scraping(site_config)
    
    # Continuar desde donde se dejó
    pagination_type = site_config.get('pagination_type', 'numbered')
    
    if pagination_type == 'numbered':
        return resume_numbered_pagination(site_config, checkpoint)
    elif pagination_type == 'infinite_scroll':
        return resume_infinite_scroll(site_config, checkpoint)
    elif pagination_type == 'time_based':
        return resume_time_based(site_config, checkpoint)
    
    return start_fresh_scraping(site_config)
```

### Resume por Tipo de Paginación

#### **Paginación Numerada (Crunchbase)**
```python
def resume_numbered_pagination(site_config, checkpoint):
    """Reanuda scraping con paginación numerada"""
    
    start_page = checkpoint['current_page'] + 1
    max_pages = site_config.get('max_pages', 100)
    
    logger.info(f"Resuming numbered pagination from page {start_page}")
    
    for page_num in range(start_page, max_pages + 1):
        try:
            # Construir URL con página
            page_url = f"{site_config['base_url']}?page={page_num}"
            
            # Hacer request
            response = requests.get(page_url, timeout=10)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Verificar si hemos terminado
            if detect_end_crunchbase(soup):
                logger.info(f"Pagination ended at page {page_num}")
                break
            
            # Extraer datos
            page_data = extract_data_from_page(soup, site_config)
            
            # Guardar progreso
            current_state = {
                'current_page': page_num,
                'extracted_records': len(page_data),
                'pagination_state': {'page': page_num}
            }
            checkpoint_manager.save_checkpoint(current_state)
            
            # Rate limiting
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            logger.error(f"Error in page {page_num}: {e}")
            checkpoint['error_count'] += 1
            
            if checkpoint['error_count'] >= 5:
                logger.error("Too many errors, stopping")
                break
            
            time.sleep(10)  # Backoff en errores
```

#### **Infinite Scroll (AngelList)**
```python
def resume_infinite_scroll(site_config, checkpoint):
    """Reanuda scraping con infinite scroll"""
    
    start_offset = checkpoint.get('current_offset', 0)
    companies_per_load = 30
    
    logger.info(f"Resuming infinite scroll from offset {start_offset}")
    
    # Simular scroll hasta llegar al offset deseado
    session = requests.Session()
    all_companies = []
    current_offset = 0
    
    while current_offset < start_offset:
        # Hacer request con offset
        scroll_url = f"{site_config['base_url']}?offset={current_offset}"
        response = session.get(scroll_url, timeout=10)
        
        if response.status_code != 200:
            break
        
        # Procesar respuesta y avanzar offset
        companies = extract_companies_from_response(response.json())
        current_offset += len(companies)
        
        time.sleep(2)
    
    # Continuar desde offset actual
    while current_offset < site_config.get('max_offset', 10000):
        scroll_url = f"{site_config['base_url']}?offset={current_offset}"
        response = session.get(scroll_url, timeout=10)
        
        if response.status_code != 200:
            break
        
        page_companies = extract_companies_from_response(response.json())
        if not page_companies:
            break
        
        all_companies.extend(page_companies)
        
        # Guardar checkpoint
        checkpoint_manager.save_checkpoint({
            'current_offset': current_offset,
            'extracted_records': len(all_companies)
        })
        
        current_offset += len(page_companies)
        time.sleep(random.uniform(2, 4))
    
    return all_companies
```

---

## Estimación de Registros y Tiempo

### Cálculos por Sitio

#### **Crunchbase**
```python
def estimate_crunchbase_metrics():
    """Estima métricas para Crunchbase"""
    
    estimates = {
        'total_organizations': 500000,
        'organizations_per_page': 20,
        'estimated_pages': 25000,
        'avg_time_per_page': 3,  # segundos
        'total_estimated_time_hours': (25000 * 3) / 3600  # ~20.8 horas
    }
    
    return estimates
```

#### **AngelList**
```python
def estimate_angellist_metrics():
    """Estima métricas para AngelList"""
    
    estimates = {
        'total_companies': 200000,
        'companies_per_load': 30,
        'estimated_loads': 6667,
        'avg_time_per_load': 4,  # segundos
        'total_estimated_time_hours': (6667 * 4) / 3600  # ~7.4 horas
    }
    
    return estimates
```

#### **Product Hunt**
```python
def estimate_producthunt_metrics():
    """Estima métricas para Product Hunt"""
    
    estimates = {
        'total_posts': 100000,
        'posts_per_page': 30,
        'estimated_pages': 3334,
        'avg_time_per_page': 2,  # segundos
        'total_estimated_time_hours': (3334 * 2) / 3600  # ~1.9 horas
    }
    
    return estimates
```

### Progresión Temporal
```python
def calculate_scraping_timeline():
    """Calcula timeline completo de scraping"""
    
    sites = ['crunchbase', 'angellist', 'producthunt']
    total_time = 0
    
    timeline = {
        'phases': [],
        'total_estimated_hours': 0,
        'bottlenecks': []
    }
    
    for site in sites:
        estimates = globals()[f'estimate_{site}_metrics']()
        
        phase = {
            'site': site,
            'estimated_hours': estimates['total_estimated_time_hours'],
            'records': estimates[f'total_{site[:-1] if site.endswith("base") else site}s'.replace('_', '')],
            'start_time': None,
            'end_time': None,
            'status': 'pending'
        }
        
        total_time += estimates['total_estimated_time_hours']
        timeline['phases'].append(phase)
    
    timeline['total_estimated_hours'] = total_time
    
    # Identificar bottlenecks
    slowest_phase = max(timeline['phases'], key=lambda x: x['estimated_hours'])
    timeline['bottlenecks'].append({
        'site': slowest_phase['site'],
        'reason': f"Highest time: {slowest_phase['estimated_hours']:.1f} hours",
        'suggestion': 'Consider parallel processing or rate limit reduction'
    })
    
    return timeline
```

### Dashboard de Progreso
```python
class ScrapingProgress:
    def __init__(self, site_name):
        self.site_name = site_name
        self.start_time = datetime.now()
        self.pages_processed = 0
        self.records_extracted = 0
        self.errors_count = 0
        
    def update_progress(self, pages_delta=0, records_delta=0):
        """Actualiza progreso actual"""
        self.pages_processed += pages_delta
        self.records_extracted += records_delta
        
    def calculate_eta(self, remaining_pages, avg_time_per_page):
        """Calcula tiempo estimado de finalización"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        if self.pages_processed > 0:
            current_avg = elapsed / self.pages_processed
            remaining_seconds = remaining_pages * current_avg
            eta = datetime.now() + timedelta(seconds=remaining_seconds)
            
            return {
                'eta': eta,
                'remaining_hours': remaining_seconds / 3600,
                'progress_percentage': (self.pages_processed / (self.pages_processed + remaining_pages)) * 100
            }
        
        return None
    
    def generate_status_report(self):
        """Genera reporte de estado actual"""
        elapsed = (datetime.now() - self.start_time).total_seconds() / 3600  # hours
        
        return {
            'site': self.site_name,
            'elapsed_hours': round(elapsed, 2),
            'pages_processed': self.pages_processed,
            'records_extracted': self.records_extracted,
            'errors_count': self.errors_count,
            'records_per_hour': round(self.records_extracted / elapsed, 2) if elapsed > 0 else 0
        }
```

---

## Estrategias de Retry

### Retry Logic por Tipo de Error
```python
def handle_pagination_retry(url, attempt, max_retries, pagination_type):
    """Maneja reintentos basados en tipo de paginación"""
    
    if attempt >= max_retries:
        logger.error(f"Max retries reached for {url}")
        return False
    
    # Errores transitorios
    if attempt < max_retries // 2:
        if pagination_type == 'numbered':
            # Para paginación numerada, intentar diferentes estrategias
            if '?page=' not in url:
                # Agregar parámetro de página
                url = url + '?page=1'
            else:
                # Cambiar página
                import re
                page_match = re.search(r'page=(\d+)', url)
                if page_match:
                    current_page = int(page_match.group(1))
                    url = re.sub(r'page=\d+', f'page={current_page + 1}', url)
        else:
            # Para infinite scroll, cambiar offset
            if 'offset=' in url:
                offset_match = re.search(r'offset=(\d+)', url)
                if offset_match:
                    current_offset = int(offset_match.group(1))
                    url = re.sub(r'offset=\d+', f'offset={current_offset + 30}', url)
    
    # Backoff exponencial con jitter
    delay = min(2 ** attempt, 60) + random.uniform(0, 1)
    time.sleep(delay)
    
    logger.warning(f"Retrying {url} (attempt {attempt + 1}/{max_retries})")
    return url
```

### Verificación de Integridad Post-Resume
```python
def verify_data_integrity_after_resume(site_config, resumed_data):
    """Verifica que los datos extraídos después del resume sean válidos"""
    
    integrity_checks = {
        'duplicate_check': len(resumed_data) == len(set(str(record) for record in resumed_data)),
        'schema_check': all(isinstance(record, dict) for record in resumed_data),
        'required_fields_check': all(
            all(field in record for field in site_config.get('required_fields', []))
            for record in resumed_data
        ),
        'quality_check': sum(1 for record in resumed_data if record.get('name')) / len(resumed_data) > 0.8
    }
    
    passed_checks = sum(integrity_checks.values())
    total_checks = len(integrity_checks)
    
    logger.info(f"Integrity checks: {passed_checks}/{total_checks} passed")
    
    if passed_checks < total_checks * 0.7:  # Menos del 70% exitoso
        logger.error("Data integrity compromised after resume")
        return False
    
    return True
```

---

## Configuración de Producción

### Variables de Entorno para Paginación
```bash
# Archivo .env
PAGINATION_MAX_RETRIES=3
PAGINATION_CHECKPOINT_INTERVAL=10
PAGINATION_RATE_LIMIT_DELAY=2
PAGINATION_MAX_PAGES_PER_RUN=1000
PAGINATION_TIMEOUT_SECONDS=30
PAGINATION_RESUME_ENABLED=true
```

### Configuración en Código
```python
# config/pagination.py
PAGINATION_CONFIG = {
    'max_retries': int(os.getenv('PAGINATION_MAX_RETRIES', 3)),
    'checkpoint_interval': int(os.getenv('PAGINATION_CHECKPOINT_INTERVAL', 10)),
    'rate_limit_delay': float(os.getenv('PAGINATION_RATE_LIMIT_DELAY', 2.0)),
    'max_pages_per_run': int(os.getenv('PAGINATION_MAX_PAGES_PER_RUN', 1000)),
    'timeout_seconds': int(os.getenv('PAGINATION_TIMEOUT_SECONDS', 30)),
    'resume_enabled': os.getenv('PAGINATION_RESUME_ENABLED', 'true').lower() == 'true',
    
    'sites': {
        'crunchbase': {
            'pagination_type': 'numbered',
            'items_per_page': 20,
            'max_pages': 10000
        },
        'angellist': {
            'pagination_type': 'infinite_scroll',
            'items_per_load': 30,
            'max_loads': 1000
        },
        'producthunt': {
            'pagination_type': 'numbered',
            'items_per_page': 30,
            'max_pages': 5000
        }
    }
}
```

---

**Última actualización**: 15 de noviembre de 2025
**Responsable**: Equipo de Desarrollo