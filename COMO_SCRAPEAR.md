# 🚀 CÓMO INICIAR EL SCRAPING - PASO A PASO

## ⚡ INICIO RÁPIDO (3 pasos)

### **PASO 1: Verificar que está funcionando**
```bash
python main_windows.py status
```
**¿Qué debería ver?** Estado "Active hours" y métricas en 0

---

### **PASO 2: Crear archivo con URLs**
```bash
python main_windows.py sample
```
**¿Qué hace?** Crea el archivo `data/sample_urls.txt` con URLs de ejemplo

---

### **PASO 3: Scraping masivo**
```bash
python main_windows.py batch data/sample_urls.txt
```
**¿Qué hace?** Extrae datos de todas las URLs del archivo

---

## 🎯 SCRAPING INDIVIDUAL

### **Para scrapear una URL específica:**
```bash
python main_windows.py single "https://ejemplo.com"
```

### **Ejemplo real:**
```bash
python main_windows.py single "https://quotes.toscrape.com/"
```

---

## 📝 CREAR TUS PROPIAS URLs

### **1. Editar el archivo de URLs:**
```bash
# Edita este archivo:
data/sample_urls.txt
```

### **2. Formato del archivo:**
```
# URLs de ejemplo para batch scraping
# Formato: una URL por línea
# Las líneas que empiecen con # son comentarios

https://www.crunchbase.com/organization/airbnb
https://angel.co/company/airbnb
https://www.producthunt.com/products/airbnb

# Agrega más URLs aquí...
```

### **3. Ejecutar scraping:**
```bash
python main_windows.py batch data/sample_urls.txt
```

---

## 📊 VER LOS RESULTADOS

### **Archivos generados automáticamente:**
- 📁 `data/` - Datos extraídos (.json)
- 📁 `exports/` - Resultados finales (.json/.csv)
- 📁 `logs/` - Archivos de log

### **Ver último resultado:**
```bash
# Lista los archivos más recientes
ls -la data/
ls -la exports/
```

---

## 🛠️ COMANDOS ÚTILES

### **Ver ayuda completa:**
```bash
python main_windows.py --help
```

### **Ver versión:**
```bash
python main_windows.py --version
```

### **Estado actual:**
```bash
python main_windows.py status
```

---

## ⚠️ NOTAS IMPORTANTES

1. **Usa `main_windows.py`** (NO `main.py`) para evitar problemas de encoding
2. **Horarios**: Funciona solo 8AM-6PM (GMT+1)
3. **Velocidad**: Lento por diseño (2-4 segundos entre requests)
4. **Sitios protegidos**: Algunos sitios bloquean bots (es normal)
5. **Datos**: Se guardan automáticamente

---

## 🎉 ¡EMPIEZA AHORA!

**Para empezar en 30 segundos:**
1. `python main_windows.py sample`
2. `python main_windows.py batch data/sample_urls.txt`

¡Y ya estás scrapearando datos!