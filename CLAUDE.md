# Ideas-Brillantes — Claude Code Guide

## Descripción del Proyecto

Este repositorio contiene la configuración, skills, training data y scripts para crear
**ideas-brillantes**, un LLM derivado de GLM-5-1 especializado como asistente de SO Linux.

## Estructura Clave

- `model/` — Sistema prompt + Modelfile Ollama + configuración
- `training/` — Fine-tuning scripts + dataset JSONL (~12k ejemplos)
- `skills/` — Definiciones de skills por categoría (50+ archivos .md)
- `agents/` — Sub-agentes especializados (10 archivos)
- `tools/schemas/` — JSON Schema de herramientas (10 archivos)
- `tools/mcp/` — Configuración MCP servers
- `workflows/` — Templates automatización n8n-style
- `knowledge/` — Patrones inteligencia extraídos de referencia pública
- `scripts/` — Setup, instalación, exportación

## Comandos Habituales

```bash
# Crear modelo en Ollama
ollama create ideas-brillantes -f model/Modelfile

# Probar modelo
ollama run ideas-brillantes "Hola, ¿qué puedes hacer?"

# Preparar dataset
python training/prepare_dataset.py

# Validar dataset
python training/validate_dataset.py

# Fine-tuning
python training/finetune.py

# Exportar GGUF
./scripts/export_to_gguf.sh
```

## Convenciones

### Skills
- Formato: Markdown en `skills/[categoria]/[nombre].md`
- Las skills describen comportamientos NATIVOS del modelo, no comandos
- Cada skill tiene: descripción, cuándo aplica, comportamiento esperado, ejemplos

### Training Data
- Formato: JSONL en `training/dataset/[categoria].jsonl`
- Cada línea: `{"messages": [{"role": "user", ...}, {"role": "assistant", ...}]}`
- Formato ChatML compatible con GLM-5-1

### Tool Schemas
- Formato: JSON Schema en `tools/schemas/[nombre].json`
- Define exactamente qué puede hacer el modelo y cómo llamar cada tool

### Agents
- Formato: Markdown en `agents/[nombre].md`
- Define comportamiento, especialización, tools disponibles, cuándo delegar

## Notas de Arquitectura

El modelo opera en 3 capas:
1. **Pesos fine-tuned** — conocimiento embebido via LoRA sobre GLM-5-1
2. **Sistema prompt** — identidad, capacidades, idioma (Modelfile Ollama)
3. **Tool schemas** — definición de acciones disponibles en runtime

Las skills NO son comandos de activación. Son conocimiento embebido en el modelo
que define cómo comportarse en diferentes situaciones.

## Idioma

- Modelo bilingüe ES/EN
- Responde en el idioma del usuario automáticamente
- Documentación técnica en ambos idiomas donde aplica
