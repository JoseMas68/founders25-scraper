"""
Rate Limiter para controlar la velocidad de requests
"""

import time
import random
from collections import deque
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, max_requests=30, time_window=60, base_delay=2):
        self.max_requests = max_requests
        self.time_window = time_window  # segundos
        self.base_delay = base_delay    # segundos mínimos entre requests
        self.requests = deque()
        self.last_request_time = 0
        
    def wait_if_needed(self):
        """Espera si es necesario según el rate limiting"""
        now = time.time()
        
        # Remover requests fuera del ventana de tiempo
        while self.requests and now - self.requests[0] > self.time_window:
            self.requests.popleft()
        
        # Verificar si hemos llegado al límite
        if len(self.requests) >= self.max_requests:
            # Calcular tiempo de espera hasta el primer request de la ventana
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                logger.info(f"Rate limit reached. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
        
        # Delay aleatorio para parecer humano
        delay = self.base_delay + random.uniform(0.5, 1.5)
        time.sleep(delay)
        
        # Agregar request actual
        self.requests.append(now)
        self.last_request_time = now
        
        logger.debug(f"Request allowed at {datetime.now().strftime('%H:%M:%S')}")
    
    def get_time_since_last_request(self):
        """Obtiene tiempo transcurrido desde el último request"""
        if self.last_request_time == 0:
            return float('inf')
        return time.time() - self.last_request_time
    
    def is_courtesy_hours(self):
        """Verifica si estamos en horarios de cortesía (8AM - 6PM GMT)"""
        now_utc = datetime.utcnow()
        hour = now_utc.hour
        
        # Ajustar por timezone si es necesario (GMT+1 para España)
        local_hour = (hour + 1) % 24
        
        return 8 <= local_hour <= 18
    
    def wait_for_courtesy_hours(self):
        """Espera hasta llegar a horarios de cortesía"""
        while not self.is_courtesy_hours():
            current_hour = (datetime.utcnow().hour + 1) % 24
            logger.warning(f"Outside courtesy hours (current: {current_hour}h). Waiting...")
            time.sleep(3600)  # Esperar 1 hora
        logger.info("Courtesy hours reached. Continuing...")
    
    def backoff_strategy(self, attempt, max_retries=3):
        """Estrategia de backoff exponencial con jitter"""
        if attempt >= max_retries:
            return False
        
        # Backoff exponencial
        base_delay = min(2 ** attempt, 60)  # Máximo 60 segundos
        jitter = base_delay * 0.1 * random.random()
        delay = base_delay + jitter
        
        logger.warning(f"Backoff: waiting {delay:.1f}s before retry {attempt + 1}/{max_retries}")
        time.sleep(delay)
        return True


class ScrapingMetrics:
    """Métricas para monitoreo del scraping"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.rate_limit_hits = 0
        self.error_types = {}
        self.current_page = 0
        self.records_extracted = 0
        
    def update_request(self, success=True, error_type=None, rate_limited=False):
        """Actualiza métricas de request"""
        self.total_requests += 1
        
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
            if error_type:
                self.error_types[error_type] = self.error_types.get(error_type, 0) + 1
        
        if rate_limited:
            self.rate_limit_hits += 1
    
    def get_success_rate(self):
        """Calcula tasa de éxito"""
        if self.total_requests == 0:
            return 0
        return (self.successful_requests / self.total_requests) * 100
    
    def get_elapsed_time(self):
        """Tiempo transcurrido en minutos"""
        return (datetime.now() - self.start_time).total_seconds() / 60
    
    def get_requests_per_minute(self):
        """Requests por minuto"""
        elapsed = self.get_elapsed_time()
        if elapsed == 0:
            return 0
        return self.total_requests / elapsed
    
    def generate_status_report(self):
        """Genera reporte de estado"""
        success_rate = self.get_success_rate()
        rpm = self.get_requests_per_minute()
        elapsed = self.get_elapsed_time()
        
        return {
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'success_rate': f"{success_rate:.1f}%",
            'requests_per_minute': f"{rpm:.1f}",
            'rate_limit_hits': self.rate_limit_hits,
            'elapsed_minutes': f"{elapsed:.1f}",
            'records_extracted': self.records_extracted,
            'error_types': self.error_types
        }
    
    def log_status(self):
        """Log del estado actual"""
        report = self.generate_status_report()
        logger.info(f"Status: {report['success_rate']} success, {report['rpm']} req/min, {report['elapsed_minutes']} min elapsed")


# Instancia global de métricas
metrics = ScrapingMetrics()

# Instancia global de rate limiter
rate_limiter = RateLimiter(
    max_requests=30,
    time_window=60,
    base_delay=2
)