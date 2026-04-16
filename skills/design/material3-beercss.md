---
name: material3-beercss
description: Material Design 3 implementation using BeerCSS — generate complete, accessible, responsive UIs natively
---

# Material 3 / BeerCSS — Complete Reference

## Overview
BeerCSS implements Material Design 3 with ~100 CSS classes, zero dependencies, 14.5kb brotli. Use this to generate any UI component or complete page layout.

## CDN Setup
```html
<link href="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.css" rel="stylesheet">
<script type="module" src="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.js"></script>
```

## Buttons
```html
<!-- Primary filled -->
<button class="responsive">Label</button>

<!-- Tonal (secondary) -->
<button class="responsive secondary">Label</button>

<!-- Outlined -->
<button class="responsive border">Label</button>

<!-- Text only -->
<button class="transparent responsive">Label</button>

<!-- FAB -->
<button class="circle extra"><i>add</i></button>

<!-- Extended FAB -->
<button class="extended-fab"><i>add</i><span>New Item</span></button>

<!-- Icon button -->
<button class="circle transparent"><i>search</i></button>

<!-- Button group -->
<div class="field">
  <button>Day</button>
  <button class="active">Week</button>
  <button>Month</button>
</div>
```

## Cards
```html
<!-- Elevated card -->
<article class="medium-elevate">
  <h5>Title</h5>
  <p>Content</p>
</article>

<!-- Filled card -->
<article class="fill">
  <h5>Title</h5>
</article>

<!-- Outlined card -->
<article class="border">
  <h5>Title</h5>
</article>

<!-- With image -->
<article>
  <img src="image.jpg" class="responsive">
  <div class="padding">
    <h5>Title</h5>
    <p>Subtitle</p>
  </div>
</article>
```

## Form Inputs
```html
<!-- Outlined input -->
<div class="field border label">
  <input type="text">
  <label>Email address</label>
</div>

<!-- Filled input -->
<div class="field fill label">
  <input type="text">
  <label>Password</label>
</div>

<!-- With icon -->
<div class="field border label suffix">
  <input type="search">
  <label>Search</label>
  <i>search</i>
</div>

<!-- Textarea -->
<div class="field border label textarea">
  <textarea></textarea>
  <label>Description</label>
</div>

<!-- Select -->
<div class="field border label">
  <select>
    <option>Option 1</option>
    <option>Option 2</option>
  </select>
  <label>Category</label>
</div>

<!-- Checkbox -->
<label class="checkbox">
  <input type="checkbox">
  <span>I agree to terms</span>
</label>

<!-- Switch -->
<label class="switch">
  <input type="checkbox">
  <span>Dark mode</span>
</label>

<!-- Radio -->
<label class="radio">
  <input type="radio" name="opt">
  <span>Option A</span>
</label>
```

## Navigation
```html
<!-- Bottom nav bar -->
<nav class="bottom">
  <a href="#" class="active"><i>home</i><span>Home</span></a>
  <a href="#"><i>search</i><span>Search</span></a>
  <a href="#"><i>person</i><span>Profile</span></a>
</nav>

<!-- Top app bar -->
<header class="responsive">
  <nav>
    <button class="circle transparent"><i>menu</i></button>
    <h5 class="max">App Name</h5>
    <button class="circle transparent"><i>more_vert</i></button>
  </nav>
</header>

<!-- Tabs -->
<div class="tabs">
  <a class="active">Tab 1</a>
  <a>Tab 2</a>
  <a>Tab 3</a>
</div>

<!-- Drawer (sidebar) -->
<dialog class="left" id="drawer">
  <nav>
    <a href="#" class="active"><i>home</i><span>Home</span></a>
    <a href="#"><i>settings</i><span>Settings</span></a>
  </nav>
</dialog>
```

## Layout & Grid
```html
<!-- Responsive grid (auto-columns) -->
<div class="grid">
  <article class="s12 m6 l4">Card 1</article>
  <article class="s12 m6 l4">Card 2</article>
  <article class="s12 m6 l4">Card 3</article>
</div>
<!-- s=small(<600px) m=medium(<1240px) l=large -->

<!-- Flex row -->
<div class="row">
  <div class="max">Left content</div>
  <button>Action</button>
</div>

<!-- Centered container -->
<main class="responsive">
  <!-- max-width: 1040px, centered -->
</main>

<!-- Full page layout -->
<body>
  <header>...</header>
  <main class="responsive">...</main>
  <footer>...</footer>
</body>
```

## Spacing & Sizing
```html
<div class="padding">          <!-- 16px padding all sides -->
<div class="small-padding">   <!-- 8px -->
<div class="large-padding">   <!-- 32px -->
<div class="no-padding">      <!-- 0px -->

<div class="margin">          <!-- 16px margin -->
<div class="small-margin">
<div class="large-margin">

<div class="small">  <!-- width: 240px max -->
<div class="medium"> <!-- width: 360px max -->
<div class="large">  <!-- width: 480px max -->
```

## Typography
```html
<h1>Headline 1</h1>   <!-- 57px -->
<h2>Headline 2</h2>   <!-- 45px -->
<h3>Headline 3</h3>   <!-- 36px -->
<h4>Headline 4</h4>   <!-- 28px -->
<h5>Title Large</h5>  <!-- 22px -->
<h6>Title Medium</h6> <!-- 16px -->
<p>Body Large</p>     <!-- 16px -->
<p class="small">Body Small</p>
<label>Label</label>  <!-- 12px -->
```

## Colors
```html
<!-- Surface variants -->
<div class="primary-container">   <!-- light primary background -->
<div class="secondary-container"> <!-- light secondary background -->
<div class="tertiary-container">  <!-- light tertiary background -->
<div class="error-container">     <!-- light error background -->
<div class="surface-variant">     <!-- neutral surface -->

<!-- Text on colored surfaces -->
<span class="on-primary-container">Text</span>
<span class="primary-text">Primary colored text</span>
```

## Dark Mode
```html
<!-- Auto (follows OS preference) -->
<script>ui("mode", "auto")</script>

<!-- Force dark -->
<script>ui("mode", "dark")</script>

<!-- Toggle button -->
<button onclick="ui('mode', document.body.className.includes('dark') ? 'light' : 'dark')">
  Toggle theme
</button>
```

## Dialogs & Overlays
```html
<!-- Modal dialog -->
<dialog id="myDialog">
  <h5>Dialog Title</h5>
  <p>Dialog content here.</p>
  <div class="row">
    <button class="transparent" onclick="document.getElementById('myDialog').close()">Cancel</button>
    <button>Confirm</button>
  </div>
</dialog>
<button onclick="document.getElementById('myDialog').showModal()">Open</button>

<!-- Snackbar (toast notification) -->
<div class="snackbar bottom active" id="toast">
  <span>Message sent successfully</span>
  <button class="transparent">Dismiss</button>
</div>
```

## Progress Indicators
```html
<!-- Linear -->
<progress></progress>
<progress value="60" max="100"></progress>

<!-- Circular -->
<progress class="circle"></progress>
<progress class="circle" value="75" max="100"></progress>
```

## Chips
```html
<div class="chips">
  <a class="chip active">All</a>
  <a class="chip">Design</a>
  <a class="chip">Engineering</a>
</div>
```

## Complete Page Template
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>App</title>
  <link href="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <script type="module" src="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.js"></script>
</head>
<body>

<header class="responsive">
  <nav>
    <button class="circle transparent" onclick="document.getElementById('sidebar').showModal()">
      <i>menu</i>
    </button>
    <h5 class="max">ideas-brillantes</h5>
    <button class="circle transparent" onclick="ui('mode', 'auto')"><i>dark_mode</i></button>
  </nav>
</header>

<dialog class="left" id="sidebar">
  <nav>
    <a href="#" class="active"><i>home</i><span>Inicio</span></a>
    <a href="#"><i>smart_toy</i><span>Asistente</span></a>
    <a href="#"><i>settings</i><span>Ajustes</span></a>
  </nav>
</dialog>

<main class="responsive">
  <div class="grid">
    <article class="s12 m6 l4 medium-elevate padding">
      <h5>Control del PC</h5>
      <p>Controla apps, archivos y sistema</p>
      <button class="responsive">Explorar</button>
    </article>
    <article class="s12 m6 l4 medium-elevate padding">
      <h5>Automatización</h5>
      <p>Crea workflows y tareas programadas</p>
      <button class="responsive">Crear workflow</button>
    </article>
    <article class="s12 m6 l4 medium-elevate padding">
      <h5>Seguridad</h5>
      <p>Escanea archivos y URLs</p>
      <button class="responsive">Escanear</button>
    </article>
  </div>
</main>

<nav class="bottom">
  <a href="#" class="active"><i>home</i><span>Inicio</span></a>
  <a href="#"><i>chat</i><span>Chat</span></a>
  <a href="#"><i>auto_awesome</i><span>Skills</span></a>
  <a href="#"><i>person</i><span>Perfil</span></a>
</nav>

<script type="module">
  ui("mode", "auto");
</script>
</body>
</html>
```
