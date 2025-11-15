"""
Validación de robots.txt y términos de servicio
"""

import requests
import time
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class RobotsChecker:
    """Validador de robots.txt y ToS"""
    
    def __init__(self, user_agent="founders25-research/1.0"):
        self.user_agent = user_agent
        self.cache = {}
    
    def check_robots_txt(self, url):
        """Verifica robots.txt para una URL específica"""
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = f"{base_url}/robots.txt"
        
        try:
            logger.info(f"Checking robots.txt: {robots_url}")
            
            response = requests.get(
                robots_url,
                timeout=10,
                headers={'User-Agent': self.user_agent}
            )
            
            if response.status_code == 200:
                robots_content = response.text
                is_allowed = self.is_url_allowed(robots_content, url, self.user_agent)
                
                return {
                    'allowed': is_allowed,
                    'robots_url': robots_url,
                    'crawl_delay': self.get_crawl_delay(robots_content, self.user_agent),
                    'disallow_paths': self.get_disallow_paths(robots_content, self.user_agent),
                    'raw_content': robots_content
                }
            else:
                logger.warning(f"robots.txt not accessible: {response.status_code}")
                return {
                    'allowed': True,  # Asumir permitido si no hay robots.txt
                    'robots_url': robots_url,
                    'crawl_delay': None,
                    'disallow_paths': [],
                    'status_code': response.status_code
                }
                
        except requests.RequestException as e:
            logger.error(f"Error checking robots.txt: {e}")
            return {
                'allowed': True,  # Ser permisivo en caso de error
                'robots_url': robots_url,
                'crawl_delay': None,
                'disallow_paths': [],
                'error': str(e)
            }
    
    def is_url_allowed(self, robots_content, test_url, user_agent):
        """Verifica si una URL está permitida según robots.txt"""
        parsed_url = urlparse(test_url)
        path = parsed_url.path
        
        # Buscar reglas específicas para el user-agent
        lines = robots_content.split('\n')
        current_ua_rules = []
        generic_rules = []
        in_specific_ua_block = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Detectar inicio de bloque de User-Agent específico
            if line.lower().startswith('user-agent:'):
                ua = line.split(':', 1)[1].strip()
                if ua == '*' or ua.lower() == user_agent.lower():
                    in_specific_ua_block = True
                elif in_specific_ua_block:
                    # Hemos salido del bloque específico
                    in_specific_ua_block = False
                continue
            
            # Determinar en qué reglas estamos
            if in_specific_ua_block:
                current_ua_rules.append(line)
            else:
                generic_rules.append(line)
        
        # Priorizar reglas específicas sobre genéricas
        all_rules = current_ua_rules + generic_rules
        
        # Procesar reglas
        for rule in all_rules:
            if rule.lower().startswith('disallow:'):
                disallow_path = rule.split(':', 1)[1].strip()
                if disallow_path == '':
                    return True  # Disallow vacío = permitir todo
                if path.startswith(disallow_path):
                    return False
            
            elif rule.lower().startswith('allow:'):
                allow_path = rule.split(':', 1)[1].strip()
                if allow_path == '':
                    continue
                if path.startswith(allow_path):
                    return True
        
        return True  # Por defecto, permitido
    
    def get_crawl_delay(self, robots_content, user_agent):
        """Obtiene delay de crawling del robots.txt"""
        lines = robots_content.split('\n')
        crawl_delay = None
        
        for line in lines:
            line = line.strip()
            if line.lower().startswith('crawl-delay:'):
                delay_str = line.split(':', 1)[1].strip()
                try:
                    crawl_delay = float(delay_str)
                except ValueError:
                    pass
            elif line.lower().startswith('user-agent:'):
                ua = line.split(':', 1)[1].strip()
                if ua != '*' and ua.lower() != user_agent.lower():
                    break  # Reglas específicas para otros UAs
        
        return crawl_delay
    
    def get_disallow_paths(self, robots_content, user_agent):
        """Obtiene paths disallow del robots.txt"""
        lines = robots_content.split('\n')
        disallow_paths = []
        
        for line in lines:
            line = line.strip()
            if line.lower().startswith('disallow:'):
                path = line.split(':', 1)[1].strip()
                if path:
                    disallow_paths.append(path)
        
        return disallow_paths
    
    def check_tos_simple(self, url):
        """Verificación simple de términos de servicio"""
        common_tos_paths = ['/terms', '/legal', '/privacy', '/tos', '/terms-of-service']
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Buscar enlaces a ToS en la página principal
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={'User-Agent': self.user_agent}
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Buscar enlaces comunes a ToS
                tos_links = []
                for path in common_tos_paths:
                    link = soup.find('a', href=re.compile(path, re.I))
                    if link:
                        href = link.get('href')
                        full_url = urljoin(base_url, href)
                        tos_links.append(full_url)
                
                return {
                    'has_tos_links': len(tos_links) > 0,
                    'tos_links': tos_links,
                    'page_title': soup.title.string if soup.title else 'No title',
                    'status_code': response.status_code
                }
            
        except requests.RequestException as e:
            logger.error(f"Error checking ToS: {e}")
            return {
                'has_tos_links': False,
                'tos_links': [],
                'error': str(e)
            }
    
    def comprehensive_check(self, url):
        """Verificación completa de robots.txt y ToS"""
        logger.info(f"Comprehensive check for: {url}")
        
        robots_result = self.check_robots_txt(url)
        tos_result = self.check_tos_simple(url)
        
        comprehensive_result = {
            'url': url,
            'timestamp': time.time(),
            'robots_txt': robots_result,
            'terms_of_service': tos_result,
            'overall_allowed': robots_result.get('allowed', True),
            'recommended_delay': robots_result.get('crawl_delay', 2),
            'warnings': []
        }
        
        # Generar advertencias
        if not comprehensive_result['overall_allowed']:
            comprehensive_result['warnings'].append("Scraping not allowed by robots.txt")
        
        if not tos_result.get('has_tos_links'):
            comprehensive_result['warnings'].append("No obvious terms of service links found")
        
        crawl_delay = robots_result.get('crawl_delay')
        if crawl_delay and crawl_delay > 5:
            comprehensive_result['warnings'].append(f"High crawl delay: {crawl_delay}s")
        
        return comprehensive_result


# Instancia global
robots_checker = RobotsChecker()

# Funciones de conveniencia
def check_site_compliance(url):
    """Función simple para verificar compliance de un sitio"""
    return robots_checker.comprehensive_check(url)

def is_site_scrapable(url):
    """Verifica si un sitio es scrapeable según robots.txt"""
    result = check_site_compliance(url)
    return result['overall_allowed']

def get_recommended_delay(url):
    """Obtiene delay recomendado para un sitio"""
    result = check_site_compliance(url)
    return result['recommended_delay']


if __name__ == "__main__":
    # Ejemplo de uso
    test_urls = [
        "https://www.crunchbase.com",
        "https://angel.co",
        "https://www.producthunt.com"
    ]
    
    for url in test_urls:
        print(f"\n=== Checking {url} ===")
        result = check_site_compliance(url)
        
        print(f"Allowed: {result['overall_allowed']}")
        print(f"Recommended delay: {result['recommended_delay']}s")
        print(f"Warnings: {result['warnings']}")
        
        if result['robots_txt'].get('disallow_paths'):
            print(f"Disallow paths: {result['robots_txt']['disallow_paths']}")
        
        print("-" * 50)