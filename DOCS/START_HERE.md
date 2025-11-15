# 🚀 GUÍA DE INICIO RÁPIDO - founders25-scraper

## ⚡ PASOS INMEDIATOS

### 1. **INSTALAR DEPENDENCIAS**
```bash
# En tu terminal, desde la carpeta del proyecto:
pip install -r requirements.txt
```

### 2. **PROBAR QUE FUNCIONA**
```bash
# Ejecuta esto para probar:
python main.py test
```

### 3. **SCRAPING SIMPLE** 
```bash
# Para probar con una URL específica:
python main.py single "https://www.crunchbase.com/organization/airbnb"
```

### 4. **CREAR ARCHIVO DE URLs**
```bash
# Crea un archivo de ejemplo:
python main.py sample
```

Luego edita el archivo `data/sample_urls.txt` y agrega tus URLs favoritas.

### 5. **SCRAPING MASIVO**
```bash
# Cuando tengas el archivo listo:
python main.py batch data/sample_urls.txt
```

---

## 🆘 SI ALGO FALLA

### **Error: ModuleNotFoundError**
```bash
# Instalar dependencias faltantes:
pip install requests beautifulsoup4 lxml pandas python-dotenv
```

### **Error: Permission denied**
```bash
# En Windows:
python -m pip install --user requests beautifulsoup4 lxml pandas python-dotenv

# En Linux/Mac:
pip install --user requests beautifulsoup4 lxml pandas python-dotenv
```

### **Error: No module named 'config'**
```bash
# Verifica que estés en el directorio correcto:
pwd  # Debe mostrar la carpeta del scraper
ls   # Debe mostrar archivos: main.py, config.py, etc.
```

---

## ✅ VERIFICACIÓN FINAL

Para confirmar que todo funciona:

1. **Ejecuta**: `python main.py status`
2. **Debe mostrar**: Estado del scraper sin errores
3. **Si muestra "✅ Active hours"**: Perfecto, puedes scrapear
4. **Si muestra "⏸️ Off hours"**: Espera hasta las 8:00 AM (GMT+1)

---

## 🎯 COMANDOS PRINCIPALES

```bash
# Ver todas las opciones:
python main.py --help

# Ver versión:
python main.py --version

# Estado actual:
python main.py status

# Scraping individual:
python main.py single "URL_AQUI"

# Scraping masivo:
python main.py batch archivo_con_urls.txt
```

---

## 📞 EJEMPLO REAL

```bash
# 1. Prueba básica:
python main.py test

# 2. Scraping de Airbnb en Crunchbase:
python main.py single "https://www.crunchbase.com/organization/airbnb"

# 3. Crear archivo de URLs:
python main.py sample

# 4. Editar data/sample_urls.txt agregando más URLs

# 5. Ejecutar scraping masivo:
python main.py batch data/sample_urls.txt
```

¡Con estos 5 pasos ya puedes scrapear datos!