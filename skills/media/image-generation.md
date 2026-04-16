---
name: image-generation
description: Generate images using AI with expert prompt engineering for any style and use case
---

# Image Generation — AI-Powered

## Overview
Generate images for any purpose using AI backends. Apply expert prompt engineering to get exactly the right result.

## Tool Call
```xml
<tool_call>{"name": "generate_image", "arguments": {
  "prompt": "A minimalist product mockup of a smartphone app, clean white background, Material Design 3 UI, professional photography, 4K",
  "style": "photorealistic",
  "size": "1024x1024",
  "output_path": "~/Pictures/generated/output.png"
}}</tool_call>
```

## Prompt Engineering Guide

### Structure of a Good Prompt
```
[SUJETO PRINCIPAL], [ACCIÓN/ESTADO], [ESTILO], [ILUMINACIÓN], [COMPOSICIÓN], [CALIDAD]

Ejemplo:
"A modern Linux desktop workspace, clean and organized, dark glassmorphism UI,
soft blue ambient lighting, wide-angle shot, 4K ultra-detailed"
```

### Style Keywords by Category

**Fotorrealista:**
`photorealistic, hyperrealistic, 8K, RAW photo, DSLR, professional photography, sharp focus, bokeh`

**Ilustración:**
`digital illustration, vector art, flat design, 2D, clean lines, vibrant colors, Adobe Illustrator style`

**UI/App Mockup:**
`app mockup, UI screenshot, Material Design 3, clean interface, white background, product design`

**Conceptual/Arte:**
`conceptual art, surrealist, abstract, oil painting, watercolor, sketch, pencil drawing`

**Marketing:**
`marketing banner, advertisement, professional, brand colors, commercial photography`

**Iconos/Logos:**
`icon design, logo, simple, scalable, flat vector, geometric, minimal`

### Lighting Keywords
```
Natural: natural light, golden hour, soft daylight, overcast sky
Studio: studio lighting, three-point lighting, product photography
Dramatic: cinematic lighting, noir, chiaroscuro, backlit
Ambient: neon lights, cyberpunk, warm ambient glow
```

### Common Use Cases

**Para presentaciones:**
```
"Professional business infographic about [topic], clean flat design,
blue and purple color scheme, data visualization, icons, white background"
```

**Para UI/App:**
```
"Mobile app screenshot showing [feature], Material Design 3, dark theme,
clean typography, realistic device mockup, iPhone 15 Pro frame"
```

**Para redes sociales:**
```
"Social media post for [brand], [product], vibrant colors, eye-catching,
[platform] format, modern design, [brand colors]"
```

**Para documentos técnicos:**
```
"Technical diagram showing [architecture/process], clean lines,
isometric view, flat design, blue and grey, white background, professional"
```

### Negative Prompts (What to Avoid)
```
Calidad: low quality, blurry, pixelated, artifacts, watermark, text, signature
Anatomía: deformed, extra fingers, bad hands, malformed, ugly
Composición: overexposed, underexposed, bad framing, cut off
```

## Available Backends
| Backend | Strengths | Notes |
|---------|-----------|-------|
| Stable Diffusion (local) | Control total, sin censura | Requiere GPU |
| fal.ai API | Rápido, alta calidad | Requiere API key |
| DALL-E 3 API | Excelente comprensión de prompts | OpenAI API key |
| Midjourney (via Discord bot) | Arte de alta calidad | Manual |

## Batch Generation
```python
# Generar múltiples variaciones
prompts = [
    "Version A: minimalist design...",
    "Version B: bold colorful...",
    "Version C: dark corporate...",
]
for i, prompt in enumerate(prompts):
    generate_image(prompt, f"~/output/variant_{i+1}.png")
```
