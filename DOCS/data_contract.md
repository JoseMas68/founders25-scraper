# Contrato de Datos - Esquema y Validación

## Objetivo del Documento
Este documento define el esquema de datos completo para el scraper, incluyendo campos requeridos, tipos de datos, validaciones, casos límite y ejemplos de exportación.

---

## Esquema Principal de Datos

### Entidad: **Company**

#### Campos Requeridos (Required Fields)
```python
REQUIRED_FIELDS = {
    'id': {
        'type': 'string',
        'description': 'Identificador único de la empresa',
        'required': True,
        'example': 'crunchbase_1234567890',
        'validation': 'alphanumeric_with_underscores'
    },
    'name': {
        'type': 'string',
        'description': 'Nombre oficial de la empresa',
        'required': True,
        'min_length': 2,
        'max_length': 100,
        'example': 'Airbnb, Inc.',
        'validation': 'non_empty_string'
    },
    'website': {
        'type': 'url',
        'description': 'URL oficial del sitio web',
        'required': True,
        'format': 'https://domain.com',
        'example': 'https://www.airbnb.com',
        'validation': 'valid_url_format'
    },
    'source': {
        'type': 'string',
        'description': 'Sitio web de origen de los datos',
        'required': True,
        'allowed_values': ['crunchbase', 'angellist', 'producthunt', 'github'],
        'example': 'crunchbase',
        'validation': 'enum_restriction'
    },
    'scraped_at': {
        'type': 'datetime',
        'description': 'Timestamp de cuando se extrajeron los datos',
        'required': True,
        'format': 'ISO 8601',
        'example': '2025-11-15T13:22:03Z',
        'validation': 'valid_datetime'
    }
}
```

#### Campos Opcionales (Optional Fields)
```python
OPTIONAL_FIELDS = {
    'description': {
        'type': 'string',
        'description': 'Descripción del negocio o producto',
        'required': False,
        'max_length': 1000,
        'example': 'Online marketplace for vacation rentals',
        'default': None,
        'validation': 'string_with_sanitization'
    },
    'founded_year': {
        'type': 'integer',
        'description': 'Año de fundación de la empresa',
        'required': False,
        'min_value': 1990,
        'max_value': 2025,
        'example': 2008,
        'default': None,
        'validation': 'year_in_valid_range'
    },
    'location': {
        'type': 'object',
        'description': 'Ubicación de la empresa',
        'required': False,
        'properties': {
            'city': {'type': 'string', 'max_length': 50},
            'country': {'type': 'string', 'max_length': 50},
            'country_code': {'type': 'string', 'pattern': '^[A-Z]{2}$'},
            'coordinates': {
                'type': 'object',
                'properties': {
                    'latitude': {'type': 'float', 'min': -90, 'max': 90},
                    'longitude': {'type': 'float', 'min': -180, 'max': 180}
                }
            }
        },
        'example': {
            'city': 'San Francisco',
            'country': 'United States',
            'country_code': 'US',
            'coordinates': {'latitude': 37.7749, 'longitude': -122.4194}
        },
        'default': None,
        'validation': 'complete_location_or_none'
    },
    'industry': {
        'type': 'array',
        'description': 'Industrias o sectores de la empresa',
        'required': False,
        'items': {'type': 'string', 'max_length': 50},
        'max_items': 5,
        'example': ['Technology', 'Travel', 'Hospitality'],
        'default': [],
        'validation': 'unique_industries'
    },
    'employee_count': {
        'type': 'integer',
        'description': 'Número estimado de empleados',
        'required': False,
        'min_value': 1,
        'max_value': 1000000,
        'example': 5000,
        'default': None,
        'validation': 'reasonable_employee_count'
    },
    'funding_total': {
        'type': 'object',
        'description': 'Información de financiamiento total',
        'required': False,
        'properties': {
            'amount_usd': {'type': 'float', 'min': 0},
            'currency': {'type': 'string', 'default': 'USD'},
            'last_round_date': {'type': 'date', 'format': 'YYYY-MM-DD'}
        },
        'example': {
            'amount_usd': 1500000000.0,
            'currency': 'USD',
            'last_round_date': '2020-01-15'
        },
        'default': None,
        'validation': 'valid_funding_data'
    },
    'valuation': {
        'type': 'object',
        'description': 'Valoración de la empresa',
        'required': False,
        'properties': {
            'amount_usd': {'type': 'float', 'min': 0},
            'date': {'type': 'date', 'format': 'YYYY-MM-DD'},
            'stage': {'type': 'string', 'allowed_values': ['series_a', 'series_b', 'series_c', 'ipo']}
        },
        'example': {
            'amount_usd': 75000000000.0,
            'date': '2020-12-01',
            'stage': 'series_d'
        },
        'default': None,
        'validation': 'valid_valuation_data'
    },
    'tags': {
        'type': 'array',
        'description': 'Tags o etiquetas relacionadas',
        'required': False,
        'items': {'type': 'string', 'max_length': 30},
        'max_items': 20,
        'example': ['unicorn', 'b2b', 'marketplace'],
        'default': [],
        'validation': 'unique_tags'
    },
    'social_links': {
        'type': 'object',
        'description': 'Enlaces a redes sociales',
        'required': False,
        'properties': {
            'linkedin': {'type': 'url'},
            'twitter': {'type': 'url'},
            'facebook': {'type': 'url'},
            'github': {'type': 'url'}
        },
        'example': {
            'linkedin': 'https://linkedin.com/company/airbnb',
            'twitter': 'https://twitter.com/airbnb'
        },
        'default': {},
        'validation': 'valid_social_urls'
    },
    'logo_url': {
        'type': 'url',
        'description': 'URL del logo de la empresa',
        'required': False,
        'example': 'https://logo.clearbit.com/airbnb.com',
        'default': None,
        'validation': 'valid_image_url'
    },
    'status': {
        'type': 'string',
        'description': 'Estado operativo actual',
        'required': False,
        'allowed_values': ['active', 'acquired', 'ipo', 'closed', 'unknown'],
        'default': 'unknown',
        'example': 'active',
        'validation': 'valid_status_value'
    }
}
```

---

## Validaciones y Casos Límite

### Validaciones de Campos Individuales
```python
import re
import validators
from datetime import datetime, date

def validate_id(id_value):
    """Validar formato de ID único"""
    if not id_value:
        return False, "ID es requerido"
    
    # Formato: source_timestamp_random
    pattern = r'^[a-z]+_\d{10,13}_[a-zA-Z0-9]+$'
    if not re.match(pattern, id_value):
        return False, "Formato de ID inválido"
    
    return True, None

def validate_name(name_value):
    """Validar nombre de empresa"""
    if not name_value or not isinstance(name_value, str):
        return False, "Nombre es requerido y debe ser string"
    
    if len(name_value.strip()) < 2:
        return False, "Nombre demasiado corto"
    
    if len(name_value) > 100:
        return False, "Nombre demasiado largo"
    
    return True, None

def validate_website(url_value):
    """Validar URL del sitio web"""
    if not url_value or not isinstance(url_value, str):
        return False, "Website es requerido"
    
    if not validators.url(url_value):
        return False, "URL inválida"
    
    # Verificar que no sea localhost o IP privada
    if any(domain in url_value.lower() for domain in ['localhost', '127.0.0.1', '192.168.', '10.', '172.']):
        return False, "URL debe ser pública"
    
    return True, None

def validate_location(location_data):
    """Validar datos de ubicación"""
    if not location_data:
        return True, None  # Opcional
    
    if not isinstance(location_data, dict):
        return False, "Location debe ser un objeto"
    
    # Si hay coordenadas, deben ser válidas
    if 'coordinates' in location_data:
        coords = location_data['coordinates']
        if not isinstance(coords, dict):
            return False, "Coordinates debe ser objeto"
        
        lat = coords.get('latitude')
        lng = coords.get('longitude')
        
        if lat is not None and not (-90 <= lat <= 90):
            return False, "Latitud inválida"
        
        if lng is not None and not (-180 <= lng <= 180):
            return False, "Longitud inválida"
    
    return True, None

def validate_founded_year(year_value):
    """Validar año de fundación"""
    if year_value is None:
        return True, None  # Opcional
    
    if not isinstance(year_value, int):
        return False, "Año debe ser número entero"
    
    current_year = datetime.now().year
    
    if year_value < 1990:
        return False, "Año muy anterior (pre-internet)"
    
    if year_value > current_year:
        return False, "Año en el futuro"
    
    return True, None

def validate_employee_count(count_value):
    """Validar número de empleados"""
    if count_value is None:
        return True, None  # Opcional
    
    if not isinstance(count_value, (int, float)):
        return False, "Employee count debe ser número"
    
    if count_value < 1:
        return False, "Employee count debe ser positivo"
    
    if count_value > 1000000:  # 1 millón
        return False, "Employee count muy alto"
    
    return True, None
```

### Validaciones de Integridad de Registro
```python
def validate_complete_record(record):
    """Validación completa de un registro de empresa"""
    
    validation_results = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'completeness_score': 0.0
    }
    
    # Validar campos requeridos
    required_validation = validate_required_fields(record)
    validation_results['errors'].extend(required_validation['errors'])
    
    # Validar tipos de datos
    type_validation = validate_field_types(record)
    validation_results['errors'].extend(type_validation['errors'])
    
    # Validaciones de negocio
    business_validation = validate_business_rules(record)
    validation_results['errors'].extend(business_validation['errors'])
    validation_results['warnings'].extend(business_validation['warnings'])
    
    # Calcular score de completitud
    validation_results['completeness_score'] = calculate_completeness_score(record)
    
    # Determinar validez general
    validation_results['is_valid'] = len(validation_results['errors']) == 0
    
    return validation_results

def validate_required_fields(record):
    """Validar que todos los campos requeridos estén presentes"""
    errors = []
    
    for field_name, field_config in REQUIRED_FIELDS.items():
        if field_name not in record or record[field_name] is None:
            errors.append(f"Campo requerido faltante: {field_name}")
    
    return {'errors': errors}

def validate_field_types(record):
    """Validar tipos de datos"""
    errors = []
    
    all_fields = {**REQUIRED_FIELDS, **OPTIONAL_FIELDS}
    
    for field_name, field_config in all_fields.items():
        if field_name in record and record[field_name] is not None:
            value = record[field_name]
            expected_type = field_config['type']
            
            if expected_type == 'string' and not isinstance(value, str):
                errors.append(f"{field_name}: debe ser string")
            elif expected_type == 'integer' and not isinstance(value, int):
                errors.append(f"{field_name}: debe ser entero")
            elif expected_type == 'float' and not isinstance(value, (int, float)):
                errors.append(f"{field_name}: debe ser número")
            elif expected_type == 'url' and not isinstance(value, str):
                errors.append(f"{field_name}: debe ser URL string")
            elif expected_type == 'array' and not isinstance(value, list):
                errors.append(f"{field_name}: debe ser array")
            elif expected_type == 'object' and not isinstance(value, dict):
                errors.append(f"{field_name}: debe ser objeto")
    
    return {'errors': errors}

def validate_business_rules(record):
    """Validaciones específicas de negocio"""
    errors = []
    warnings = []
    
    # Regla: Si hay founded_year, debe ser consistente con status
    if record.get('founded_year') and record.get('status'):
        founded_year = record['founded_year']
        current_year = datetime.now().year
        
        if record['status'] == 'closed' and founded_year > current_year - 1:
            warnings.append("Empresa marcada como cerrada pero founded_year es reciente")
    
    # Regla: Employee count debe ser consistente con funding
    if record.get('funding_total') and record.get('employee_count'):
        funding_amount = record['funding_total'].get('amount_usd', 0)
        employee_count = record['employee_count']
        
        # Startup con mucho funding debe tener employees
        if funding_amount > 100000000 and employee_count < 10:
            warnings.append("Funding muy alto pero pocos empleados")
        
        # Muchos empleados con poco funding es sospechoso
        if employee_count > 100 and funding_amount < 100000:
            warnings.append("Muchos empleados pero poco funding")
    
    # Regla: Website debe coincidir con dominio conocido
    website = record.get('website', '')
    if website and 'source' in record:
        source = record['source']
        if source == 'crunchbase' and 'crunchbase' in website.lower():
            warnings.append("Website parece ser crunchbase en lugar de sitio oficial")
    
    return {'errors': errors, 'warnings': warnings}

def calculate_completeness_score(record):
    """Calcular score de completitud de datos (0.0 - 1.0)"""
    
    total_optional_fields = len(OPTIONAL_FIELDS)
    filled_optional_fields = 0
    
    for field_name in OPTIONAL_FIELDS.keys():
        value = record.get(field_name)
        if value is not None:
            # Considerar arrays vacíos como no llenos
            if isinstance(value, list) and len(value) == 0:
                continue
            # Considerar objetos vacíos como no llenos
            if isinstance(value, dict) and len(value) == 0:
                continue
            filled_optional_fields += 1
    
    # Campos requeridos siempre cuentan como llenos
    required_fields_count = len(REQUIRED_FIELDS)
    total_fields = required_fields_count + total_optional_fields
    filled_fields = required_fields_count + filled_optional_fields
    
    return filled_fields / total_fields if total_fields > 0 else 0.0
```

### Casos Límite y Manejo de Errores

#### **Casos Límite de Datos**
```python
def handle_edge_cases(raw_data, source):
    """Maneja casos límite en datos extraídos"""
    
    processed_data = raw_data.copy()
    
    # Caso: Nombre vacío o muy corto
    if not processed_data.get('name') or len(processed_data['name'].strip()) < 2:
        # Intentar extraer nombre de URL o usar dominio
        if 'website' in processed_data:
            domain = extract_domain_from_url(processed_data['website'])
            processed_data['name'] = domain or 'Unknown Company'
    
    # Caso: Website inválido o vacío
    website = processed_data.get('website', '')
    if not website or not validators.url(website):
        # Si es URL inválida, intentar normalizarla
        if website and not website.startswith(('http://', 'https://')):
            processed_data['website'] = f'https://{website}'
        else:
            # Si no se puede reparar, usar placeholder
            processed_data['website'] = f'https://company-{processed_data.get("id", "unknown")}.com'
    
    # Caso:founded_year fuera de rango
    founded_year = processed_data.get('founded_year')
    if founded_year and (founded_year < 1990 or founded_year > datetime.now().year):
        # Ajustar año inválido
        if founded_year < 1990:
            processed_data['founded_year'] = 1990
        else:
            processed_data['founded_year'] = datetime.now().year
    
    # Caso: Employee count muy alto (probablemente es string)
    employee_count = processed_data.get('employee_count')
    if employee_count and isinstance(employee_count, str):
        # Intentar extraer número de string
        import re
        numbers = re.findall(r'\d+', employee_count)
        if numbers:
            processed_data['employee_count'] = int(numbers[0])
        else:
            processed_data['employee_count'] = None
    
    # Caso: Múltiples ubicaciones
    location = processed_data.get('location')
    if isinstance(location, list):
        # Tomar la primera ubicación completa
        if location:
            processed_data['location'] = location[0] if isinstance(location[0], dict) else None
    
    # Caso: URLs de redes sociales múltiples
    social_links = processed_data.get('social_links', {})
    if isinstance(social_links, dict):
        # Limpiar URLs vacías
        cleaned_links = {}
        for platform, url in social_links.items():
            if url and validators.url(url):
                cleaned_links[platform] = url
        processed_data['social_links'] = cleaned_links
    
    return processed_data
```

---

## Ejemplos de Datos

### Ejemplo JSON Completo
```json
{
  "id": "crunchbase_1702664523000_abc123def",
  "name": "Airbnb, Inc.",
  "website": "https://www.airbnb.com",
  "source": "crunchbase",
  "scraped_at": "2025-11-15T13:22:03Z",
  "description": "Online marketplace for vacation rentals and unique travel experiences",
  "founded_year": 2008,
  "location": {
    "city": "San Francisco",
    "country": "United States",
    "country_code": "US",
    "coordinates": {
      "latitude": 37.7749,
      "longitude": -122.4194
    }
  },
  "industry": ["Technology", "Travel", "Hospitality", "Marketplace"],
  "employee_count": 5654,
  "funding_total": {
    "amount_usd": 1500000000.0,
    "currency": "USD",
    "last_round_date": "2020-04-06"
  },
  "valuation": {
    "amount_usd": 75000000000.0,
    "date": "2020-12-01",
    "stage": "series_d"
  },
  "tags": ["unicorn", "b2b", "marketplace", "sharing-economy"],
  "social_links": {
    "linkedin": "https://linkedin.com/company/airbnb",
    "twitter": "https://twitter.com/airbnb",
    "facebook": "https://facebook.com/airbnb"
  },
  "logo_url": "https://logo.clearbit.com/airbnb.com",
  "status": "active"
}
```

### Ejemplo CSV
```csv
id,name,website,source,scraped_at,description,founded_year,city,country,country_code,latitude,longitude,industry,employee_count,funding_total_usd,last_round_date,valuation_usd,valuation_date,valuation_stage,tags,linkedin,twitter,facebook,logo_url,status
crunchbase_1702664523000_abc123def,Airbnb Inc.,https://www.airbnb.com,crunchbase,2025-11-15T13:22:03Z,Online marketplace for vacation rentals and unique travel experiences,2008,San Francisco,United States,US,37.7749,-122.4194,"Technology,Travel,Hospitality,Marketplace",5654,1500000000.0,2020-04-06,75000000000.0,2020-12-01,series_d,"unicorn,b2b,marketplace,sharing-economy",https://linkedin.com/company/airbnb,https://twitter.com/airbnb,https://facebook.com/airbnb,https://logo.clearbit.com/airbnb.com,active
```

### Ejemplo de Registro Mínimo
```json
{
  "id": "github_1702664523000_def456ghi",
  "name": "open-source-project",
  "website": "https://github.com/user/repo",
  "source": "github",
  "scraped_at": "2025-11-15T13:22:03Z"
}
```

---

## Exportación y Formatos

### Configuración de Exportación
```python
EXPORT_CONFIGS = {
    'json': {
        'filename': 'companies_{timestamp}.json',
        'format': 'json',
        'compression': 'gzip',  # Opciones: gzip, bz2, xz
        'encoding': 'utf-8',
        'ensure_ascii': False,
        'indent': 2
    },
    'csv': {
        'filename': 'companies_{timestamp}.csv',
        'format': 'csv',
        'encoding': 'utf-8',
        'sep': ',',
        'quotechar': '"',
        'escapechar': '\\',
        'lineterminator': '\n',
        'date_format': '%Y-%m-%d',
        'decimal_separator': '.'
    },
    'excel': {
        'filename': 'companies_{timestamp}.xlsx',
        'format': 'xlsx',
        'sheet_name': 'Companies',
        'engine': 'openpyxl',
        'index': False,
        'date_format': 'yyyy-mm-dd',
        'decimal_separator': '.'
    }
}
```

### Funciones de Exportación
```python
def export_to_json(data, filename, config=None):
    """Exportar datos a JSON"""
    if config is None:
        config = EXPORT_CONFIGS['json']
    
    import json
    import gzip
    from datetime import datetime
    
    if filename.endswith('.gz'):
        with gzip.open(filename, 'wt', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=config.get('ensure_ascii', False), 
                     indent=config.get('indent', 2))
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=config.get('ensure_ascii', False), 
                     indent=config.get('indent', 2))

def export_to_csv(data, filename, config=None):
    """Exportar datos a CSV"""
    if config is None:
        config = EXPORT_CONFIGS['csv']
    
    import pandas as pd
    
    df = pd.DataFrame(data)
    
    # Flatten nested objects para CSV
    flattened_data = []
    for record in data:
        flat_record = flatten_record(record)
        flattened_data.append(flat_record)
    
    df = pd.DataFrame(flattened_data)
    df.to_csv(filename, encoding=config['encoding'], sep=config['sep'], 
              index=False, date_format=config['date_format'])

def export_to_excel(data, filename, config=None):
    """Exportar datos a Excel"""
    if config is None:
        config = EXPORT_CONFIGS['excel']
    
    import pandas as pd
    
    flattened_data = []
    for record in data:
        flat_record = flatten_record(record)
        flattened_data.append(flat_record)
    
    df = pd.DataFrame(flattened_data)
    
    with pd.ExcelWriter(filename, engine=config['engine']) as writer:
        df.to_excel(writer, sheet_name=config['sheet_name'], 
                   index=config.get('index', False), 
                   date_format=config.get('date_format'))

def flatten_record(record):
    """Aplanar registro anidado para CSV/Excel"""
    flat = {}
    
    for key, value in record.items():
        if isinstance(value, dict):
            # Aplanar objetos anidados
            for subkey, subvalue in value.items():
                flat[f"{key}_{subkey}"] = subvalue
        elif isinstance(value, list):
            # Convertir arrays a strings separados por comas
            flat[key] = ','.join(str(item) for item in value) if value else ''
        else:
            flat[key] = value
    
    return flat
```

---

**Última actualización**: 15 de noviembre de 2025
**Responsable**: Equipo de Desarrollo