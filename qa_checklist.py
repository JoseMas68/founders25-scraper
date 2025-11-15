"""
QA Checklist - Validaciones y control de calidad
"""

import json
import logging
from datetime import datetime
from collections import Counter
import re

logger = logging.getLogger(__name__)

def calculate_completeness_score(record):
    """Calcula score de completitud de un registro"""
    if not record:
        return 0.0
    
    # Campos requeridos
    required_fields = ['id', 'name', 'website', 'source', 'scraped_at']
    
    # Campos opcionales importantes
    optional_fields = ['description', 'founded_year', 'location', 'industry']
    
    # Calcular completitud
    required_score = sum(1 for field in required_fields if record.get(field)) / len(required_fields)
    optional_score = sum(1 for field in optional_fields if record.get(field)) / len(optional_fields)
    
    # Ponderación: 70% campos requeridos, 30% opcionales
    return (required_score * 0.7) + (optional_score * 0.3)

def detect_exact_duplicates(records):
    """Detecta duplicados exactos por ID"""
    seen_ids = set()
    duplicates = []
    
    for record in records:
        record_id = record.get('id')
        if record_id in seen_ids:
            duplicates.append(record)
        else:
            seen_ids.add(record_id)
    
    return duplicates

def validate_url(url):
    """Valida formato de URL"""
    if not url:
        return False
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def validate_data(records):
    """Validación básica de datos"""
    validation_results = {
        'total_records': len(records),
        'valid_records': 0,
        'invalid_records': 0,
        'validation_errors': [],
        'completeness_stats': {}
    }
    
    if not records:
        return validation_results
    
    completeness_scores = []
    
    for i, record in enumerate(records):
        errors = []
        
        # Validar campos requeridos
        if not record.get('name'):
            errors.append("Missing name")
        
        if not record.get('website'):
            errors.append("Missing website")
        elif not validate_url(record['website']):
            errors.append("Invalid website URL")
        
        if not record.get('source'):
            errors.append("Missing source")
        
        # Calcular score de completitud
        score = calculate_completeness_score(record)
        completeness_scores.append(score)
        
        if errors:
            validation_results['invalid_records'] += 1
            validation_results['validation_errors'].append({
                'record_index': i,
                'record_id': record.get('id', 'unknown'),
                'errors': errors
            })
        else:
            validation_results['valid_records'] += 1
    
    # Estadísticas de completitud
    if completeness_scores:
        validation_results['completeness_stats'] = {
            'average': sum(completeness_scores) / len(completeness_scores),
            'min': min(completeness_scores),
            'max': max(completeness_scores),
            'records_above_70_percent': sum(1 for score in completeness_scores if score >= 0.7)
        }
    
    return validation_results

def run_qa_pipeline(records, expected_counts=None):
    """Pipeline básico de QA"""
    if not records:
        logger.warning("No records to validate")
        return {}, "# QA Report - No Data\n\nNo records provided for validation."
    
    logger.info(f"Running QA on {len(records)} records")
    
    # 1. Validación de datos
    validation = validate_data(records)
    
    # 2. Detección de duplicados
    duplicates = detect_exact_duplicates(records)
    
    # 3. Generar reporte
    report = f"""# QA Report
**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Registros analizados**: {validation['total_records']}

## Resumen
- **Registros válidos**: {validation['valid_records']}
- **Registros inválidos**: {validation['invalid_records']}
- **Tasa de éxito**: {(validation['valid_records']/validation['total_records']*100):.1f}%
- **Duplicados**: {len(duplicates)}

## Completitud
"""
    
    if validation['completeness_stats']:
        stats = validation['completeness_stats']
        report += f"""- **Score promedio**: {stats['average']:.2%}
- **Score mínimo**: {stats['min']:.2%}
- **Score máximo**: {stats['max']:.2%}
- **Registros >70% completos**: {stats['records_above_70_percent']}
"""
    
    # 4. Errores de validación
    if validation['validation_errors']:
        report += "\n## Errores de Validación\n\n"
        for error in validation['validation_errors'][:10]:  # Primeros 10
            report += f"- **Registro {error['record_index']}** ({error['record_id']}): {', '.join(error['errors'])}\n"
        
        if len(validation['validation_errors']) > 10:
            report += f"- ... y {len(validation['validation_errors']) - 10} errores más\n"
    
    # 5. Duplicados
    if duplicates:
        report += f"\n## Duplicados ({len(duplicates)})\n\n"
        for dup in duplicates[:5]:  # Primeros 5
            report += f"- {dup.get('name', 'Unknown')} ({dup.get('id', 'Unknown')})\n"
        
        if len(duplicates) > 5:
            report += f"- ... y {len(duplicates) - 5} duplicados más\n"
    
    # Resultados detallados
    qa_results = {
        'validation': validation,
        'duplicates': duplicates,
        'timestamp': datetime.now().isoformat()
    }
    
    return qa_results, report

def save_qa_report(qa_results, report, filename=None):
    """Guarda reporte de QA"""
    if filename is None:
        filename = f"logs/qa_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    # Guardar reporte markdown
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Guardar resultados JSON
    json_filename = filename.replace('.md', '.json')
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(qa_results, f, indent=2, default=str)
    
    logger.info(f"QA report saved: {filename}")
    logger.info(f"QA results saved: {json_filename}")
    
    return filename, json_filename