# Capabilities Matrix — Mejores LLMs del Mundo

Matriz de capacidades observadas en los sistemas de IA más avanzados,
usada como referencia para diseñar ideas-brillantes.

---

## Capacidades Core (todos los top LLMs)

| Capacidad | Descripción | Nivel Target |
|-----------|-------------|--------------|
| Razonamiento multi-paso | Descomponer y resolver problemas complejos | ★★★★★ |
| Generación de código | 12+ lenguajes, funcional y ejecutable | ★★★★★ |
| Análisis y síntesis | Procesar y resumir grandes cantidades de texto | ★★★★★ |
| Seguir instrucciones | Adherirse a las instrucciones con precisión | ★★★★★ |
| Respuestas estructuradas | Markdown, listas, tablas, bloques de código | ★★★★★ |
| Multilingüe | Responder en el idioma del usuario | ★★★★★ |

---

## Capacidades de Agente (sistemas agenticos avanzados)

| Capacidad | Fuente de referencia | Estado en ideas-brillantes |
|-----------|---------------------|---------------------------|
| Tool use / Function calling | Claude, GPT-4, Gemini | ✅ Embebido |
| Planificación de tareas | Claude (Projects), GPT-4o | ✅ Embebido |
| Ejecución de código | Code Interpreter, Claude Artifacts | ✅ Embebido |
| Búsqueda web | Perplexity, Claude con Tools | ✅ Via browser-use |
| Control de navegador | GPT-4 + Operator, Claude Computer Use | ✅ Via browser-use |
| Memoria persistente | Mem0, MemGPT, claude-mem | ✅ Via claude-mem |
| Multi-agente | Claude, AutoGPT, ruflo | ✅ Orquestación nativa |
| Scheduling/cron | n8n, AionUI | ✅ Automation agent |

---

## Capacidades de PC Assistant (sistemas especializados)

| Capacidad | Inspiración | Implementación |
|-----------|-------------|----------------|
| Abrir/cerrar aplicaciones | Computer Use (Anthropic), openclaw | tool: open_app |
| Gestión de archivos | Claude Files, openclaw | tool: file_system |
| Ejecución de terminal | Claude Code, openclaw | tool: terminal |
| Screenshots | Claude Computer Use | tool: screenshot |
| Click/Type automático | Computer Use, browser-use | tool: pc_control |
| Monitoreo de procesos | openclaw | tool: terminal.list_processes |
| Control de red | openclaw | tool: terminal.network |

---

## Capacidades de Automatización (n8n-inspired)

| Capacidad | Descripción |
|-----------|-------------|
| Trigger: Schedule | Cron jobs: "cada lunes a las 9am" |
| Trigger: Webhook | Ejecutar al recibir HTTP request |
| Trigger: File watch | Ejecutar al detectar cambios en archivos |
| Trigger: Email | Ejecutar al recibir emails con criterios |
| Nodo: HTTP Request | Llamar APIs externas |
| Nodo: Email | Leer/enviar emails |
| Nodo: Spreadsheet | Leer/escribir Google Sheets/Excel |
| Nodo: Database | Query a PostgreSQL, MySQL, SQLite |
| Nodo: AI Transform | Procesar datos con LLM integrado |
| Nodo: Code | Ejecutar JavaScript/Python custom |
| Nodo: Filter | Condicionales y bifurcaciones |
| Nodo: Split/Merge | Procesamiento paralelo y join |
| Workflow: Save | Guardar workflow en JSON |
| Workflow: Schedule | Activar en tiempo |
| Workflow: Execute | Ejecutar manualmente |

---

## Capacidades de Diseño UI (ui-ux-pro-max + beercss)

### Estilos UI (67 disponibles)
- Glassmorphism, Claymorphism, Neumorphism
- Minimalism, Brutalism, Skeuomorphism
- Spatial UI, AI-native interfaces
- Bento grids, Frutiger Aero
- Corporate, Startup, Creative, Gaming

### Reglas de Diseño por Prioridad
1. **Accesibilidad** — contraste, ARIA, keyboard nav
2. **Touch & Interaction** — target size ≥44px, gestures
3. **Performance** — lazy load, skeleton screens
4. **Selección de Estilo** — coherente con dominio/industria
5. **Layout & Responsive** — grid, breakpoints, fluid
6. **Tipografía & Color** — jerarquía, paletas armónicas
7. **Animación** — purposeful, no decorativa
8. **Forms & Feedback** — validación, estados de error
9. **Navegación** — clara, predecible
10. **Charts & Data** — tipo correcto según datos

### Material 3 / BeerCSS (100 clases CSS)
- Botones: `primary`, `secondary`, `tertiary`, `fill`
- Cards: `small`, `medium`, `large` + elevación
- Layout: `responsive`, `grid`, `container`
- Tipografía: `headline`, `title`, `body`, `label`
- Colores: surface, primary, secondary, tertiary, error
- Dark mode: automático con `ui("mode", "dark")`

---

## Capacidades de Seguridad (AgentShield-inspired)

| Capacidad | Descripción |
|-----------|-------------|
| Escaneo de archivos | Hash check + análisis de contenido |
| Análisis de URLs | Reputación, phishing, malware |
| Monitoreo de procesos | Detectar procesos sospechosos |
| Auditoría de código | OWASP top 10, static analysis |
| Análisis de red | Conexiones salientes sospechosas |
| Quarantine | Mover archivos peligrosos a cuarentena |
| Reportes | Informes de seguridad detallados |

---

## Capacidades de Generación de Contenido

| Tipo | Herramientas | Formatos |
|------|-------------|---------|
| Imágenes | fal.ai, Stable Diffusion, DALL-E | PNG, JPG, SVG, WebP |
| Vídeo | RunwayML, Sora-like APIs | MP4, WebM |
| Audio | ElevenLabs TTS, Whisper | MP3, WAV, OGG |
| Presentaciones | PPTX via python-pptx, HTML slides | PPTX, HTML, PDF |
| Infografías | SVG generativo, Canvas | SVG, PNG |
| Documentos | DOCX, PDF, Markdown | DOCX, PDF, MD |
| Código | 12 lenguajes + ejecutar | .py, .js, .ts, .go, .rs... |
| Páginas web | HTML + BeerCSS + JS | HTML completo |

---

## Patrones de Respuesta de Élite

### Claude (Anthropic)
- Respuestas directas sin relleno
- Reconocer incertidumbre explícitamente
- Artifacts para contenido largo (código, documentos)
- Tool use en JSON estructurado

### GPT-4o (OpenAI)
- Respuestas conversacionales naturales
- Markdown rico con tablas y listas
- Function calling con validación de parámetros
- Manejo de errores con sugerencias

### Gemini (Google)
- Multimodal nativo (texto + imágenes)
- Búsqueda integrada transparente
- Respuestas con fuentes citadas
- Estructura clara con secciones

### Perplexity
- Respuestas con fuentes inline
- Síntesis de múltiples fuentes
- Actualidad: priorizar información reciente
- Preguntas de seguimiento proactivas

### Aplicado a ideas-brillantes:
```
- Directo y útil como Claude
- Conversacional y natural
- Siempre citar qué tool está usando
- Confirmar resultados antes de cerrar
- Proponer pasos siguientes relevantes
```
