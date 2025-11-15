# Onboarding del Scraper - Guía Ética y Técnica

## Objetivo del Documento
Esta guía establece las mejores prácticas éticas, técnicas y legales para el uso responsable del scraper. Todos los desarrolladores deben leer y comprender estos lineamientos antes de ejecutar el scraper.

---

## 🛡️ Alcance Ético

### Principios Fundamentales
- **✅ Respecto**: No dañar ni sobrecargar servidores objetivo
- **✅ Legalidad**: Cumplir robots.txt y términos de servicio
- **✅ Responsabilidad**: Usar datos de manera ética y legal
- **✅ Transparencia**: Documentar el uso del scraper

### Uso Prohibido
- ❌ No scrapear datos personales sin consentimiento explícito
- ❌ No realizar scraping que viole términos de servicio
- ❌ No usar para spam, phishing o actividades maliciosas
- ❌ No comercial re-routing sin autorización
- ❌ No circumventing de medidas de protección técnica

---

## 🤖 Análisis de robots.txt

### Comando para Verificar robots.txt
```bash
# Extraer y analizar robots.txt del sitio objetivo
curl -s https://sitio-objetivo.com/robots.txt | head -20

# O usando Python para análisis automatizado
python -c "
import requests
try:
    r = requests.get('https://sitio-objetivo.com/robots.txt', timeout=10)
    print('Status:', r.status_code)
    if r.status_code == 200:
        print(r.text[:500])  # Primeras 500 líneas
    else:
        print('robots.txt no disponible')
except Exception as e:
    print('Error:', e)
"
```

### Interpretación de Reglas
- **Disallow: /** → No se permite scraping
- **Allow: /public/** → Solo estas rutas son permitidas
- **Crawl-delay: 10** → Esperar 10 segundos entre requests
- **User-agent: *** → Regla aplica a todos los scrapers
- **User-agent: Googlebot** → Regla específica para Google

### Ejemplo de robots.txt Restrictivo
```
User-agent: *
Disallow: /
Disallow: /api/
Disallow: /admin/
Disallow: /private/
Crawl-delay: 30

# URLs permitidas
Allow: /public/
Allow: /docs/
```

---

## 📋 Términos de Servicio (ToS)

### Proceso de Verificación ToS
1. **Localizar ToS**: Buscar en `/terms`, `/legal`, `/privacy`
2. **Buscar Restricciones**: Revisar cláusulas sobre scraping/bots
3. **Verificar Comercial**: ¿Se permite uso comercial?
4. **Contactar si Duda**: Cuando hay ambigüedad, contactar al sitio

### Frases Clave a Buscar
- "web scraping"
- "automated access"
- "data collection"
- "commercial use"
- "robots" o "bots"

### Ejemplo de ToS Problemático
```
"You may not use any automated system or software to extract data from our website without express written permission."
→ ❌ NO PROCEDER sin autorización
```

### Ejemplo de ToS Permisivo
```
"Reasonable automated access for research purposes is permitted, provided you respect our robots.txt file and implement appropriate rate limiting."
→ ✅ PROCEDER con precauciones
```

---

## 🏷️ User-Agent Propuesto

### User-Agent Principal
```python
USER_AGENT = "founders25-research/1.0 (+https://universidad.edu/research; contact: research@universidad.edu)"
```

### Headers Completos Recomendados
```python
HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
```

### Rotación de User-Agents (Avanzado)
```python
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36", 
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)
```

---

## ⏱️ Rate Limits y Control de Velocidad

### Configuración Recomendada
```python
RATE_LIMIT_CONFIG = {
    'DELAY_BETWEEN_REQUESTS': 2,  # segundos
    'MAX_REQUESTS_PER_MINUTE': 30,
    'BATCH_SIZE': 10,  # requests por batch
    'BATCH_DELAY': 60,  # pausa entre batches
    'MAX_RETRIES': 3,
    'BACKOFF_MULTIPLIER': 2
}
```

### Implementación de Rate Limiting
```python
import time
import random
from collections import deque

class RateLimiter:
    def __init__(self, max_requests=30, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def wait_if_needed(self):
        now = time.time()
        
        # Remover requests fuera del ventana de tiempo
        while self.requests and now - self.requests[0] > self.time_window:
            self.requests.popleft()
        
        # Si llegamos al límite, esperar
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Agregar request actual
        self.requests.append(now)
        
        # Delay aleatorio para parecer humano
        time.sleep(random.uniform(1, 3))
```

### Detección de Rate Limiting
```python
def detect_rate_limit(response):
    indicators = [
        response.status_code == 429,  # Too Many Requests
        'rate limit' in response.text.lower(),
        'too many requests' in response.text.lower(),
        'retry-after' in response.headers,
        response.status_code == 503  # Service Unavailable
    ]
    return any(indicators)
```

---

## 🔄 Estrategia de Backoff

### Backoff Lineal
```python
def linear_backoff(attempt, base_delay=1):
    return base_delay * attempt
```

### Backoff Exponencial
```python
def exponential_backoff(attempt, base_delay=1, max_delay=60):
    delay = base_delay * (2 ** (attempt - 1))
    return min(delay, max_delay)
```

### Backoff con Jitter
```python
import random

def backoff_with_jitter(attempt, base_delay=1, max_delay=60):
    base = min(base_delay * (2 ** (attempt - 1)), max_delay)
    jitter = base * 0.1 * random.random()
    return base + jitter
```

### Implementación Completa
```python
def scrape_with_backoff(url, max_retries=3):
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                # Rate limited, aplicar backoff
                wait_time = exponential_backoff(attempt)
                print(f"Rate limited. Esperando {wait_time:.1f}s")
                time.sleep(wait_time)
                continue
            
        except requests.RequestException as e:
            if attempt == max_retries:
                raise
            
            wait_time = backoff_with_jitter(attempt)
            print(f"Error: {e}. Reintentando en {wait_time:.1f}s")
            time.sleep(wait_time)
    
    raise Exception(f"Falló después de {max_retries} intentos")
```

---

## 🕐 Horarios de Cortesía

### Horarios Recomendados
- **✅ Actividad Normal**: 08:00 - 18:00 (GMT)
- **🟡 Actividad Reducida**: 18:00 - 22:00 (GMT)
- **❌ NO Scrapear**: 22:00 - 08:00 (GMT)

### Implementación de Horarios
```python
from datetime import datetime, timezone

def is_courtesy_hours():
    now_utc = datetime.now(timezone.utc)
    hour = now_utc.hour
    
    # Convertir a horario local si es necesario
    # Por ejemplo, GMT+1 (España):
    # hour = (hour + 1) % 24
    
    return 8 <= hour <= 18

def wait_for_courtesy_hours():
    while not is_courtesy_hours():
        print("Fuera de horarios de cortesía. Esperando...")
        time.sleep(3600)  # Esperar 1 hora
```

---

## 📊 Monitoreo de Salud

### Métricas Importantes
```python
SCRAPING_METRICS = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'rate_limit_hits': 0,
    'avg_response_time': 0,
    'error_types': {}
}
```

### Alertas Recomendadas
- 🚨 **Crítico**: >10 errores consecutivos
- ⚠️ **Warning**: >5 rate limits en 10 minutos  
- ✅ **Info**: <95% éxito en último batch

---

## ✅ Checklist Pre-Ejecución

Antes de ejecutar el scraper, verificar:

- [ ] ✅ robots.txt permite el scraping
- [ ] ✅ ToS permite el uso del scraper
- [ ] ✅ Rate limiting configurado (mín. 2s delay)
- [ ] ✅ User-Agent identificable configurado
- [ ] ✅ Backoff strategy implementada
- [ ] ✅ Horarios de cortesía respetados
- [ ] ✅ Logs de monitoreo configurados
- [ ] ✅ Datos de prueba ejecutados exitosamente

---

**Última actualización**: 15 de noviembre de 2025
**Responsable**: Equipo de Desarrollo