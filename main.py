#!/usr/bin/env python3
"""
Script principal del scraper founders25
Uso: python main.py [comando] [opciones]
"""

import argparse
import logging
import sys
import json
import os
from datetime import datetime

# Importar módulos del scraper
from config import PROJECT_NAME, VERSION, EXPORT_CONFIG
from scraper import scraper, scrape_company, scrape_multiple_companies
from rate_limiter import metrics, rate_limiter
from robots_checker import check_site_compliance
from qa_checklist import run_qa_pipeline

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)-8s %(name)-30s %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'logs/scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

logger = logging.getLogger(__name__)

def setup_directories():
    """Crea los directorios necesarios"""
    directories = ['data', 'logs', 'cache', 'exports']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    logger.info("Directories setup complete")

def test_scraper():
    """Prueba básica del scraper con URLs conocidas"""
    print("\n🧪 TESTING SCRAPER")
    print("=" * 50)
    
    test_urls = [
        "https://www.crunchbase.com/organization/airbnb",
        "https://angel.co/company/airbnb",
        "https://www.producthunt.com/products/airbnb"
    ]
    
    print(f"Testing with {len(test_urls)} URLs...")
    print("This may take a few minutes due to rate limiting.\n")
    
    try:
        results, errors = scrape_multiple_companies(test_urls)
        
        print(f"\n📊 RESULTS:")
        print(f"✅ Successful: {len(results)}")
        print(f"❌ Errors: {len(errors)}")
        print(f"📈 Success rate: {len(results)/(len(results)+len(errors))*100:.1f}%")
        
        if results:
            print(f"\n📋 EXTRACTED DATA:")
            for result in results:
                print(f"• {result['name']} ({result['source']})")
                print(f"  Website: {result['website']}")
                print(f"  Description: {result['description'][:100]}...")
                print()
        
        if errors:
            print(f"\n❌ ERRORS:")
            for error in errors:
                print(f"• {error['url']}: {error['error']}")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def scrape_single(url):
    """Scrapea una URL individual"""
    print(f"\n🕷️ SCRAPING SINGLE URL")
    print("=" * 50)
    
    try:
        print(f"URL: {url}")
        print("Checking compliance...")
        
        # Verificar compliance
        compliance = check_site_compliance(url)
        print(f"✅ Allowed: {compliance['overall_allowed']}")
        print(f"⏱️ Recommended delay: {compliance['recommended_delay']}s")
        
        if not compliance['overall_allowed']:
            print("❌ Scraping not allowed by robots.txt")
            return False
        
        if compliance['warnings']:
            print("⚠️ Warnings:")
            for warning in compliance['warnings']:
                print(f"  - {warning}")
        
        print("\nStarting scrape...")
        result = scrape_company(url)
        
        print(f"\n✅ SUCCESS!")
        print(f"Name: {result['name']}")
        print(f"Website: {result['website']}")
        print(f"Source: {result['source']}")
        print(f"Description: {result['description'][:200]}...")
        
        # Guardar resultado
        filename = f"data/single_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved to: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def scrape_batch(urls_file):
    """Scrapea múltiples URLs desde un archivo"""
    print(f"\n📦 BATCH SCRAPING")
    print("=" * 50)
    
    # Leer URLs del archivo
    try:
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"Loaded {len(urls)} URLs from {urls_file}")
        
        if len(urls) == 0:
            print("❌ No URLs found")
            return False
        
        # Mostrar primera URL como ejemplo
        print(f"Example URL: {urls[0]}")
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Confirmar antes de continuar
    print(f"\n⚠️ This will scrape {len(urls)} URLs")
    print("This may take several minutes/hours depending on rate limiting.")
    response = input("Continue? (y/N): ")
    
    if response.lower() != 'y':
        print("Cancelled")
        return False
    
    try:
        print("\n🚀 Starting batch scrape...")
        results, errors = scrape_multiple_companies(urls)
        
        # Generar reporte
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Guardar resultados
        results_file = f"exports/batch_results_{timestamp}.json"
        errors_file = f"exports/batch_errors_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        with open(errors_file, 'w', encoding='utf-8') as f:
            json.dump(errors, f, indent=2, ensure_ascii=False)
        
        # Mostrar resumen
        print(f"\n📊 BATCH COMPLETE!")
        print(f"✅ Successful: {len(results)}")
        print(f"❌ Errors: {len(errors)}")
        print(f"📈 Success rate: {len(results)/(len(results)+len(errors))*100:.1f}%")
        
        # QA básico
        if results:
            print(f"\n🔍 QUALITY CHECK:")
            unique_names = len(set(r['name'] for r in results))
            print(f"• Unique companies: {unique_names}/{len(results)}")
            
            with_website = len([r for r in results if r['website']])
            print(f"• With website: {with_website}/{len(results)} ({with_website/len(results)*100:.1f}%)")
        
        print(f"\n💾 Results saved:")
        print(f"  📄 Success: {results_file}")
        print(f"  📄 Errors: {errors_file}")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"❌ Batch failed: {e}")
        return False

def show_status():
    """Muestra el estado actual del scraper"""
    print(f"\n📊 SCRAPER STATUS")
    print("=" * 50)
    
    report = metrics.generate_status_report()
    
    print(f"📈 Performance:")
    for key, value in report.items():
        if key != 'error_types':
            print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n🕐 Courtesy Hours Check:")
    is_courtesy = rate_limiter.is_courtesy_hours()
    print(f"  • Current status: {'✅ Active hours' if is_courtesy else '⏸️ Off hours'}")
    
    if not is_courtesy:
        print(f"  • Waiting until 8:00 AM GMT+1...")
        # rate_limiter.wait_for_courtesy_hours()

def create_sample_urls():
    """Crea un archivo de ejemplo con URLs"""
    sample_urls = [
        "# URLs de ejemplo para batch scraping",
        "# Formato: una URL por línea",
        "# Las líneas que empiecen con # son comentarios",
        "",
        "https://www.crunchbase.com/organization/airbnb",
        "https://angel.co/company/airbnb",
        "https://www.producthunt.com/products/airbnb",
        "",
        "# Agrega más URLs aquí..."
    ]
    
    filename = "data/sample_urls.txt"
    with open(filename, 'w') as f:
        f.write('\n'.join(sample_urls))
    
    print(f"\n📄 Created sample file: {filename}")
    print(f"Edit this file to add your own URLs and run:")
    print(f"  python main.py batch {filename}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description=f"{PROJECT_NAME} v{VERSION} - Web Scraper for Startups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py test                 # Prueba el scraper
  python main.py single <URL>         # Scrapea una URL
  python main.py batch <file>         # Scrapea URLs desde archivo
  python main.py status               # Muestra estado actual
  python main.py sample               # Crea archivo de ejemplo
        """
    )
    
    parser.add_argument('command', choices=['test', 'single', 'batch', 'status', 'sample'],
                       help='Command to execute')
    parser.add_argument('url_or_file', nargs='?', help='URL for single or file for batch')
    parser.add_argument('--version', action='version', version=f'{PROJECT_NAME} {VERSION}')
    
    args = parser.parse_args()
    
    # Setup inicial
    setup_directories()
    print(f"🚀 {PROJECT_NAME} v{VERSION}")
    print("=" * 50)
    
    # Ejecutar comando
    if args.command == 'test':
        return test_scraper()
    
    elif args.command == 'single':
        if not args.url_or_file:
            print("❌ Please provide a URL")
            print("Usage: python main.py single <URL>")
            return False
        
        return scrape_single(args.url_or_file)
    
    elif args.command == 'batch':
        if not args.url_or_file:
            print("❌ Please provide a file with URLs")
            print("Usage: python main.py batch <file>")
            print("Tip: Run 'python main.py sample' to create an example file")
            return False
        
        return scrape_batch(args.url_or_file)
    
    elif args.command == 'status':
        show_status()
        return True
    
    elif args.command == 'sample':
        create_sample_urls()
        return True
    
    else:
        parser.print_help()
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.exception("Fatal error in main")
        sys.exit(1)