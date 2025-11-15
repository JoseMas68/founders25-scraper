"""
Configuración principal del scraper
"""

import os
from datetime import datetime

# === CONFIGURACIÓN GENERAL ===
PROJECT_NAME = "founders25-scraper"
VERSION = "1.0.0"

# === RATE LIMITING ===
RATE_LIMIT_CONFIG = {
    'DELAY_BETWEEN_REQUESTS': 2,  # segundos
    'MAX_REQUESTS_PER_MINUTE': 30,
    'BATCH_SIZE': 10,
    'BATCH_DELAY': 60,
    'MAX_RETRIES': 3,
    'BACKOFF_MULTIPLIER': 2
}

# === USER AGENT ===
USER_AGENT = "founders25-research/1.0 (+https://universidad.edu/research; contact: research@universidad.edu)"

HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# === URLs BASE ===
BASE_URLS = {
    'crunchbase': 'https://www.crunchbase.com',
    'angellist': 'https://angel.co',
    'producthunt': 'https://www.producthunt.com',
    'github': 'https://github.com'
}

# === TIMEOUTS ===
TIMEOUT_CONFIG = {
    'request_timeout': 10,
    'read_timeout': 30,
    'total_timeout': 60
}

# === DIRECTORIOS ===
DATA_DIR = "data"
LOGS_DIR = "logs"
CACHE_DIR = "cache"
EXPORTS_DIR = "exports"

# Crear directorios si no existen
for directory in [DATA_DIR, LOGS_DIR, CACHE_DIR, EXPORTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# === CONFIGURACIÓN DE EXPORTACIÓN ===
EXPORT_CONFIG = {
    'json': {
        'filename': f'{EXPORTS_DIR}/companies_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
        'compression': 'gzip',
        'ensure_ascii': False,
        'indent': 2
    },
    'csv': {
        'filename': f'{EXPORTS_DIR}/companies_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        'encoding': 'utf-8',
        'sep': ',',
        'index': False
    }
}

# === VALIDACIÓN DE ROBOTS.TXT ===
ROBOTS_CHECK = {
    'enabled': True,
    'user_agent': USER_AGENT,
    'timeout': 10
}