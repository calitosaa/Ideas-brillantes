---
name: infographics
description: Generate SVG infographics, data visualizations and visual summaries natively
---

# Infographics — SVG Generation

## Overview
Generate complete SVG infographics for any data or concept. Always output self-contained SVG code.

## Bar Chart Infographic
```svg
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <rect width="600" height="400" fill="#1c1b1f" rx="16"/>
  <text x="300" y="40" text-anchor="middle" fill="white" font-size="20" font-weight="bold">
    Título del Gráfico
  </text>
  <!-- Bars -->
  <g transform="translate(60, 60)">
    <rect x="0"   y="220" width="60" height="80"  fill="#6750a4" rx="4"/>
    <rect x="80"  y="160" width="60" height="140" fill="#6750a4" rx="4"/>
    <rect x="160" y="100" width="60" height="200" fill="#6750a4" rx="4"/>
    <rect x="240" y="140" width="60" height="160" fill="#6750a4" rx="4"/>
    <rect x="320" y="60"  width="60" height="240" fill="#6750a4" rx="4"/>
    <!-- Labels -->
    <text x="30"  y="315" text-anchor="middle" fill="#cac4d0" font-size="12">Ene</text>
    <text x="110" y="315" text-anchor="middle" fill="#cac4d0" font-size="12">Feb</text>
    <text x="190" y="315" text-anchor="middle" fill="#cac4d0" font-size="12">Mar</text>
    <text x="270" y="315" text-anchor="middle" fill="#cac4d0" font-size="12">Abr</text>
    <text x="350" y="315" text-anchor="middle" fill="#cac4d0" font-size="12">May</text>
    <!-- Y axis -->
    <line x1="-10" y1="0" x2="-10" y2="300" stroke="#49454f" stroke-width="1"/>
    <line x1="-10" y1="300" x2="420" y2="300" stroke="#49454f" stroke-width="1"/>
  </g>
</svg>
```

## Process Flow (Steps)
```svg
<svg viewBox="0 0 700 180" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <rect width="700" height="180" fill="#f7f2fa" rx="16"/>
  <text x="350" y="30" text-anchor="middle" fill="#1c1b1f" font-size="18" font-weight="bold">
    Proceso en 4 pasos
  </text>
  <!-- Steps -->
  <g>
    <!-- Step 1 -->
    <circle cx="100" cy="100" r="35" fill="#6750a4"/>
    <text x="100" y="95" text-anchor="middle" fill="white" font-size="22" font-weight="bold">1</text>
    <text x="100" y="155" text-anchor="middle" fill="#49454f" font-size="13">Planificar</text>
    <!-- Arrow -->
    <path d="M 140 100 L 175 100" stroke="#6750a4" stroke-width="2" marker-end="url(#arrow)"/>
    <!-- Step 2 -->
    <circle cx="210" cy="100" r="35" fill="#6750a4"/>
    <text x="210" y="95" text-anchor="middle" fill="white" font-size="22" font-weight="bold">2</text>
    <text x="210" y="155" text-anchor="middle" fill="#49454f" font-size="13">Diseñar</text>
    <!-- Arrow -->
    <path d="M 250 100 L 285 100" stroke="#6750a4" stroke-width="2" marker-end="url(#arrow)"/>
    <!-- Step 3 -->
    <circle cx="320" cy="100" r="35" fill="#6750a4"/>
    <text x="320" y="95" text-anchor="middle" fill="white" font-size="22" font-weight="bold">3</text>
    <text x="320" y="155" text-anchor="middle" fill="#49454f" font-size="13">Construir</text>
    <!-- Arrow -->
    <path d="M 360 100 L 395 100" stroke="#6750a4" stroke-width="2" marker-end="url(#arrow)"/>
    <!-- Step 4 -->
    <circle cx="430" cy="100" r="35" fill="#4caf50"/>
    <text x="430" y="95" text-anchor="middle" fill="white" font-size="22" font-weight="bold">4</text>
    <text x="430" y="155" text-anchor="middle" fill="#49454f" font-size="13">Lanzar</text>
  </g>
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#6750a4"/>
    </marker>
  </defs>
</svg>
```

## Pie/Donut Chart
```svg
<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- Donut chart using stroke-dasharray trick -->
  <circle cx="150" cy="150" r="80" fill="none" stroke="#e8def8" stroke-width="40"/>
  <circle cx="150" cy="150" r="80" fill="none" stroke="#6750a4" stroke-width="40"
    stroke-dasharray="150 352" stroke-dashoffset="88" transform="rotate(-90 150 150)"/>
  <circle cx="150" cy="150" r="80" fill="none" stroke="#7d5260" stroke-width="40"
    stroke-dasharray="100 352" stroke-dashoffset="-62" transform="rotate(-90 150 150)"/>
  <!-- Center label -->
  <text x="150" y="145" text-anchor="middle" font-size="28" font-weight="bold" fill="#1c1b1f">68%</text>
  <text x="150" y="165" text-anchor="middle" font-size="12" fill="#49454f">Completado</text>
  <!-- Legend -->
  <rect x="270" y="80" width="14" height="14" fill="#6750a4" rx="3"/>
  <text x="290" y="92" fill="#1c1b1f" font-size="13">Categoría A (43%)</text>
  <rect x="270" y="105" width="14" height="14" fill="#7d5260" rx="3"/>
  <text x="290" y="117" fill="#1c1b1f" font-size="13">Categoría B (28%)</text>
  <rect x="270" y="130" width="14" height="14" fill="#e8def8" rx="3"/>
  <text x="290" y="142" fill="#1c1b1f" font-size="13">Otros (29%)</text>
</svg>
```

## Timeline
```svg
<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <rect width="600" height="300" fill="#f7f2fa" rx="16"/>
  <text x="300" y="35" text-anchor="middle" fill="#1c1b1f" font-size="18" font-weight="bold">
    Línea de Tiempo
  </text>
  <!-- Horizontal line -->
  <line x1="60" y1="150" x2="540" y2="150" stroke="#6750a4" stroke-width="3"/>
  <!-- Events -->
  <circle cx="120" cy="150" r="12" fill="#6750a4"/>
  <text x="120" y="135" text-anchor="middle" fill="#49454f" font-size="11">2022</text>
  <text x="120" y="175" text-anchor="middle" fill="#1c1b1f" font-size="12" font-weight="bold">Inicio</text>

  <circle cx="250" cy="150" r="12" fill="#6750a4"/>
  <text x="250" y="135" text-anchor="middle" fill="#49454f" font-size="11">2023</text>
  <text x="250" y="175" text-anchor="middle" fill="#1c1b1f" font-size="12" font-weight="bold">Fase 1</text>

  <circle cx="380" cy="150" r="12" fill="#6750a4"/>
  <text x="380" y="135" text-anchor="middle" fill="#49454f" font-size="11">2024</text>
  <text x="380" y="175" text-anchor="middle" fill="#1c1b1f" font-size="12" font-weight="bold">Lanzamiento</text>

  <circle cx="480" cy="150" r="14" fill="#4caf50"/>
  <text x="480" y="135" text-anchor="middle" fill="#49454f" font-size="11">2025</text>
  <text x="480" y="175" text-anchor="middle" fill="#1c1b1f" font-size="13" font-weight="bold">Hoy</text>
</svg>
```

## Infographic Types Reference
| Tipo | Cuándo usar |
|------|-------------|
| Barras | Comparar valores entre categorías |
| Líneas | Tendencias temporales |
| Dona/Pie | Proporciones de un total |
| Timeline | Secuencias cronológicas |
| Proceso | Pasos o flujos de trabajo |
| Comparación | Contrastar 2-4 opciones |
| Estadísticas | Destacar números clave con iconos |
| Mapa | Datos geográficos |
| Árbol/Jerarquía | Estructuras organizativas |

## Design Principles
- **Colores**: máximo 3-4 colores por infografía
- **Tipografía**: sans-serif, jerarquía clara (título > labels > datos)
- **Espacio**: dejar respirar los elementos, no saturar
- **Datos**: cada elemento visual representa UN dato o concepto
- **Accesibilidad**: no depender solo del color para codificar información
