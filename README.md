# Ideas-Brillantes LLM

Un nuevo modelo de lenguaje propio construido sobre **GLM-5-1** como base, con más de **5.000 skills, agentes, workflows y patrones de inteligencia** embebidos nativamente mediante fine-tuning.

## ¿Qué es esto?

`ideas-brillantes` es un LLM especializado como **asistente inteligente de sistema operativo Linux**, capaz de:

- **Controlar el PC** — abrir aplicaciones, gestionar archivos, ejecutar comandos, monitorear procesos
- **Navegar la web autónomamente** — buscar, leer, extraer y sintetizar información de internet
- **Crear automatizaciones** — workflows programados estilo n8n (cron, triggers, pipelines)
- **Generar contenido multimedia** — imágenes, vídeos, audio, presentaciones, infografías
- **Escribir y revisar código** — 12 lenguajes, TDD, debugging sistemático, arquitectura
- **Diseñar interfaces** — Material 3, BeerCSS, UI/UX con 161 reglas de diseño profesional
- **Seguridad proactiva** — escaneo automático de archivos descargados y URLs visitadas
- **Memoria persistente** — contexto mantenido entre sesiones via vector database
- **Orquestar sub-agentes** — delegar tareas a especialistas automáticamente

## Capacidades Nativas (no requieren activación)

Todas las capacidades están embebidas en el modelo mediante fine-tuning. No hay comandos que activar:

| Área | Capacidades |
|------|-------------|
| PC Control | Abrir/cerrar apps, gestionar archivos, terminal, procesos, red |
| Web | Buscar, navegar, extraer datos, formularios, screenshots |
| Automatización | Crear/ejecutar workflows, cron jobs, triggers de eventos |
| Código | Generar, revisar, debuggear, testear (Python, JS, Go, Rust, Java...) |
| Diseño UI | Material 3, BeerCSS, 67 estilos, 161 reglas, 161 paletas de color |
| Multimedia | Imágenes, vídeos, audio TTS, presentaciones PPTX, infografías |
| Documentos | DOCX, PDF, Excel, Markdown, HTML |
| Investigación | Búsqueda web profunda, síntesis, notebooklm-py |
| Email/Comm | Gmail, Slack, Teams, Discord, calendario |
| Seguridad | Antivirus en tiempo real, análisis de URLs, auditorías de código |
| Memoria | SQLite + Chroma vector DB, contexto entre sesiones |

## Arquitectura del Modelo

```
┌─────────────────────────────────────────────────┐
│           ideas-brillantes LLM                  │
│                                                 │
│  Base: GLM-5-1 (weights originales)             │
│  + LoRA adapters (fine-tuning ~12k pares)       │
│  + Sistema prompt maestro (Modelfile Ollama)    │
│                                                 │
│  Conocimiento embebido:                         │
│  • 1,410 skills (antigravity-awesome-skills)    │
│  • 1,184+ skills (VoltAgent awesome-agent)      │
│  • 200+ skills + 313 MCP tools (ruflo)          │
│  • 14 skills metodológicos (superpowers)        │
│  • 183 skills + 48 subagents (everything-claude)│
│  • 144 agentes especializados (agency-agents)   │
│  • 500+ integraciones (ComposioHQ)              │
│  • 7 skills diseño (ui-ux-pro-max-skill)        │
│  • Material 3 completo (beercss + M3 catalog)   │
│  • 4,343 workflow templates (n8n-workflows)     │
│  • Patrones inteligencia (system prompt leaks)  │
└─────────────────────────────────────────────────┘
```

## Estructura del Repositorio

```
Ideas-brillantes/
├── model/           # Sistema prompt, Modelfile Ollama, config
├── training/        # Scripts fine-tuning + dataset JSONL
│   └── dataset/     # ~12,000 pares instrucción→respuesta
├── skills/          # Definición de todas las skills por categoría
│   ├── core/        # PC control, browser, memory, automation
│   ├── design/      # UI/UX, Material3, infografías, web
│   ├── engineering/ # Código, TDD, arquitectura, DevOps
│   ├── productivity/# Documentos, investigación, email
│   ├── media/       # Imagen, vídeo, audio, grabación
│   ├── integrations/# GitHub, Google, Slack, 500+ apps
│   └── security/    # Antivirus, web safety, auditorías
├── agents/          # Definición de sub-agentes especializados
├── tools/           # Schemas JSON de tools + MCP configs
│   ├── schemas/     # JSON Schema de cada herramienta
│   └── mcp/         # Configuración MCP servers
├── workflows/       # Templates automatización n8n-style
├── knowledge/       # Patrones de inteligencia extraídos
└── scripts/         # Setup, instalación, exportación
```

## Uso Rápido

### Con Ollama (recomendado)

```bash
# 1. Clonar repo
git clone https://github.com/calitosaa/ideas-brillantes
cd ideas-brillantes

# 2. Setup completo
./scripts/setup.sh

# 3. Crear modelo
ollama create ideas-brillantes -f model/Modelfile

# 4. Ejecutar
ollama run ideas-brillantes
```

### Fine-tuning (crear modelo propio)

```bash
# Instalar dependencias de entrenamiento
./scripts/install_training_deps.sh

# Preparar dataset
python training/prepare_dataset.py

# Entrenar (requiere GPU con ≥16GB VRAM)
python training/finetune.py

# Exportar a GGUF
./scripts/export_to_gguf.sh
```

## Requisitos

### Para usar el modelo (Ollama)
- Linux (x86_64)
- RAM: ≥16GB
- Ollama instalado

### Para fine-tuning
- GPU NVIDIA con ≥16GB VRAM (RTX 3090/4090, A100)
- CUDA 12.x
- Python 3.11+
- ~50GB espacio en disco

## Fuentes de Conocimiento

| Repo | Contribución |
|------|-------------|
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1,184+ skills enterprise |
| [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | 1,410 skills en catalog.json |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | 200+ skills, 313 MCP tools |
| [obra/superpowers](https://github.com/obra/superpowers) | 14 skills metodológicos |
| [everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 183 skills + AgentShield |
| [agency-agents](https://github.com/msitarzewski/agency-agents) | 144 agentes especializados |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 500+ integraciones |
| [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 7 skills diseño, 161 reglas |
| [beercss](https://github.com/beercss/beercss) | Material 3 CSS framework completo |
| [browser-use](https://github.com/browser-use/browser-use) | Agente web autónomo |
| [claude-mem](https://github.com/thedotmack/claude-mem) | Memoria persistente SQLite+Chroma |
| [n8n-workflows](https://github.com/Zie619/n8n-workflows) | 4,343 workflow templates |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | Research programático |
| [system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks) | Patrones de inteligencia LLM |
| [leaked-system-prompts](https://github.com/jujumilk3/leaked-system-prompts) | Patrones de inteligencia LLM |

## Licencia

MIT
