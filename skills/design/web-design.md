---
name: web-design
description: Generate complete, production-ready web pages with HTML5, BeerCSS, Material 3 and vanilla JS
---

# Web Design — Complete Page Generation

## Overview
Generate full, functional web pages. Always use BeerCSS + Material 3 for styling. Output complete, copy-paste-ready HTML files.

## Landing Page Pattern
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="[description]">
  <title>[Product Name]</title>
  <link href="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <script type="module" src="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.js"></script>
  <style>
    .hero { min-height: 80vh; display: flex; align-items: center; }
    .feature-icon { font-size: 48px; }
    section { padding: 4rem 0; }
  </style>
</head>
<body>

<!-- Navbar -->
<header>
  <nav class="responsive">
    <h5 class="max">Logo</h5>
    <a href="#features">Características</a>
    <a href="#pricing">Precios</a>
    <button>Empezar gratis</button>
  </nav>
</header>

<!-- Hero -->
<section class="hero primary-container">
  <main class="responsive center-align">
    <h1>Título Principal</h1>
    <p class="large-text">Subtítulo descriptivo que explica el valor</p>
    <div class="row center-align large-padding">
      <button class="large-padding">Empezar gratis</button>
      <button class="border large-padding">Ver demo</button>
    </div>
  </main>
</section>

<!-- Features -->
<section id="features">
  <main class="responsive">
    <h2 class="center-align">Características</h2>
    <div class="grid large-margin">
      <article class="s12 m6 l4 padding center-align">
        <i class="feature-icon">bolt</i>
        <h5>Rápido</h5>
        <p>Descripción de la característica.</p>
      </article>
      <article class="s12 m6 l4 padding center-align">
        <i class="feature-icon">shield</i>
        <h5>Seguro</h5>
        <p>Descripción de la característica.</p>
      </article>
      <article class="s12 m6 l4 padding center-align">
        <i class="feature-icon">devices</i>
        <h5>Multi-plataforma</h5>
        <p>Descripción de la característica.</p>
      </article>
    </div>
  </main>
</section>

<!-- CTA -->
<section class="secondary-container">
  <main class="responsive center-align padding">
    <h2>Empieza hoy</h2>
    <p>Sin tarjeta de crédito requerida.</p>
    <button class="large-padding">Crear cuenta gratis</button>
  </main>
</section>

<!-- Footer -->
<footer class="surface-variant">
  <main class="responsive padding">
    <div class="grid">
      <div class="s12 m6">
        <h6>Producto</h6>
        <nav class="vertical"><a href="#">Características</a><a href="#">Precios</a></nav>
      </div>
      <div class="s12 m6">
        <h6>Empresa</h6>
        <nav class="vertical"><a href="#">Acerca de</a><a href="#">Contacto</a></nav>
      </div>
    </div>
    <p class="center-align small">© 2025 Empresa. Todos los derechos reservados.</p>
  </main>
</footer>

</body>
</html>
```

## Dashboard Pattern
```html
<body class="dark">
<header>
  <nav class="responsive">
    <button class="circle transparent" onclick="document.getElementById('drawer').showModal()">
      <i>menu</i>
    </button>
    <h5 class="max">Dashboard</h5>
    <button class="circle transparent"><i>notifications</i></button>
  </nav>
</header>

<dialog class="left" id="drawer">
  <nav>
    <a class="active"><i>dashboard</i><span>Panel</span></a>
    <a><i>bar_chart</i><span>Análisis</span></a>
    <a><i>group</i><span>Usuarios</span></a>
    <a><i>settings</i><span>Ajustes</span></a>
  </nav>
</dialog>

<main class="responsive large-padding">
  <!-- KPI Cards -->
  <div class="grid">
    <article class="s6 l3 padding">
      <label>Usuarios totales</label>
      <h3>12,847</h3>
      <span class="green-text"><i>trending_up</i> +12%</span>
    </article>
    <!-- repeat for other KPIs -->
  </div>

  <!-- Chart placeholder -->
  <article class="padding large-margin">
    <h5>Actividad mensual</h5>
    <canvas id="chart"></canvas>
  </article>
</main>
```

## Responsive Design Rules
- Mobile first: `s12` (full width) → `m6` (half) → `l4` (third)
- Navigation: bottom nav on mobile, drawer on desktop
- Typography scales automatically with BeerCSS
- Test at 320px, 768px, 1024px, 1440px breakpoints

## Forms
```html
<article class="medium padding">
  <h5>Formulario de contacto</h5>
  <form>
    <div class="field border label">
      <input type="text" required>
      <label>Nombre completo</label>
    </div>
    <div class="field border label">
      <input type="email" required>
      <label>Email</label>
    </div>
    <div class="field border label textarea">
      <textarea required></textarea>
      <label>Mensaje</label>
    </div>
    <button type="submit" class="responsive">Enviar mensaje</button>
  </form>
</article>
```

## SEO & Accessibility Checklist
- `<meta name="description">` always included
- `<h1>` exactly once per page
- All `<img>` have `alt` attributes
- Color contrast ratio ≥ 4.5:1 (Material 3 guarantees this)
- Keyboard navigable (BeerCSS handles focus styles)
- `lang` attribute on `<html>`
- Structured data for rich snippets when relevant
