"""
Módulo principal de scraping
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
import hashlib
import re

from config import HEADERS, TIMEOUT_CONFIG, BASE_URLS
from rate_limiter import rate_limiter, metrics
from robots_checker import is_site_scrapable, get_recommended_delay

logger = logging.getLogger(__name__)

class DataExtractor:
    """Extractor base de datos"""
    
    def __init__(self, source_name):
        self.source_name = source_name
        self.base_url = BASE_URLS.get(source_name)
        
    def generate_id(self, data):
        """Genera ID único para un registro"""
        timestamp = int(time.time() * 1000)  # milliseconds
        identifier = f"{self.source_name}_{timestamp}"
        
        # Si tenemos nombre y website, agregar hash
        if data.get('name') and data.get('website'):
            hash_input = f"{data['name']}_{data['website']}"
            hash_suffix = hashlib.md5(hash_input.encode()).hexdigest()[:8]
            identifier = f"{self.source_name}_{timestamp}_{hash_suffix}"
        
        return identifier
    
    def extract_basic_data(self, soup, url):
        """Extrae datos básicos del HTML"""
        return {
            'id': None,  # Se genera después
            'name': '',
            'website': '',
            'description': '',
            'source': self.source_name,
            'scraped_at': datetime.utcnow().isoformat() + 'Z',
            'source_url': url
        }
    
    def validate_data(self, data):
        """Valida datos extraídos"""
        if not data.get('name') or not data.get('website'):
            return False, "Missing required fields"
        
        # Validar URL
        if not data['website'].startswith(('http://', 'https://')):
            return False, "Invalid URL format"
        
        return True, "Valid"


class CrunchbaseExtractor(DataExtractor):
    """Extractor específico para Crunchbase"""
    
    def __init__(self):
        super().__init__('crunchbase')
        self.selectors = {
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
            ]
        }
    
    def extract_data(self, soup, url):
        """Extrae datos específicos de Crunchbase"""
        data = self.extract_basic_data(soup, url)
        
        # Nombre de la empresa
        data['name'] = self.extract_with_selectors(soup, self.selectors['company_name'])
        
        # Website
        website = self.extract_with_selectors(soup, self.selectors['website'])
        if website and not website.startswith('http'):
            website = f"https://{website}"
        data['website'] = website
        
        # Descripción
        data['description'] = self.extract_with_selectors(soup, self.selectors['description'])
        
        # Generar ID único
        data['id'] = self.generate_id(data)
        
        return data
    
    def extract_with_selectors(self, soup, selectors):
        """Intenta múltiples selectores hasta encontrar datos"""
        for selector in selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    # Tomar el primer elemento no vacío
                    for element in elements:
                        text = element.get_text(strip=True)
                        if text:
                            return text
            except Exception as e:
                logger.debug(f"Selector failed: {selector} - {e}")
                continue
        return ""


class AngelListExtractor(DataExtractor):
    """Extractor específico para AngelList"""
    
    def __init__(self):
        super().__init__('angellist')
        self.selectors = {
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
            ]
        }
    
    def extract_data(self, soup, url):
        """Extrae datos específicos de AngelList"""
        data = self.extract_basic_data(soup, url)
        
        # Nombre de la empresa
        data['name'] = self.extract_with_selectors(soup, self.selectors['company_name'])
        
        # Website
        website = self.extract_with_selectors(soup, self.selectors['website'])
        if website and not website.startswith('http'):
            website = f"https://{website}"
        data['website'] = website
        
        # Tagline como descripción
        tagline = self.extract_with_selectors(soup, self.selectors['tagline'])
        data['description'] = tagline
        
        # Generar ID único
        data['id'] = self.generate_id(data)
        
        return data
    
    def extract_with_selectors(self, soup, selectors):
        """Intenta múltiples selectores hasta encontrar datos"""
        for selector in selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        text = element.get_text(strip=True)
                        if text:
                            return text
            except Exception as e:
                logger.debug(f"Selector failed: {selector} - {e}")
                continue
        return ""


class ProductHuntExtractor(DataExtractor):
    """Extractor específico para Product Hunt"""
    
    def __init__(self):
        super().__init__('producthunt')
        self.selectors = {
            'product_name': [
                'h1[class*="name"]',
                '.product-title',
                '.item-title'
            ],
            'website': [
                '.website-link',
                'a[href^="http"]',
                '.product-link'
            ],
            'tagline': [
                '.tagline',
                '.product-tagline',
                '.summary'
            ]
        }
    
    def extract_data(self, soup, url):
        """Extrae datos específicos de Product Hunt"""
        data = self.extract_basic_data(soup, url)
        
        # Nombre del producto
        data['name'] = self.extract_with_selectors(soup, self.selectors['product_name'])
        
        # Website
        website = self.extract_with_selectors(soup, self.selectors['website'])
        if website and not website.startswith('http'):
            website = f"https://{website}"
        data['website'] = website
        
        # Tagline como descripción
        tagline = self.extract_with_selectors(soup, self.selectors['tagline'])
        data['description'] = tagline
        
        # Generar ID único
        data['id'] = self.generate_id(data)
        
        return data
    
    def extract_with_selectors(self, soup, selectors):
        """Intenta múltiples selectores hasta encontrar datos"""
        for selector in selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        text = element.get_text(strip=True)
                        if text:
                            return text
            except Exception as e:
                logger.debug(f"Selector failed: {selector} - {e}")
                continue
        return ""


class Scraper:
    """Scraper principal"""
    
    def __init__(self):
        self.extractors = {
            'crunchbase': CrunchbaseExtractor(),
            'angellist': AngelListExtractor(),
            'producthunt': ProductHuntExtractor()
        }
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def scrape_url(self, url, max_retries=3):
        """Scrapea una URL específica"""
        logger.info(f"Starting scrape: {url}")
        
        # Verificar compliance
        if not is_site_scrapable(url):
            raise ValueError(f"Scraping not allowed for {url}")
        
        # Aplicar delay recomendado
        recommended_delay = get_recommended_delay(url)
        if recommended_delay > 2:
            logger.info(f"Using recommended delay: {recommended_delay}s")
            time.sleep(recommended_delay)
        
        # Rate limiting
        rate_limiter.wait_if_needed()
        
        # Hacer request
        for attempt in range(max_retries):
            try:
                logger.debug(f"Request attempt {attempt + 1}/{max_retries}")
                
                response = self.session.get(
                    url,
                    timeout=TIMEOUT_CONFIG['request_timeout']
                )
                
                # Verificar status code
                if response.status_code == 200:
                    metrics.update_request(success=True)
                    return self.parse_response(response, url)
                
                elif response.status_code == 429:
                    # Rate limited
                    metrics.update_request(success=False, rate_limited=True)
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after}s")
                    time.sleep(retry_after)
                
                else:
                    metrics.update_request(success=False)
                    logger.warning(f"HTTP {response.status_code}: {url}")
                
            except requests.RequestException as e:
                metrics.update_request(success=False, error_type=type(e).__name__)
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                
                if attempt < max_retries - 1:
                    if rate_limiter.backoff_strategy(attempt, max_retries):
                        continue
                
                raise Exception(f"Failed after {max_retries} attempts: {e}")
        
        raise Exception(f"Max retries reached for {url}")
    
    def parse_response(self, response, url):
        """Parsea la respuesta HTTP"""
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Determinar extractor basado en el dominio
        extractor = self.get_extractor_for_url(url)
        if not extractor:
            raise ValueError(f"No extractor found for URL: {url}")
        
        # Extraer datos
        data = extractor.extract_data(soup, url)
        
        # Validar datos
        is_valid, message = extractor.validate_data(data)
        if not is_valid:
            logger.warning(f"Data validation failed: {message}")
        
        metrics.records_extracted += 1
        logger.info(f"Extracted data: {data.get('name', 'Unknown')} from {data.get('source', 'Unknown')}")
        
        return data
    
    def get_extractor_for_url(self, url):
        """Determina qué extractor usar para una URL"""
        domain = urlparse(url).netloc.lower()
        
        if 'crunchbase' in domain:
            return self.extractors['crunchbase']
        elif 'angel.co' in domain:
            return self.extractors['angellist']
        elif 'producthunt' in domain:
            return self.extractors['producthunt']
        
        return None
    
    def scrape_multiple_urls(self, urls):
        """Scrapea múltiples URLs"""
        results = []
        errors = []
        
        logger.info(f"Starting batch scrape of {len(urls)} URLs")
        
        for i, url in enumerate(urls, 1):
            try:
                logger.info(f"Processing {i}/{len(urls)}: {url}")
                data = self.scrape_url(url)
                results.append(data)
                
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")
                errors.append({
                    'url': url,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        logger.info(f"Batch complete: {len(results)} successful, {len(errors)} errors")
        
        return results, errors


# Instancia global del scraper
scraper = Scraper()

# Funciones de conveniencia
def scrape_company(url):
    """Función simple para scrapeer una empresa"""
    return scraper.scrape_url(url)

def scrape_multiple_companies(urls):
    """Función simple para scrapeer múltiples empresas"""
    return scraper.scrape_multiple_urls(urls)


if __name__ == "__main__":
    # Ejemplo de uso
    test_urls = [
        "https://www.crunchbase.com/organization/airbnb",
        "https://angel.co/company/airbnb", 
        "https://www.producthunt.com/products/airbnb"
    ]
    
    print("🕷️ Starting test scraping...")
    results, errors = scrape_multiple_companies(test_urls)
    
    print(f"\n✅ Results: {len(results)}")
    print(f"❌ Errors: {len(errors)}")
    
    for result in results:
        print(f"- {result['name']} ({result['source']})")
    
    for error in errors:
        print(f"- ERROR: {error['url']} - {error['error']}")