# Logo & Brand Design Skill

## Fuente
Extraído de: ui-ux-pro-max-skill (design category), agency-agents (design division), VoltAgent/awesome-agent-skills (branding)

---

## 55+ Estilos de Logo

### Estilo Minimalista
- Formas geométricas simples (círculo, cuadrado, triángulo)
- Máximo 2 colores
- Espacio negativo como elemento de diseño
- Sin ornamentos
- Ejemplos: Apple, Nike, FedEx (flecha oculta)

### Estilo Wordmark
- Solo tipografía, sin ícono
- Fuente personalizada o modificada
- Legibilidad como prioridad
- Escalable de favicon a billboard
- Ejemplos: Google, Coca-Cola, FedEx

### Estilo Lettermark (Monograma)
- Iniciales de la empresa
- 1-3 letras máximo
- Fuente bold o personalizada
- Versátil para uso pequeño
- Ejemplos: IBM, HBO, NASA

### Estilo Combination Mark
- Ícono + texto juntos
- Pueden usarse separados
- El ícono refuerza el texto
- Más información transmitida
- Ejemplos: Burger King, Lacoste, Puma

### Estilo Emblem/Shield
- Texto dentro del ícono
- Sensación de autoridad y tradición
- Círculo, escudo, o forma contenedora
- Difícil de escalar a muy pequeño
- Ejemplos: Harvard, Starbucks, NFL

### Estilo Mascot
- Personaje representativo
- Marca amigable y cercana
- Alta memorabilidad
- Mejor para marcas de consumo
- Ejemplos: KFC, Michelin, Mr. Clean

### Estilo Abstracto
- Formas no representativas
- Significado interpretable
- Alta unicidad
- Puede resultar ambiguo
- Ejemplos: Pepsi, Adidas, Mitsubishi

---

## Paletas por Industria

### Tecnología/IA
```css
--primary: #6366F1;   /* Indigo */
--secondary: #06B6D4; /* Cyan */
--accent: #8B5CF6;    /* Violet */
--background: #0F172A; /* Slate 900 */
--text: #F8FAFC;
```

### Finanzas/Banca
```css
--primary: #1E3A5F;   /* Navy Blue */
--secondary: #2E7D32; /* Forest Green */
--accent: #C9A84C;    /* Gold */
--background: #FAFAFA;
--text: #1A1A2E;
```

### Salud/Medicina
```css
--primary: #0EA5E9;   /* Sky Blue */
--secondary: #10B981; /* Emerald */
--accent: #F0FDF4;    /* Light mint */
--background: #FFFFFF;
--text: #1E293B;
```

### Food & Beverage
```css
--primary: #DC2626;   /* Red (appetite) */
--secondary: #F59E0B; /* Amber */
--accent: #15803D;    /* Green (fresh) */
--background: #FEF9EF;
--text: #1C1917;
```

### Lujo/Premium
```css
--primary: #1A1A1A;   /* Negro */
--secondary: #C9A84C; /* Oro */
--accent: #FFFFFF;    /* Blanco */
--background: #0D0D0D;
--text: #F5F0E8;      /* Crema */
```

### Sostenibilidad/Eco
```css
--primary: #2D6A4F;   /* Verde bosque */
--secondary: #74C69D; /* Verde claro */
--accent: #B7E4C7;    /* Verde pálido */
--background: #F8FFF4;
--text: #1B4332;
```

---

## Proceso de Diseño de Logo

### Fase 1: Brief (5 preguntas clave)
1. ¿Cuál es el nombre y qué significa?
2. ¿Cuáles son los valores de la marca? (3 palabras)
3. ¿Quién es el cliente/usuario objetivo?
4. ¿Qué dónde se usará? (web, app, imprenta, ropa)
5. ¿Competidores a evitar parecerse?

### Fase 2: Exploración (sketch rápido)
- 20-30 sketches en 30 minutos
- No juzgar, solo explorar
- 3-5 categorías: wordmark, symbol, combination, abstract, mascot
- Elegir top 3 conceptos

### Fase 3: Digitalización
- Vectorizar en Inkscape o Illustrator
- Construir desde formas primitivas
- Usar grids y proporciones áureas
- Preparar variantes: horizontal, vertical, solo ícono

### Fase 4: Sistema de Color
- Paleta primaria (1-2 colores)
- Versión monocromática obligatoria
- Versión sobre fondo oscuro
- Versión sobre fondo claro

### Fase 5: Brand Identity System (CIP)
```
Logo principal
Logo secundario (reducido)
Logo mínimo (favicon 16x16)
Paleta completa
Tipografía principal + secundaria
Iconografía
Fotografía style guide
Patrones/texturas
```

---

## SVG Logo Generation Patterns

### Logo Minimalista con SVG
```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Geometric minimal logo -->
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6366F1"/>
      <stop offset="100%" style="stop-color:#8B5CF6"/>
    </linearGradient>
  </defs>
  
  <!-- Main shape -->
  <circle cx="50" cy="50" r="45" fill="url(#grad)"/>
  
  <!-- Letter or symbol -->
  <text x="50" y="67" 
        font-family="Inter, sans-serif" 
        font-size="52" 
        font-weight="700"
        text-anchor="middle" 
        fill="white">A</text>
</svg>
```

### Tech Logo con Formas Geométricas
```svg
<svg viewBox="0 0 120 40" xmlns="http://www.w3.org/2000/svg">
  <!-- Icon part -->
  <rect x="0" y="10" width="20" height="20" rx="4" fill="#6366F1"/>
  <rect x="5" y="5" width="10" height="10" rx="2" fill="#A5B4FC" opacity="0.7"/>
  
  <!-- Text part -->
  <text x="28" y="28" 
        font-family="Inter, sans-serif"
        font-size="18"
        font-weight="700"
        fill="#1E293B">brand</text>
</svg>
```

---

## Tipografías por Personalidad de Marca

### Innovador / Tech
- **Geist** — Vercel's font, futurista
- **Space Grotesk** — Sci-fi sin serif
- **Syne** — Experimental, única

### Confiable / Corporativo
- **Inter** — Neutral, profesional
- **DM Sans** — Clean, legible
- **Manrope** — Moderna y seria

### Creativo / Artístico
- **Fraunces** — Serif óptica, expresiva
- **Playfair Display** — Elegante editorial
- **Bebas Neue** — Bold, impacto total

### Amigable / Cercano
- **Nunito** — Redondeada, warm
- **Poppins** — Geométrica, friendly
- **Outfit** — Contemporánea, accesible

---

## Checklist de Logo Final

- [ ] Legible a 16x16px (favicon)
- [ ] Funciona en B&N
- [ ] Funciona sobre blanco y negro
- [ ] Versión SVG disponible (escalable infinitamente)
- [ ] Archivos: SVG, PNG 2x, PNG 4x, PDF
- [ ] Guía de uso incorrecto (qué NO hacer)
- [ ] Proporciones documentadas
- [ ] Zona de exclusión definida (espacio mínimo alrededor)
