# Banner & Ad Design Skill

## Fuente
ui-ux-pro-max-skill (banner-design category) — 12+ art styles, plataformas, dimensiones

---

## Dimensiones por Plataforma

### Redes Sociales
```
Instagram Post:      1080×1080px  (1:1)
Instagram Story:     1080×1920px  (9:16)
Instagram Reels:     1080×1920px  (9:16)
Facebook Post:       1200×630px   (1.91:1)
Facebook Cover:      851×315px
Twitter/X Header:    1500×500px
Twitter/X Post:      1200×675px   (16:9)
LinkedIn Post:       1200×627px
LinkedIn Cover:      1584×396px
YouTube Thumbnail:   1280×720px   (16:9)
YouTube Channel Art: 2560×1440px
TikTok Video:        1080×1920px  (9:16)
Pinterest Pin:       1000×1500px  (2:3)
```

### Publicidad Digital
```
Leaderboard:         728×90px
Medium Rectangle:    300×250px   (más universal)
Large Rectangle:     336×280px
Wide Skyscraper:     160×600px
Half Page:           300×600px
Billboard:           970×250px
Mobile Banner:       320×50px
Mobile Interstitial: 320×480px
```

### Email Marketing
```
Email Header:        600×200px
Email Banner:        600×150px
HTML email width:    600px (max recomendado)
```

---

## 12+ Estilos Artísticos

### 1. Flat Design
- Colores sólidos sin sombras ni gradientes
- Formas geométricas simples
- Tipografía sans-serif bold
- Ideal: tech, startups, apps
```css
background: #6366F1;
color: white;
border-radius: 8px;
/* Sin box-shadow, sin gradientes */
```

### 2. Gradient/Glassmorphism
- Degradados vivos (rosa→púrpura, azul→verde)
- `backdrop-filter: blur()` para glassmorphism
- Ideal: música, gaming, lifestyle
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Glass overlay */
background: rgba(255,255,255,0.1);
backdrop-filter: blur(20px);
border: 1px solid rgba(255,255,255,0.3);
```

### 3. Bold Typography
- Tipografía masiva como elemento visual
- Poco o ningún elemento gráfico adicional
- Alto contraste
- Ideal: marcas de moda, eventos, editorial
```css
font-size: 120px;
font-weight: 900;
text-transform: uppercase;
letter-spacing: -2px;
```

### 4. Retro/Vintage
- Colores desaturados, tonos sepia o pastel
- Tipografías con serif o script
- Texturas de papel/ruido
- Marcos y ornamentos decorativos
- Ideal: food, craft, hipster brands

### 5. Neón/Cyberpunk
- Fondo oscuro (negro o azul marino)
- Colores neón brillantes: rosa, verde, cian, amarillo
- `text-shadow` y `box-shadow` con color glow
- Ideal: gaming, música electrónica, tech
```css
background: #0D0D0D;
color: #00F5FF;
text-shadow: 0 0 20px #00F5FF, 0 0 40px #00F5FF;
box-shadow: 0 0 30px #FF006E;
```

### 6. Minimalista White Space
- Muchísimo espacio en blanco
- Un solo elemento visual focal
- Tipografía ligera y elegante
- Ideal: lujo, cosmética, arquitectura

### 7. 3D Illustration
- Elementos 3D renderizados o CSS 3D
- Profundidad y perspectiva
- Ideal: tech, SaaS, gaming
```css
transform: perspective(1000px) rotateY(-15deg);
transform-style: preserve-3d;
```

### 8. Handcraft/Organic
- Elementos dibujados a mano
- Formas irregulares, no perfectas
- Colores naturales (tierra, verde, ocre)
- Ideal: orgánico, artesanal, bienestar

### 9. Geometric Abstract
- Formas geométricas superpuestas
- Transparencias y blending modes
- Sin representación figurativa
- Ideal: corporate, consulting, fintech

### 10. Photo + Text Overlay
- Fotografía de impacto como fondo
- Overlay de color semi-transparente
- Texto en blanco contrastado
- Ideal: turismo, eventos, lifestyle
```css
.banner {
    background-image: url(photo.jpg);
    background-size: cover;
}
.overlay {
    background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.7) 100%);
}
```

### 11. Data Visualization
- Gráficos, números grandes, estadísticas
- Ideal: finanzas, tecnología, investigación

### 12. Emoji/Gen-Z
- Emojis como elementos visuales
- Colores saturados y contrastantes
- Tipografía casual, irregular
- Ideal: apps juveniles, social media

---

## Plantillas HTML para Banners

### Banner Social Media Universal
```html
<div style="
    width: 1080px; height: 1080px;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-family: 'Inter', sans-serif;
    position: relative; overflow: hidden;
">
    <!-- Background decoration -->
    <div style="
        position: absolute; top: -100px; right: -100px;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%);
        border-radius: 50%;
    "></div>
    
    <!-- Tag/category -->
    <span style="
        background: rgba(99,102,241,0.2);
        color: #A5B4FC; 
        padding: 8px 20px;
        border-radius: 100px;
        font-size: 24px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 32px;
        border: 1px solid rgba(99,102,241,0.4);
    ">CATEGORÍA</span>
    
    <!-- Main headline -->
    <h1 style="
        color: white; 
        font-size: 96px; font-weight: 800;
        text-align: center; margin: 0 80px;
        line-height: 1.1;
        letter-spacing: -2px;
    ">Título Principal del Banner</h1>
    
    <!-- Subtitle -->
    <p style="
        color: rgba(255,255,255,0.6);
        font-size: 36px; margin-top: 32px;
        text-align: center;
    ">Subtítulo descriptivo aquí</p>
    
    <!-- CTA Button -->
    <div style="
        margin-top: 64px;
        background: #6366F1;
        color: white;
        padding: 24px 64px;
        border-radius: 100px;
        font-size: 32px; font-weight: 600;
        letter-spacing: 1px;
    ">Descubre más →</div>
    
    <!-- Logo position -->
    <div style="
        position: absolute; bottom: 60px;
        font-size: 28px; color: rgba(255,255,255,0.4);
        font-weight: 700; letter-spacing: 4px;
    ">MARCA</div>
</div>
```

### Thumbnail YouTube
```html
<div style="
    width: 1280px; height: 720px;
    background: #1A1A2E;
    display: flex; align-items: center;
    font-family: 'Inter', sans-serif;
    overflow: hidden; position: relative;
">
    <!-- Left side: text -->
    <div style="flex: 1; padding: 80px; z-index: 1;">
        <!-- Number/hook -->
        <div style="font-size: 120px; font-weight: 900; color: #F59E0B; line-height: 1;">
            10
        </div>
        <h1 style="
            color: white; font-size: 72px; font-weight: 800;
            line-height: 1.1; margin: 0; text-transform: uppercase;
        ">TIPS DE<br>PYTHON</h1>
        <div style="
            background: #EF4444; color: white;
            padding: 12px 32px; border-radius: 8px;
            font-size: 36px; font-weight: 700;
            display: inline-block; margin-top: 24px;
        ">QUE NO SABÍAS</div>
    </div>
    
    <!-- Right side: image placeholder -->
    <div style="
        width: 500px; height: 100%;
        background: linear-gradient(to left, rgba(26,26,46,0), rgba(26,26,46,1));
        /* Replace with actual person/mascot image */
    "></div>
</div>
```

---

## Reglas de Composición

### Regla de Tercios
- Divide el banner en 9 secciones (3×3)
- Coloca elementos clave en las intersecciones
- El texto en los tercios izquierdo o central
- El visual en el tercio derecho o superior

### Jerarquía Visual
```
1. HEADLINE — más grande, más contrastado
2. SUBHEADLINE — 60-70% del tamaño principal
3. BODY COPY — texto informativo
4. CTA — botón diferenciado por color
5. LOGO — pequeño, en corner
```

### Zona de Seguridad para Redes Sociales
- Mantén texto e elementos importantes a 10% del borde
- Instagram Stories: zona segura = 250px top + bottom (UI overlay)
- YouTube: zona segura = 100px de cada borde

---

## Checklist Pre-Publicación

- [ ] Texto legible en mobile (mínimo 24px equivalente)
- [ ] Contraste suficiente (WCAG AA: ratio ≥4.5:1)
- [ ] Call-to-action visible y claro
- [ ] Logo presente y legible
- [ ] Dimensiones exactas de la plataforma
- [ ] Exportado en formato correcto (PNG para logos, JPEG para fotos, MP4 para animados)
- [ ] Peso del archivo optimizado (<1MB para web)
