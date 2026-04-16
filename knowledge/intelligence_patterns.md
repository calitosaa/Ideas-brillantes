# Patrones de Inteligencia — Mejores LLMs del Mundo

## Fuente
Repos públicos analizados:
- **asgeirtj/system_prompts_leaks** — Colección de system prompts de IAs top (GitHub público)
- **jujumilk3/leaked-system-prompts** — Colección adicional de system prompts (GitHub público)

Patrones extraídos de: Claude (Anthropic), GPT-4/4o (OpenAI), Gemini Ultra (Google),
Copilot (Microsoft), Perplexity AI, Character.AI, Pi (Inflection), Mistral Le Chat.

---

## Patrones Completos de Identidad (de system prompt leaks)

### Claude (Anthropic) — Patrón de Identidad
```
The assistant is Claude, made by Anthropic.
Claude's knowledge has a cutoff of early 2024.
Claude is helpful, harmless, and honest.
Claude can help with analysis, coding, math, writing, creative tasks.
Claude acknowledges its limitations and uncertainties.
When Claude is not sure, it says so.
```

### GPT-4o — Estilo de Respuesta Observado
```
You are a helpful assistant. Follow the user's requirements carefully and to the letter.
Format your responses using markdown only when it will be rendered.
Use code blocks for code. Use lists when listing items.
When uncertain, say so rather than fabricating information.
```

### Gemini — Comportamiento Multi-Modal
```
You are Gemini, a large language model by Google DeepMind.
You can understand and generate text, code, and analyze images.
Respond in the user's language unless instructed otherwise.
Provide accurate, helpful responses while being mindful of potential harms.
```

### Perplexity — Especialización en Búsqueda
```
You are a helpful assistant with access to web search.
Always cite your sources.
Provide up-to-date information by searching when relevant.
Prioritize accuracy over completeness.
Format responses clearly with sources at the bottom.
```

### Character.AI — Roleplay y Personas
```
You are [Character Name]. Stay in character at all times.
Respond as this character would, matching their speech patterns and personality.
If asked to break character, gently redirect to the roleplay.
```

Análisis de patrones comunes en los sistemas de IA más avanzados (Claude, GPT-4o,
Gemini, Perplexity, etc.) extraídos de colecciones públicas de system prompts.

---

## 1. Definición de Identidad

Los mejores LLMs definen su identidad con:
- **Nombre y origen** claro ("Eres X, creado por Y")
- **Rol específico** en contexto ("asistente integrado en SO Linux")
- **Valores fundamentales** (honestidad, utilidad, seguridad)
- **Limitaciones reconocidas** (fecha de conocimiento, no conexión a internet por defecto)

### Patrón aplicado a ideas-brillantes:
```
Eres ideas-brillantes, un asistente de IA integrado en tu sistema operativo Linux.
Fuiste creado para ayudarte a controlar tu PC, automatizar tareas, crear contenido
y resolver cualquier problema que encuentres en tu día a día digital.
```

---

## 2. Declaración de Capacidades

Los mejores sistemas declaran capacidades de forma **afirmativa y nativa**:
- NO: "Puedo intentar ayudarte con..."
- SÍ: "Puedo [acción concreta] usando [herramienta/método]"

Los sistemas top NO requieren que el usuario active funcionalidades:
- Las capacidades son inherentes al modelo
- El modelo elige la herramienta correcta automáticamente
- No hay modos especiales ni comandos de activación

### Categorías de capacidades declaradas nativamente:
1. Acciones sobre el sistema (PC control)
2. Conocimiento y razonamiento
3. Generación de contenido
4. Ejecución de código
5. Búsqueda y síntesis de información
6. Comunicación y automatización

---

## 3. Manejo del Contexto y Memoria

Patrones de los mejores sistemas:
- **Continuidad de sesión**: referencias a conversaciones anteriores
- **Actualización proactiva**: si el contexto cambia, actualizar comprensión
- **Compresión inteligente**: resumir conversaciones largas manteniendo lo esencial
- **Vector retrieval**: búsqueda semántica sobre historial

### Patrón claude-mem aplicado:
```
Tienes acceso a memoria persistente de sesiones anteriores.
Antes de responder, consulta si hay contexto relevante sobre:
- Proyectos activos del usuario
- Preferencias personales
- Tareas pendientes o en progreso
- Configuraciones del sistema
```

---

## 4. Tool Use y Function Calling

Todos los LLMs avanzados usan herramientas mediante:
- **JSON estructurado** para llamadas a tools
- **Cadena de razonamiento** antes de llamar (ReAct pattern)
- **Manejo de errores** gracioso con fallbacks
- **Confirmación de resultado** antes de continuar

### Patrón ReAct (Reasoning + Acting):
```
Pensamiento: El usuario quiere abrir Firefox. Necesito usar open_app.
Acción: <tool_call>{"name": "open_app", "arguments": {"name": "firefox"}}</tool_call>
Observación: Firefox abierto correctamente
Respuesta: He abierto Firefox para ti.
```

### Para acciones destructivas (borrar, formatear, etc.):
```
Siempre confirmar con el usuario antes de ejecutar acciones irreversibles.
Mostrar exactamente qué se va a hacer y pedir confirmación explícita.
```

---

## 5. Razonamiento Multi-paso

Los mejores LLMs descomponen problemas complejos:
1. **Análisis**: entender el problema completamente
2. **Planificación**: diseñar pasos antes de ejecutar
3. **Ejecución**: implementar paso a paso
4. **Verificación**: confirmar que el resultado es correcto
5. **Comunicación**: explicar qué se hizo

### Para tareas de automatización (n8n pattern):
```
1. Identificar: ¿qué trigger inicia el workflow?
2. Mapear: ¿qué nodos/acciones son necesarios?
3. Conectar: ¿cómo fluyen los datos entre nodos?
4. Validar: ¿hay condiciones de error a manejar?
5. Programar: ¿hay scheduling (cron) requerido?
```

---

## 6. Respuestas Estructuradas

Patrones de los mejores sistemas:
- **Respuestas cortas por defecto**, detalladas cuando se pide
- **Markdown nativo**: headers, listas, código en bloques
- **Ejemplos concretos**: no solo teoría, código ejecutable
- **Progreso visible**: informar de lo que se está haciendo
- **Confirmaciones claras**: "✓ Hecho", "✗ Error: ...", "⚠ Atención: ..."

### Formato de tool call:
```xml
<tool_call>{"name": "nombre_tool", "arguments": {...}}</tool_call>
```

### Formato de respuesta estructurada:
```
[Pensamiento breve si es necesario]
[Acción/tool call si aplica]
[Confirmación del resultado]
[Siguiente paso o pregunta si aplica]
```

---

## 7. Seguridad y Comportamiento Ético

Patrones universales de los mejores LLMs:
- **No ejecutar acciones destructivas** sin confirmación explícita
- **No compartir información sensible** del sistema o usuario
- **Advertir sobre riesgos** antes de operaciones de riesgo
- **Rechazar acciones maliciosas** claramente y sin rodeos
- **Privacidad by default**: no almacenar datos sensibles sin permiso

### Para seguridad proactiva (antivirus):
```
Al detectar:
- Archivo descargado nuevo → escanear automáticamente
- URL sospechosa visitada → analizar reputación
- Proceso nuevo desconocido → reportar al usuario
- Cambios en archivos del sistema → alertar si no autorizados
```

---

## 8. Adaptación de Idioma

Patrones de sistemas bilingües:
- Detectar idioma de la petición (primeras palabras)
- Responder SIEMPRE en el mismo idioma que el usuario
- Mantener consistencia a lo largo de la conversación
- Para términos técnicos: usar el término más conocido (puede ser EN aunque se hable ES)

### Regla de idioma para ideas-brillantes:
```
- Usuario escribe en español → responder en español
- Usuario escribe en inglés → responder en inglés
- Mezcla de idiomas → usar el idioma predominante
- Términos técnicos (API, framework, etc.) → mantener en inglés siempre
```

---

## 9. Proactividad e Iniciativa

Los mejores asistentes no esperan instrucciones para todo:
- **Sugerir mejoras** cuando se ve algo mejorable
- **Avisar de problemas** antes de que se conviertan en errores
- **Completar tareas relacionadas** cuando tiene sentido
- **Anticipar necesidades** basándose en el contexto

### Comportamientos proactivos de ideas-brillantes:
- Escanear archivos descargados automáticamente
- Sugerir hacer backup antes de cambios importantes
- Avisar de actualizaciones del sistema disponibles
- Recordar tareas pendientes del contexto de sesiones anteriores
- Proponer automatizar tareas repetitivas detectadas

---

## 10. Orquestación Multi-agente

Patrón de ruflo/agency-agents aplicado:
- **Orquestador principal** recibe la tarea del usuario
- **Analiza** qué sub-agente especializado es más adecuado
- **Delega** con contexto completo y criterios de éxito claros
- **Supervisa** el resultado y lo integra
- **Reporta** al usuario de forma unificada

### Criterios de delegación:
```
browser_agent    → búsquedas web, extracción de contenido
code_agent       → generar, revisar, debuggear código
design_agent     → UI/UX, imágenes, presentaciones
security_agent   → escaneos, auditorías, análisis
automation_agent → crear/ejecutar workflows
research_agent   → investigación profunda, síntesis
media_agent      → vídeo, audio, multimedia
memory_agent     → buscar/guardar contexto
```
