# Template de Pull Request - founders25-scraper

## 📝 Descripción del Cambio
<!-- Proporciona una descripción clara y concisa de lo que hace este PR -->

**¿Qué problema resuelve?**
Describe el problema o issue que este PR aborda.

**¿Qué cambio incluye?**
- Feature: [Descripción breve]
- Fix: [Descripción breve]  
- Refactor: [Descripción breve]
- Docs: [Descripción breve]

**¿Por qué es necesario este cambio?**
Explica la necesidad del cambio y cómo mejora el proyecto.

---

## 🔗 Issue Relacionado
<!-- Link al issue que resuelve este PR -->

Closes #[número]
Related to #[número]

---

## ✅ Checklist de Validación

### Funcionalidad
- [ ] **El código funciona como se espera**
- [ ] **La nueva funcionalidad está completa**
- [ ] **Los tests (si existen) pasan**
- [ ] **La funcionalidad se probó manualmente**

### Código
- [ ] **El código sigue las convenciones del proyecto**
- [ ] **No hay linting errors**
- [ ] **El código está bien documentado**
- [ ] **No hay código duplicado**

### Documentación
- [ ] **Se actualizó la documentación necesaria**
- [ ] **Los comentarios del código son claros**
- [ ] **Se actualizó el README si es necesario**
- [ ] **Se documentaron los cambios en APIs**

### Performance
- [ ] **No se introdujeron regressions de performance**
- [ ] **El código es eficiente**
- [ ] **Se considera la escalabilidad**

### Seguridad
- [ ] **No hay vulnerabilidades de seguridad**
- [ ] **Las credenciales están protegidas**
- [ ] **Se validan los inputs del usuario**

---

## 🧪 Cómo Probar

### Pruebas Manuales
<!-- Describe cómo probar manualmente los cambios -->

1. **Requisitos previos**
   ```bash
   # Commands needed before testing
   ```

2. **Pasos de prueba**
   ```bash
   # Step-by-step testing instructions
   ```

3. **Resultado esperado**
   ```
   # What should happen
   ```

### Pruebas Automáticas
<!-- Si aplicable, describe las pruebas automáticas -->

```bash
# Commands to run tests
pytest tests/
```

### Datos de Prueba
<!-- Usa datos de ejemplo para demostrar el funcionamiento -->

```python
# Ejemplo de uso con datos de prueba
```

---

## 📊 Cambios Esperados

### Datos Extraídos
- **Antes**: [Descripción del comportamiento anterior]
- **Después**: [Descripción del nuevo comportamiento]

### Performance
- **Tiempo de ejecución**: [antes] → [después]
- **Uso de memoria**: [antes] → [después]
- **Requests por minuto**: [valor]

### Compatibilidad
- **Versiones de Python soportadas**: [lista]
- **Dependencias actualizadas**: [lista]
- **Breaking changes**: [sí/no + descripción]

---

## ⚠️ Riesgos y Limitaciones

### Riesgos Identificados
- **Riesgo 1**: [Descripción y probabilidad]
- **Riesgo 2**: [Descripción y probabilidad]

### Limitaciones Conocidas
- **Limitación 1**: [Descripción]
- **Limitación 2**: [Descripción]

### Mitigaciones
- **Mitigación 1**: [Cómo se aborda el riesgo]
- **Mitigación 2**: [Cómo se aborda el riesgo]

---

## 🔍 Review Checklist para Revisors

### Funcionalidad
- [ ] **La implementación cumple con los requisitos**
- [ ] **El código es correcto y sin bugs**
- [ ] **Los casos edge están manejados**
- [ ] **La funcionalidad es intuitiva**

### Código
- [ ] **El código es legible y bien estructurado**
- [ ] **Se siguen las mejores prácticas**
- [ ] **El código es reutilizable y mantenible**
- [ ] **No hay code smells obvios**

### Testing
- [ ] **Existen pruebas para la nueva funcionalidad**
- [ ] **Las pruebas cubren casos importantes**
- [ ] **Las pruebas pasan consistentemente**
- [ ] **Se probaron casos de error**

### Performance y Escalabilidad
- [ ] **El código es eficiente**
- [ ] **No introduce memory leaks**
- [ ] **Escala apropiadamente**
- [ ] **Se consideran recursos del sistema**

### Seguridad
- [ ] **No introduce vulnerabilidades**
- [ ] **Los datos sensibles están protegidos**
- [ ] **Se validan inputs externos**
- [ ] **Se sigue el principio de menor privilegio**

---

## 🎯 Casos de Uso Afectados

### Usuarios/Use Cases Afectados
- **Caso de uso 1**: [Descripción de cómo se afecta]
- **Caso de uso 2**: [Descripción de cómo se afecta]

### APIs Endpoints
- **Endpoint 1**: [Cambios realizados]
- **Endpoint 2**: [Cambios realizados]

### Archivos de Configuración
- **Archivo 1**: [Cambios realizados]
- **Archivo 2**: [Cambios realizados]

---

## 📝 Changelog

### Tipo de Cambio
Selecciona el tipo de cambio que mejor describe tu PR:

- **[ADD]** Nueva funcionalidad
- **[CHANGE]** Cambio en funcionalidad existente  
- **[FIX]** Corrección de bug
- **[UPDATE]** Actualización de dependencia
- **[REMOVE]** Eliminación de funcionalidad
- **[DEPRECATE]** Deprecación de funcionalidad
- **[SECURITY]** Mejora de seguridad

### Descripción Detallada
<!-- Usa formato de changelog estándar -->

**Versión**: [X.Y.Z] (si aplica)

** Cambios:
- [ADD] Nueva función `nombre_funcion()` para [propósito]
- [CHANGE] Modificado selector CSS para [campo] en [sitio]
- [FIX] Corregido error de parsing en [componente]
- [UPDATE] Actualizado `lxml` a versión 4.9.3
- [REMOVE] Eliminada función obsoleta `old_function()`

---

## 📋 Ejemplos de Commits

### Formato Recomendado
```
[tipo]([área]): descripción corta

descripción más detallada si es necesario

- punto específico 1
- punto específico 2

Closes #[issue]
```

### Ejemplos
```
feat(selectors): agregar selector fallback para Crunchbase website

- Actualizar mapeo de selectores para campo website
- Agregar validación de URL en post-procesamiento
- Mejorar manejo de casos edge

Closes #123
```

```
fix(pagination): corregir detección de fin en AngelList

- Cambiar criterio de detección basado en conteo de elementos
- Mejorar log de eventos de paginación
- Agregar test para caso edge

Related #456
```

```
docs(readme): actualizar instrucciones de instalación

- Agregar sección de dependencias opcionales
- Mejorar ejemplos de uso
- Actualizar requisitos de sistema

No issue
```

---

## 🔍 Detalles Técnicos

### Arquitectura
- **Componentes afectados**: [lista]
- **Dependencias modificadas**: [lista]
- **Interfaces cambiadas**: [lista]

### Algoritmos/Lógica
- **Algoritmo principal**: [descripción]
- **Complejidad**: [O(n), O(n log n), etc.]
- **Casos edge manejados**: [lista]

### Base de Datos/Storage
- **Esquema modificado**: [sí/no]
- **Migraciones requeridas**: [sí/no + descripción]
- **Backup necesario**: [sí/no]

---

## 📸 Screenshots/Demo (Si Aplica)

<!-- Si el cambio es visual o afecta la UI, incluye screenshots -->

**Antes**:
![Antes del cambio](screenshots/before.png)

**Después**:
![Después del cambio](screenshots/after.png)

---

## 🚀 Deployment

### Preparación para Producción
- [ ] **Variables de entorno actualizadas**
- [ ] **Configuración de producción validada**
- [ ] **Backup de datos realizado**
- [ ] **Plan de rollback definido**

### Pasos de Deploy
```bash
# Comandos para deployment
```

### Rollback Plan
```bash
# Comandos para rollback si es necesario
```

---

## 📞 Contacto

**Desarrollador**: [nombre]
**Email**: [email]
**Slack**: [@usuario]
**Fecha límite de review**: [fecha]

---

## ✅ Aprobaciones Requeridas

- [ ] **Review de código principal**
- [ ] **Review de seguridad** (si aplica)
- [ ] **Review de performance** (si aplica)
- [ ] **Review de producto** (si aplica)

**Mínimo de aprobaciones**: 1

---

## 📝 Notas Adicionales

### Contexto
[Cualquier información contextual adicional que ayude a entender el cambio]

### Decisiones de Diseño
- **Alternativas consideradas**: [lista]
- **Razón de la elección**: [explicación]
- **Trade-offs**: [descripción]

### Trabajo Futuro
- [ ] **Tarea 1 pendiente**
- [ ] **Tarea 2 pendiente**
- [ ] **Mejoras futuras identificadas**

---

**Template version**: 1.0  
**Última actualización**: 15 de noviembre de 2025  
**Responsable**: Equipo de Desarrollo