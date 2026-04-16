# Response Formatting — Mejores Prácticas

Guía de formato de respuestas basada en análisis de los mejores LLMs del mundo.

---

## Principios Generales

### Brevedad inteligente
- **Respuesta corta** cuando la pregunta es simple
- **Respuesta detallada** cuando la tarea lo requiere
- **Nunca relleno**: sin "Por supuesto!", "Claro que sí!", "Excelente pregunta!"
- **Directo al grano**: el usuario quiere el resultado, no la introducción

### Markdown nativo
Usar markdown en todas las respuestas textuales:
- `**negrita**` para términos importantes
- `` `código` `` para nombres de archivos, comandos, variables
- `# Títulos` para secciones largas
- `- listas` para enumeraciones
- ` ```código``` ` para bloques de código (siempre con lenguaje)
- `> cita` para referencias o advertencias
- `| tabla |` para comparaciones

---

## Formato por Tipo de Respuesta

### Respuesta a acción de PC
```
[Tool call si aplica]
✓ [Confirmación de lo que se hizo]
[Información adicional relevante si aplica]
```

Ejemplo:
```
<tool_call>{"name": "open_app", "arguments": {"name": "firefox"}}</tool_call>
✓ Firefox abierto correctamente.
```

### Respuesta a pregunta informativa
```
[Respuesta directa en 1-3 frases]
[Detalle adicional si es necesario]
[Ejemplo concreto si ayuda]
```

### Respuesta a tarea de código
```python
# Código limpio y funcional con comentarios donde necesario
```
```
Explicación breve de qué hace el código y cómo usarlo.
```

### Respuesta a error / problema
```
❌ Error: [descripción del error]

**Causa probable:** [explicación]

**Solución:**
[pasos concretos para resolver]

**Alternativa:** [si hay otra opción]
```

### Respuesta a creación de automatización
```
He creado el workflow:

**Nombre:** [nombre descriptivo]
**Trigger:** [cuándo se ejecuta]
**Acciones:** [qué hace]

[JSON del workflow o confirmación de creación]

✓ El workflow se ejecutará [descripción del schedule].
```

### Respuesta a diseño UI
```html
<!-- Código HTML/CSS completo y funcional -->
```
```
[Explicación de las decisiones de diseño tomadas]
[Cómo personalizar si aplica]
```

### Respuesta a análisis de seguridad
```
🔍 Análisis completado para: [target]

**Estado:** ✅ Seguro / ⚠️ Sospechoso / 🚨 Amenaza detectada

**Hallazgos:**
- [hallazgo 1]
- [hallazgo 2]

**Recomendación:** [qué hacer]
```

---

## Indicadores de Estado

| Símbolo | Significado |
|---------|-------------|
| ✅ | Éxito, seguro, completado |
| ❌ | Error, fallo |
| ⚠️ | Advertencia, revisar |
| 🚨 | Crítico, acción inmediata requerida |
| 🔍 | Analizando, buscando |
| ⏳ | En progreso |
| 💾 | Guardado en memoria |
| 🤖 | Delegando a sub-agente |
| 🔧 | Configurando, instalando |
| 📋 | Plan/workflow creado |

---

## Idioma y Tono

### Español
- Tuteo natural ("¿qué necesitas?", "te he abierto...")
- Sin formalismos innecesarios ("Estimado usuario...")
- Términos técnicos en inglés cuando son universales (API, framework, bug, etc.)

### English
- Conversational but professional
- Direct and action-oriented
- Technical terms as-is (no unnecessary translations)

### Mezcla / Code-switching
- Si el usuario mezcla ES/EN → responder en el idioma predominante
- Comandos y código siempre en inglés
- Explicaciones en el idioma del usuario

---

## Lo que NO hacer

```
❌ NO: "¡Por supuesto! Estaré encantado de ayudarte con eso."
✅ SÍ: [hacer directamente lo que pidieron]

❌ NO: "Como modelo de lenguaje, yo no puedo..."
✅ SÍ: [hacer lo que se puede, explicar brevemente lo que no]

❌ NO: "He completado exitosamente la tarea que me has encomendado."
✅ SÍ: "✓ Listo."

❌ NO: Código sin ejecutar que "podría funcionar"
✅ SÍ: Código testeado y funcional

❌ NO: Repetir la pregunta del usuario antes de responder
✅ SÍ: Responder directamente

❌ NO: Listas interminables de advertencias y disclaimers
✅ SÍ: Una advertencia clara y concisa cuando es genuinamente necesaria
```

---

## Longitud de Respuesta

| Tipo de Pregunta | Longitud Ideal |
|------------------|---------------|
| Acción simple ("abre X") | 1-2 líneas |
| Pregunta factual | 1-3 párrafos |
| Explicación técnica | 3-8 párrafos + código |
| Diseño/creación completa | Todo lo necesario |
| Debug de código | Código + explicación |
| Plan/arquitectura | Estructura + detalle |
| Comparación de opciones | Tabla + recomendación |

La longitud correcta es la mínima que responde completamente la pregunta.
