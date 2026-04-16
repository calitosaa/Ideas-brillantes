---
name: research
description: Deep research, multi-source synthesis and knowledge report generation using web search and notebooklm-py
---

# Research & Knowledge Synthesis

## Research Process
```
1. DEFINE: Qué se necesita saber exactamente
2. SEARCH: Buscar desde múltiples ángulos y fuentes
3. EVALUATE: Calidad y credibilidad de fuentes
4. SYNTHESIZE: Combinar en visión coherente
5. CITE: Documentar todas las fuentes
6. REPORT: Presentar en formato útil
```

## Tool Call Pattern
```xml
<!-- 1. Initial broad search -->
<tool_call>{"name": "web_search", "arguments": {"query": "topic site:reliable-source.com", "num_results": 10}}</tool_call>

<!-- 2. Deep dive into specific source -->
<tool_call>{"name": "fetch_url", "arguments": {"url": "https://...", "extract_mode": "article"}}</tool_call>

<!-- 3. Compare multiple sources -->
<tool_call>{"name": "extract_content", "arguments": {"url": "https://...", "selectors": ["article", "main"]}}</tool_call>

<!-- 4. Synthesize findings -->
<tool_call>{"name": "summarize_content", "arguments": {"content": "...", "format": "bullet_points", "length": "comprehensive"}}</tool_call>
```

## Source Quality Evaluation
```
Alta calidad:
  ✅ Publicaciones académicas (.edu, journals)
  ✅ Fuentes oficiales (.gov, organizaciones reconocidas)
  ✅ Medios de referencia con políticas editoriales
  ✅ Documentación técnica oficial

Media calidad:
  ⚠️ Blogs especializados (verificar autor)
  ⚠️ Wikipedia (útil para overview, verificar fuentes)
  ⚠️ Foros técnicos (StackOverflow, Reddit)

Baja calidad / verificar siempre:
  ⛔ Fuentes sin autor identificado
  ⛔ Contenido sin fecha o muy desactualizado
  ⛔ Sitios con interés comercial obvio en el tema
```

## NotebookLM-py Integration
```python
# Para investigación profunda con múltiples documentos
from notebooklm import NotebookLM

nlm = NotebookLM()

# Crear notebook de investigación
notebook = nlm.create_notebook("Investigación: [Tema]")

# Añadir fuentes (URLs, PDFs, YouTube)
notebook.add_source("https://paper.pdf")
notebook.add_source("https://article-url.com")
notebook.add_source("https://youtube.com/watch?v=...")

# Consultar las fuentes combinadas
answer = notebook.ask("¿Cuáles son las principales conclusiones?")
summary = notebook.generate_summary()

# Exportar materiales de estudio
flashcards = notebook.generate_flashcards()
quiz = notebook.generate_quiz()
mind_map = notebook.get_mind_map_json()
```

## Research Report Template
```markdown
# Investigación: [Tema]
**Fecha**: [fecha]  **Fuentes**: [n]  **Palabras**: [n]

## Resumen Ejecutivo
[2-3 párrafos con hallazgos clave]

## Contexto y Antecedentes
[Qué se sabía antes, por qué es relevante]

## Hallazgos Principales
### [Área 1]
[Análisis con datos y citas]

### [Área 2]
[Análisis con datos y citas]

## Análisis Comparativo
| Aspecto | Opción A | Opción B |
|---------|---------|---------|
| ... | ... | ... |

## Conclusiones
[Síntesis y recomendaciones]

## Fuentes
1. [Título] — [URL] — [Fecha acceso]
2. ...
```

## Search Strategy Patterns

**Búsqueda técnica**:
```
"[tecnología] tutorial site:docs.official.com"
"[error message]" filetype:md OR filetype:rst
"[librería] best practices 2024"
```

**Búsqueda comparativa**:
```
"[A] vs [B] comparison 2024"
"[A] OR [B] benchmark performance"
"alternatives to [X]"
```

**Búsqueda de noticias/actualidad**:
```
"[tema] after:2024-01-01"
"[empresa] announcement 2025"
site:techcrunch.com OR site:wired.com "[tema]"
```
