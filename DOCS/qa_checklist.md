# QA Checklist - Validaciones y Control de Calidad

## Objetivo del Documento
Este documento define todas las validaciones, controles de calidad y métricas que debe pasar el scraper antes de considerar los datos como válidos para uso en producción.

---

## Checklist Principal de Validación

### ✅ **Duplicados**
- [ ] **Sin registros duplicados por ID único**
- [ ] **Sin empresas duplicadas por nombre + dominio**
- [ ] **Sin URLs duplicadas en el dataset**
- [ ] **Deteción de duplicados por similitud de nombre (>90%)**

### ✅ **Campos Nulos**
- [ ] **Campos requeridos no nulos (name, website, source, id, scraped_at)**
- [ ] **Campos críticos con <15% de nulos (description, founded_year, location)**
- [ ] **Campos opcionales con <50% de nulos (employee_count, funding, valuation)**
- [ ] **Validación de campos estructurados (location.industry arrays)**

### ✅ **Rangos de Valores**
- [ ] **founded_year entre 1990-2025**
- [ ] **employee_count entre 1-1,000,000**
- [ ] **funding_amount >= 0**
- [ ] **coordinates dentro de rangos válidos (-90 a 90, -180 a 180)**
- [ ] **text_length dentro de límites (name: 2-100, description: 0-1000)**

### ✅ **Conteo y Completitud**
- [ ] **Conteo esperado de registros por fuente**
- [ ] **Distribución de datos por fuente balanceada**
- [ ] **Campos por registro dentro de rangos esperados**
- [ ] **Score de completitud promedio >75%**

### ✅ **Codificación y Formato**
- [ ] **Encoding UTF-8 sin errores**
- [ ] **Fechas en formato ISO 8601 válido**
- [ ] **URLs con formato válido (http/https)**
- [ ] **Texto sin caracteres extraños o de control**
- [ ] **CSV/Excel con separadores correctos**

---

## Detección de Duplicados

### Implementación de Deduplicación
```python
import hashlib
from difflib import SequenceMatcher
import re

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

def detect_fuzzy_duplicates(records, threshold=0.9):
    """Detecta duplicados por similitud de nombre + dominio"""
    from fuzzywuzzy import fuzz
    
    duplicates = []
    processed = set()
    
    for i, record1 in enumerate(records):
        if record1['id'] in processed:
            continue
            
        name1 = record1.get('name', '').lower().strip()
        domain1 = extract_domain(record1.get('website', ''))
        
        potential_duplicates = []
        
        for j, record2 in enumerate(records[i+1:], i+1):
            if record2['id'] in processed:
                continue
                
            name2 = record2.get('name', '').lower().strip()
            domain2 = extract_domain(record2.get('website', ''))
            
            # Comparar nombres y dominios
            name_similarity = fuzz.ratio(name1, name2) / 100
            domain_similarity = fuzz.ratio(domain1, domain2) / 100
            
            if name_similarity > threshold or domain_similarity > threshold:
                potential_duplicates.append(record2)
                processed.add(record2['id'])
        
        if potential_duplicates:
            duplicates.append({
                'primary': record1,
                'duplicates': potential_duplicates
            })
            processed.add(record1['id'])
    
    return duplicates

def detect_url_duplicates(records):
    """Detecta duplicados por URL del sitio web"""
    seen_domains = {}
    url_duplicates = []
    
    for record in records:
        website = record.get('website', '')
        domain = extract_domain(website)
        
        if domain in seen_domains:
            url_duplicates.append({
                'domain': domain,
                'record1': seen_domains[domain],
                'record2': record
            })
        else:
            seen_domains[domain] = record
    
    return url_duplicates

def generate_duplicate_report(duplicates):
    """Genera reporte detallado de duplicados"""
    
    report = "# Reporte de Duplicados\n\n"
    
    # Duplicados exactos
    exact_dups = detect_exact_duplicates(all_records)
    if exact_dups:
        report += f"## Duplicados Exactos ({len(exact_dups)})\n\n"
        for dup in exact_dups:
            report += f"- ID: `{dup['id']}` (aparece múltiples veces)\n"
        report += "\n"
    
    # Duplicados por similitud
    fuzzy_dups = detect_fuzzy_duplicates(all_records)
    if fuzzy_dups:
        report += f"## Duplicados por Similitud ({len(fuzzy_dups)})\n\n"
        for dup_group in fuzzy_dups:
            report += f"### Grupo de Similitud\n"
            report += f"- **Principal**: {dup_group['primary']['name']} ({dup_group['primary']['id']})\n"
            for dup in dup_group['duplicates']:
                report += f"- **Duplicado**: {dup['name']} ({dup['id']})\n"
            report += "\n"
    
    # Duplicados por URL
    url_dups = detect_url_duplicates(all_records)
    if url_dups:
        report += f"## Duplicados por URL ({len(url_dups)})\n\n"
        for dup in url_dups:
            report += f"- **Dominio**: {dup['domain']}\n"
            report += f"  - {dup['record1']['name']} ({dup['record1']['id']})\n"
            report += f"  - {dup['record2']['name']} ({dup['record2']['id']})\n"
        report += "\n"
    
    return report
```

---

## Validación de Nulos

### Análisis de Completitud por Campo
```python
def analyze_null_fields(records):
    """Analiza completitud de campos por sitio y globalmente"""
    
    field_stats = {}
    required_fields = ['id', 'name', 'website', 'source', 'scraped_at']
    critical_fields = ['description', 'founded_year', 'location']
    
    # Contar nulos por campo
    for field in required_fields + critical_fields:
        total_count = len(records)
        null_count = sum(1 for r in records if not r.get(field))
        field_stats[field] = {
            'total': total_count,
            'nulls': null_count,
            'null_percentage': (null_count / total_count) * 100,
            'non_null': total_count - null_count
        }
    
    # Análisis por fuente
    sources = {}
    for record in records:
        source = record.get('source', 'unknown')
        if source not in sources:
            sources[source] = []
        sources[source].append(record)
    
    source_stats = {}
    for source, source_records in sources.items():
        source_stats[source] = {}
        for field in required_fields:
            null_count = sum(1 for r in source_records if not r.get(field))
            source_stats[source][field] = {
                'total': len(source_records),
                'null_percentage': (null_count / len(source_records)) * 100
            }
    
    return field_stats, source_stats

def generate_null_report(field_stats, source_stats):
    """Genera reporte de completitud de campos"""
    
    report = "# Reporte de Completitud de Datos\n\n"
    report += f"**Total de registros analizados**: {list(field_stats.values())[0]['total']}\n\n"
    
    # Tabla de campos requeridos
    report += "## Campos Requeridos\n\n"
    report += "| Campo | Completitud | Registros Válidos | Estado |\n"
    report += "|-------|-------------|-------------------|--------|\n"
    
    for field, stats in field_stats.items():
        completeness = 100 - stats['null_percentage']
        status = "✅ OK" if completeness >= 95 else "⚠️ Warning" if completeness >= 85 else "❌ Error"
        report += f"| {field} | {completeness:.1f}% | {stats['non_null']} | {status} |\n"
    
    report += "\n## Análisis por Fuente\n\n"
    
    for source, source_field_stats in source_stats.items():
        report += f"### {source.title()}\n\n"
        report += "| Campo | Completitud | Estado |\n"
        report += "|-------|-------------|--------|\n"
        
        for field, stats in source_field_stats.items():
            completeness = 100 - stats['null_percentage']
            status = "✅ OK" if completeness >= 90 else "⚠️ Warning" if completeness >= 75 else "❌ Error"
            report += f"| {field} | {completeness:.1f}% | {status} |\n"
        report += "\n"
    
    return report
```

---

## Validación de Rangos

### Validaciones Numéricas y de Fecha
```python
import datetime
from datetime import datetime as dt

def validate_ranges(records):
    """Valida rangos de valores para campos numéricos y de fecha"""
    
    validation_results = {
        'errors': [],
        'warnings': [],
        'stats': {}
    }
    
    # Validar founded_year
    current_year = datetime.datetime.now().year
    founded_years = [r.get('founded_year') for r in records if r.get('founded_year')]
    
    if founded_years:
        invalid_years = [year for year in founded_years if year < 1990 or year > current_year]
        if invalid_years:
            validation_results['errors'].append(
                f"founded_year inválido: {len(invalid_years)} registros fuera de rango [1990, {current_year}]"
            )
        
        validation_results['stats']['founded_year'] = {
            'min': min(founded_years),
            'max': max(founded_years),
            'average': sum(founded_years) / len(founded_years),
            'count': len(founded_years)
        }
    
    # Validar employee_count
    employee_counts = [r.get('employee_count') for r in records if r.get('employee_count')]
    
    if employee_counts:
        invalid_counts = [count for count in employee_counts if count < 1 or count > 1000000]
        if invalid_counts:
            validation_results['errors'].append(
                f"employee_count inválido: {len(invalid_counts)} registros fuera de rango [1, 1000000]"
            )
        
        validation_results['stats']['employee_count'] = {
            'min': min(employee_counts),
            'max': max(employee_counts),
            'average': sum(employee_counts) / len(employee_counts),
            'count': len(employee_counts)
        }
    
    # Validar funding amounts
    funding_amounts = []
    for record in records:
        funding = record.get('funding_total')
        if funding and funding.get('amount_usd'):
            amount = funding['amount_usd']
            if amount < 0:
                validation_results['errors'].append(
                    f"Negative funding amount: {amount} for {record.get('name')}"
                )
            else:
                funding_amounts.append(amount)
    
    if funding_amounts:
        validation_results['stats']['funding_amount'] = {
            'min': min(funding_amounts),
            'max': max(funding_amounts),
            'average': sum(funding_amounts) / len(funding_amounts),
            'count': len(funding_amounts)
        }
    
    # Validar coordinates
    coordinates = []
    for record in records:
        location = record.get('location')
        if location and location.get('coordinates'):
            coords = location['coordinates']
            lat = coords.get('latitude')
            lng = coords.get('longitude')
            
            if lat is not None and not (-90 <= lat <= 90):
                validation_results['errors'].append(
                    f"Latitud inválida: {lat} para {record.get('name')}"
                )
            
            if lng is not None and not (-180 <= lng <= 180):
                validation_results['errors'].append(
                    f"Longitud inválida: {lng} para {record.get('name')}"
                )
            
            if lat is not None and lng is not None:
                coordinates.append((lat, lng))
    
    if coordinates:
        lats, lngs = zip(*coordinates)
        validation_results['stats']['coordinates'] = {
            'latitude': {'min': min(lats), 'max': max(lats)},
            'longitude': {'min': min(lngs), 'max': max(lngs)},
            'count': len(coordinates)
        }
    
    # Validar longitud de texto
    name_lengths = [len(r.get('name', '')) for r in records]
    desc_lengths = [len(r.get('description', '')) for r in records if r.get('description')]
    
    invalid_names = [length for length in name_lengths if length < 2 or length > 100]
    if invalid_names:
        validation_results['warnings'].append(
            f"Nombres con longitud inválida: {len(invalid_names)} registros"
        )
    
    invalid_descs = [length for length in desc_lengths if length > 1000]
    if invalid_descs:
        validation_results['warnings'].append(
            f"Descripciones muy largas (>1000 chars): {len(invalid_descs)} registros"
        )
    
    return validation_results

def detect_outliers(values, method='iqr', threshold=1.5):
    """Detecta outliers usando IQR o Z-score"""
    
    if not values or len(values) < 4:
        return []
    
    import numpy as np
    
    values_array = np.array(values)
    
    if method == 'iqr':
        q1 = np.percentile(values_array, 25)
        q3 = np.percentile(values_array, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        
        outliers = values_array[(values_array < lower_bound) | (values_array > upper_bound)]
    
    elif method == 'zscore':
        mean = np.mean(values_array)
        std = np.std(values_array)
        
        z_scores = np.abs((values_array - mean) / std)
        outliers = values_array[z_scores > threshold]
    
    return outliers.tolist()
```

---

## Validación de Conteos

### Análisis de Distribución de Datos
```python
def analyze_data_distribution(records):
    """Analiza distribución de datos por fuente y características"""
    
    distribution_stats = {
        'by_source': {},
        'by_year': {},
        'by_industry': {},
        'by_location': {},
        'completeness': {}
    }
    
    # Distribución por fuente
    sources = {}
    for record in records:
        source = record.get('source', 'unknown')
        if source not in sources:
            sources[source] = 0
        sources[source] += 1
    
    distribution_stats['by_source'] = sources
    
    # Distribución por año de fundación
    founded_years = {}
    for record in records:
        year = record.get('founded_year')
        if year:
            year_str = str(year)
            if year_str not in founded_years:
                founded_years[year_str] = 0
            founded_years[year_str] += 1
    
    distribution_stats['by_year'] = founded_years
    
    # Distribución por industria
    industries = {}
    for record in records:
        industry_list = record.get('industry', [])
        if isinstance(industry_list, list):
            for industry in industry_list:
                industry = industry.strip()
                if industry:
                    if industry not in industries:
                        industries[industry] = 0
                    industries[industry] += 1
    
    distribution_stats['by_industry'] = industries
    
    # Distribución por ubicación
    locations = {}
    for record in records:
        location = record.get('location')
        if location:
            country = location.get('country', 'Unknown')
            if country not in locations:
                locations[country] = 0
            locations[country] += 1
    
    distribution_stats['by_location'] = locations
    
    # Score de completitud promedio
    completeness_scores = []
    for record in records:
        score = calculate_completeness_score(record)
        completeness_scores.append(score)
    
    distribution_stats['completeness'] = {
        'average': sum(completeness_scores) / len(completeness_scores),
        'min': min(completeness_scores),
        'max': max(completeness_scores),
        'median': sorted(completeness_scores)[len(completeness_scores) // 2]
    }
    
    return distribution_stats

def validate_expected_counts(distribution_stats, expected_counts):
    """Valida que los conteos estén dentro de rangos esperados"""
    
    validation_results = {
        'errors': [],
        'warnings': [],
        'actual_vs_expected': {}
    }
    
    # Validar distribución por fuente
    actual_sources = distribution_stats['by_source']
    for source, expected_count in expected_counts.get('by_source', {}).items():
        actual_count = actual_sources.get(source, 0)
        validation_results['actual_vs_expected'][f'source_{source}'] = {
            'expected': expected_count,
            'actual': actual_count,
            'variance': actual_count - expected_count,
            'variance_percentage': ((actual_count - expected_count) / expected_count * 100) if expected_count > 0 else 0
        }
        
        # Validar que esté dentro del 20% del esperado
        variance_pct = abs(validation_results['actual_vs_expected'][f'source_{source}']['variance_percentage'])
        if variance_pct > 50:  # Más del 50% de varianza
            validation_results['errors'].append(
                f"Fuente {source}: esperados {expected_count}, obtenidos {actual_count} (varianza {variance_pct:.1f}%)"
            )
        elif variance_pct > 20:  # Más del 20% de varianza
            validation_results['warnings'].append(
                f"Fuente {source}: esperados {expected_count}, obtenidos {actual_count} (varianza {variance_pct:.1f}%)"
            )
    
    # Validar completitud promedio
    avg_completeness = distribution_stats['completeness']['average']
    expected_completeness = expected_counts.get('average_completeness', 0.75)
    
    if avg_completeness < expected_completeness * 0.8:  # 20% menos de lo esperado
        validation_results['errors'].append(
            f"Completitud promedio muy baja: {avg_completeness:.2f} (esperado: {expected_completeness:.2f})"
        )
    elif avg_completeness < expected_completeness:
        validation_results['warnings'].append(
            f"Completitud promedio baja: {avg_completeness:.2f} (esperado: {expected_completeness:.2f})"
        )
    
    return validation_results

def detect_unusual_distributions(distribution_stats):
    """Detecta distribuciones inusuales que pueden indicar problemas"""
    
    warnings = []
    
    # Detectar skewness en distribución por año
    year_dist = distribution_stats['by_year']
    if year_dist:
        recent_years = sum(count for year, count in year_dist.items() 
                          if int(year) >= datetime.datetime.now().year - 2)
        total_years = sum(year_dist.values())
        
        if recent_years / total_years > 0.5:
            warnings.append("Muchos registros recientes pueden indicar duplicados temporales")
        
        if recent_years / total_years < 0.1:
            warnings.append("Muy pocos registros recientes, posible scraping incompleto")
    
    # Detectar concentración excesiva en una industria
    industry_dist = distribution_stats['by_industry']
    if industry_dist:
        max_industry_count = max(industry_dist.values())
        total_companies = sum(industry_dist.values())
        
        if max_industry_count / total_companies > 0.4:
            max_industry = max(industry_dist, key=industry_dist.get)
            warnings.append(f"Industria {max_industry} domina con {max_industry_count/total_companies*100:.1f}% de registros")
    
    # Detectar distribución geográfica extraña
    location_dist = distribution_stats['by_location']
    if location_dist:
        us_count = location_dist.get('United States', 0)
        total_locations = sum(location_dist.values())
        
        if us_count / total_locations > 0.8:
            warnings.append("Distribución geográfica muy centrada en US, posible sesgo de fuentes")
    
    return warnings
```

---

## Validación de Codificación

### Verificación de Formatos y Encoding
```python
import chardet
import json
import csv
import codecs

def detect_encoding_issues(records):
    """Detecta problemas de encoding en los datos"""
    
    encoding_issues = {
        'encoding_errors': [],
        'invalid_characters': [],
        'format_violations': []
    }
    
    # Detectar caracteres inválidos en strings
    for i, record in enumerate(records):
        for field_name, field_value in record.items():
            if isinstance(field_value, str):
                try:
                    # Verificar encoding UTF-8
                    field_value.encode('utf-8').decode('utf-8')
                    
                    # Detectar caracteres de control
                    if any(ord(char) < 32 and char not in '\t\n\r' for char in field_value):
                        encoding_issues['invalid_characters'].append({
                            'record_index': i,
                            'field': field_name,
                            'character': repr(field_value)
                        })
                
                except UnicodeEncodeError as e:
                    encoding_issues['encoding_errors'].append({
                        'record_index': i,
                        'field': field_name,
                        'error': str(e)
                    })
    
    return encoding_issues

def validate_url_format(records):
    """Valida formato de URLs"""
    
    import re
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    url_issues = []
    
    for i, record in enumerate(records):
        website = record.get('website')
        if website:
            if not url_pattern.match(website):
                url_issues.append({
                    'record_index': i,
                    'record_id': record.get('id'),
                    'invalid_url': website,
                    'name': record.get('name')
                })
    
    return url_issues

def validate_date_format(records):
    """Valida formato de fechas"""
    
    date_issues = []
    
    for i, record in enumerate(records):
        scraped_at = record.get('scraped_at')
        if scraped_at:
            try:
                # Verificar formato ISO 8601
                datetime.datetime.fromisoformat(scraped_at.replace('Z', '+00:00'))
            except ValueError:
                date_issues.append({
                    'record_index': i,
                    'record_id': record.get('id'),
                    'invalid_date': scraped_at,
                    'field': 'scraped_at'
                })
        
        # Validar fechas de funding si existen
        funding = record.get('funding_total')
        if funding and funding.get('last_round_date'):
            try:
                datetime.datetime.strptime(funding['last_round_date'], '%Y-%m-%d')
            except ValueError:
                date_issues.append({
                    'record_index': i,
                    'record_id': record.get('id'),
                    'invalid_date': funding['last_round_date'],
                    'field': 'funding_total.last_round_date'
                })
    
    return date_issues

def test_csv_export(records, filename='test_export.csv'):
    """Prueba exportación a CSV para detectar problemas"""
    
    import pandas as pd
    
    try:
        # Aplanar datos para CSV
        flattened_data = []
        for record in records:
            flat_record = flatten_record(record)
            flattened_data.append(flat_record)
        
        df = pd.DataFrame(flattened_data)
        
        # Exportar a CSV temporal
        df.to_csv(filename, index=False, encoding='utf-8')
        
        # Leer de vuelta para verificar
        df_read = pd.read_csv(filename, encoding='utf-8')
        
        # Verificar integridad
        export_issues = {
            'row_count_match': len(df) == len(df_read),
            'column_count_match': len(df.columns) == len(df_read.columns),
            'columns_match': list(df.columns) == list(df_read.columns)
        }
        
        # Limpiar archivo temporal
        import os
        os.remove(filename)
        
        return export_issues
    
    except Exception as e:
        return {'error': str(e), 'type': 'export_failed'}

def test_json_export(records, filename='test_export.json'):
    """Prueba exportación a JSON para detectar problemas"""
    
    try:
        # Exportar a JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        # Leer de vuelta
        with open(filename, 'r', encoding='utf-8') as f:
            records_read = json.load(f)
        
        # Verificar integridad
        export_issues = {
            'record_count_match': len(records) == len(records_read),
            'structure_preserved': isinstance(records_read, list)
        }
        
        # Limpiar archivo temporal
        import os
        os.remove(filename)
        
        return export_issues
    
    except Exception as e:
        return {'error': str(e), 'type': 'export_failed'}
```

---

## Reporte Final de QA

### Generación de Reporte Comprensivo
```python
def generate_qa_report(records, expected_counts=None):
    """Genera reporte completo de QA"""
    
    from datetime import datetime
    
    report = f"""# Reporte de Control de Calidad
**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Registros analizados**: {len(records)}

---

## Resumen Ejecutivo
"""
    
    # 1. Validación de duplicados
    exact_dups = detect_exact_duplicates(records)
    fuzzy_dups = detect_fuzzy_duplicates(records)
    url_dups = detect_url_duplicates(records)
    
    total_duplicates = len(exact_dups) + len(fuzzy_dups) + len(url_dups)
    report += f"- **Duplicados detectados**: {total_duplicates}\n"
    
    # 2. Completitud de datos
    field_stats, source_stats = analyze_null_fields(records)
    avg_completeness = sum(100 - stats['null_percentage'] for stats in field_stats.values()) / len(field_stats)
    report += f"- **Completitud promedio**: {avg_completeness:.1f}%\n"
    
    # 3. Validación de rangos
    range_validation = validate_ranges(records)
    report += f"- **Errores de rango**: {len(range_validation['errors'])}\n"
    
    # 4. Distribución de datos
    distribution_stats = analyze_data_distribution(records)
    unique_sources = len(distribution_stats['by_source'])
    report += f"- **Fuentes únicas**: {unique_sources}\n"
    
    report += "\n---\n\n## Detalles de Validación\n\n"
    
    # Duplicados detallados
    if total_duplicates > 0:
        report += "### ❌ Duplicados\n\n"
        if exact_dups:
            report += f"- **Exactos**: {len(exact_dups)} registros\n"
        if fuzzy_dups:
            report += f"- **Por similitud**: {len(fuzzy_dups)} grupos\n"
        if url_dups:
            report += f"- **Por URL**: {len(url_dups)} casos\n"
        report += "\n"
    
    # Completitud detallada
    report += "### 📊 Completitud por Campo\n\n"
    report += "| Campo | Completitud | Estado |\n"
    report += "|-------|-------------|--------|\n"
    
    for field, stats in field_stats.items():
        completeness = 100 - stats['null_percentage']
        status = "✅" if completeness >= 95 else "⚠️" if completeness >= 85 else "❌"
        report += f"| {field} | {completeness:.1f}% | {status} |\n"
    
    # Errores de validación
    if range_validation['errors']:
        report += "\n### ⚠️ Errores de Validación\n\n"
        for error in range_validation['errors']:
            report += f"- {error}\n"
    
    # Advertencias
    if range_validation['warnings']:
        report += "\n### ⚡ Advertencias\n\n"
        for warning in range_validation['warnings']:
            report += f"- {warning}\n"
    
    # Distribución por fuente
    report += "\n### 📈 Distribución por Fuente\n\n"
    for source, count in distribution_stats['by_source'].items():
        report += f"- **{source}**: {count} registros\n"
    
    report += "\n---\n\n## Recomendaciones\n\n"
    
    # Generar recomendaciones basadas en los resultados
    recommendations = []
    
    if total_duplicates > 0:
        recommendations.append("Implementar deduplicación antes de la exportación final")
    
    if avg_completeness < 75:
        recommendations.append("Mejorar estrategias de extracción para aumentar completitud")
    
    if len(range_validation['errors']) > 0:
        recommendations.append("Corregir datos fuera de rango antes de usar en producción")
    
    if len(distribution_stats['by_source']) < 2:
        recommendations.append("Diversificar fuentes para reducir sesgo en datos")
    
    if not recommendations:
        recommendations.append("✅ Datos listos para producción")
    
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"
    
    return report

# Función principal de QA
def run_qa_pipeline(records, expected_counts=None):
    """Ejecuta pipeline completo de QA"""
    
    print("🔍 Iniciando control de calidad...")
    
    # 1. Validaciones básicas
    print("📋 Validando duplicados...")
    duplicates_report = {
        'exact': detect_exact_duplicates(records),
        'fuzzy': detect_fuzzy_duplicates(records),
        'url': detect_url_duplicates(records)
    }
    
    print("📊 Analizando completitud...")
    field_stats, source_stats = analyze_null_fields(records)
    
    print("📏 Validando rangos...")
    range_validation = validate_ranges(records)
    
    print("🌍 Analizando distribución...")
    distribution_stats = analyze_data_distribution(records)
    
    print("🔤 Verificando codificación...")
    encoding_issues = detect_encoding_issues(records)
    
    print("🔗 Validando URLs...")
    url_issues = validate_url_format(records)
    
    print("📅 Validando fechas...")
    date_issues = validate_date_format(records)
    
    print("💾 Probando exportación...")
    csv_test = test_csv_export(records)
    json_test = test_json_export(records)
    
    # 2. Generar reporte
    qa_report = generate_qa_report(records, expected_counts)
    
    # 3. Guardar resultados
    import json
    qa_results = {
        'duplicates': duplicates_report,
        'field_stats': field_stats,
        'source_stats': source_stats,
        'range_validation': range_validation,
        'distribution_stats': distribution_stats,
        'encoding_issues': encoding_issues,
        'url_issues': url_issues,
        'date_issues': date_issues,
        'export_tests': {'csv': csv_test, 'json': json_test},
        'timestamp': datetime.now().isoformat()
    }
    
    with open('logs/qa_results.json', 'w') as f:
        json.dump(qa_results, f, indent=2, default=str)
    
    with open('logs/qa_report.md', 'w') as f:
        f.write(qa_report)
    
    print("✅ Control de calidad completado")
    print(f"📄 Reporte guardado en logs/qa_report.md")
    print(f"📊 Resultados JSON en logs/qa_results.json")
    
    return qa_results, qa_report
```

---

**Última actualización**: 15 de noviembre de 2025
**Responsable**: Equipo de Desarrollo