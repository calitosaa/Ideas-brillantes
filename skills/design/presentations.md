---
name: presentations
description: Create professional presentations as PPTX (python-pptx) or HTML slides with animations
---

# Presentations — PPTX & HTML Slides

## PPTX via python-pptx
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import io

def create_presentation(title: str, slides_data: list, output_path: str):
    """
    slides_data = [
      {"type": "title", "title": "...", "subtitle": "..."},
      {"type": "content", "title": "...", "bullets": ["...", "..."]},
      {"type": "two_col", "title": "...", "left": "...", "right": "..."},
    ]
    """
    prs = Presentation()
    prs.slide_width  = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # Color scheme (Material 3 inspired)
    PRIMARY = RGBColor(0x67, 0x50, 0xA4)
    ON_PRIMARY = RGBColor(0xFF, 0xFF, 0xFF)
    SURFACE = RGBColor(0xFE, 0xF7, 0xFF)
    ON_SURFACE = RGBColor(0x1C, 0x1B, 0x1F)

    for slide_data in slides_data:
        stype = slide_data.get("type", "content")

        if stype == "title":
            layout = prs.slide_layouts[0]  # Title slide
            slide = prs.slides.add_slide(layout)
            slide.shapes.title.text = slide_data["title"]
            slide.placeholders[1].text = slide_data.get("subtitle", "")

            # Style title slide background
            bg = slide.background.fill
            bg.solid()
            bg.fore_color.rgb = PRIMARY

            # Style title text
            tf = slide.shapes.title.text_frame
            for para in tf.paragraphs:
                for run in para.runs:
                    run.font.color.rgb = ON_PRIMARY
                    run.font.size = Pt(44)
                    run.font.bold = True

        elif stype == "content":
            layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(layout)
            slide.shapes.title.text = slide_data["title"]

            body = slide.placeholders[1]
            tf = body.text_frame
            tf.clear()

            for i, bullet in enumerate(slide_data.get("bullets", [])):
                if i == 0:
                    tf.paragraphs[0].text = bullet
                else:
                    p = tf.add_paragraph()
                    p.text = bullet
                    p.level = 0

        elif stype == "two_col":
            layout = prs.slide_layouts[3]
            slide = prs.slides.add_slide(layout)
            slide.shapes.title.text = slide_data["title"]
            try:
                slide.placeholders[1].text = slide_data.get("left", "")
                slide.placeholders[2].text = slide_data.get("right", "")
            except Exception:
                pass

    prs.save(output_path)
    return output_path

# Usage example
slides = [
    {"type": "title", "title": "ideas-brillantes", "subtitle": "Tu asistente de IA para Linux"},
    {"type": "content", "title": "Capacidades", "bullets": [
        "Control del PC y automatización",
        "Generación de código en 12 lenguajes",
        "Diseño UI con Material 3",
        "Seguridad proactiva integrada",
    ]},
    {"type": "two_col", "title": "Comparación", "left": "Antes\n• Manual\n• Lento", "right": "Con ideas-brillantes\n• Automático\n• Instantáneo"},
]
create_presentation("Mi Presentación", slides, "output.pptx")
```

## HTML Slides (Reveal.js-style, no dependencies)
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Presentación</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', sans-serif; background: #1c1b1f; color: white; overflow: hidden; }
  .slides { width: 100vw; height: 100vh; }
  .slide { display: none; width: 100%; height: 100vh; padding: 60px 80px;
           flex-direction: column; justify-content: center; }
  .slide.active { display: flex; }
  .slide.title-slide { background: linear-gradient(135deg, #6750a4, #7d5260); }
  h1 { font-size: 3.5rem; margin-bottom: 1rem; }
  h2 { font-size: 2.5rem; margin-bottom: 1.5rem; color: #e8def8; }
  p, li { font-size: 1.4rem; line-height: 1.8; opacity: 0.9; }
  ul { list-style: none; }
  ul li::before { content: "→ "; color: #b69df8; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; }
  .col { background: rgba(255,255,255,0.1); border-radius: 16px; padding: 2rem; }
  .progress { position: fixed; bottom: 0; left: 0; height: 4px; background: #6750a4;
              transition: width 0.3s; }
  .nav { position: fixed; bottom: 20px; right: 20px; display: flex; gap: 1rem; }
  .nav button { background: rgba(255,255,255,0.2); border: none; color: white;
                padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 1rem; }
  .nav button:hover { background: rgba(255,255,255,0.3); }
  .slide-num { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
               opacity: 0.6; font-size: 0.9rem; }
</style>
</head>
<body>
<div class="slides">
  <!-- Slide 1: Title -->
  <div class="slide title-slide active">
    <h1>Título Principal</h1>
    <p>Subtítulo explicativo</p>
    <p style="margin-top:2rem; opacity:0.7">Autor · Fecha</p>
  </div>

  <!-- Slide 2: Bullets -->
  <div class="slide">
    <h2>Puntos Clave</h2>
    <ul>
      <li>Primer punto importante</li>
      <li>Segundo punto con más detalle</li>
      <li>Tercer punto de la lista</li>
      <li>Conclusión o llamada a la acción</li>
    </ul>
  </div>

  <!-- Slide 3: Two columns -->
  <div class="slide">
    <h2>Comparación</h2>
    <div class="two-col">
      <div class="col"><h3>Antes</h3><ul><li>Manual</li><li>Lento</li></ul></div>
      <div class="col"><h3>Después</h3><ul><li>Automático</li><li>Instantáneo</li></ul></div>
    </div>
  </div>

  <!-- Slide 4: Closing -->
  <div class="slide title-slide">
    <h1>¿Preguntas?</h1>
    <p>contacto@ejemplo.com</p>
  </div>
</div>

<div class="progress" id="progress"></div>
<div class="slide-num" id="slideNum">1 / 4</div>
<div class="nav">
  <button onclick="changeSlide(-1)">← Anterior</button>
  <button onclick="changeSlide(1)">Siguiente →</button>
</div>

<script>
let current = 0;
const slides = document.querySelectorAll('.slide');
const total = slides.length;

function changeSlide(dir) {
  slides[current].classList.remove('active');
  current = Math.max(0, Math.min(total - 1, current + dir));
  slides[current].classList.add('active');
  document.getElementById('progress').style.width = ((current + 1) / total * 100) + '%';
  document.getElementById('slideNum').textContent = (current + 1) + ' / ' + total;
}

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'Space') changeSlide(1);
  if (e.key === 'ArrowLeft') changeSlide(-1);
});

// Init progress
document.getElementById('progress').style.width = (1 / total * 100) + '%';
</script>
</body>
</html>
```

## Chart.js Integration
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<canvas id="myChart" width="600" height="300"></canvas>
<script>
new Chart(document.getElementById('myChart'), {
  type: 'bar',
  data: {
    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May'],
    datasets: [{
      label: 'Ventas',
      data: [12, 19, 8, 15, 22],
      backgroundColor: '#6750a4',
      borderRadius: 8,
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { labels: { color: 'white' } } },
    scales: {
      x: { ticks: { color: '#cac4d0' }, grid: { color: '#49454f' } },
      y: { ticks: { color: '#cac4d0' }, grid: { color: '#49454f' } }
    }
  }
});
</script>
```
