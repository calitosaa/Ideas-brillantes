# UI/UX Pro Max Skill

## Purpose
Comprehensive UI/UX design system for generating beautiful, accessible, production-ready interfaces across all industries and styles.

---

## 30+ Named UI Styles

### Glass & Material
1. **Glassmorphism** — Frosted glass effect using `backdrop-filter: blur(10px)` with semi-transparent backgrounds (`rgba(255,255,255,0.15)`), subtle border (`1px solid rgba(255,255,255,0.3)`), and soft drop shadows. Best on gradient backgrounds.
2. **Claymorphism** — Soft 3D clay-like elements with thick borders, multiple layered box-shadows for depth, pastel or saturated fills, and rounded corners (≥20px). Elements appear puffy and tactile.
3. **Neumorphism** — Extruded from the background using dual shadows (light top-left, dark bottom-right), same color as background. Subtle, low-contrast. Risk: poor accessibility — always test contrast ratios.
4. **Material 3 (You)** — Google's dynamic color system. Tonal palettes derived from a seed color. Components: cards, FABs, navigation bars, chips. Elevation via tonal surface fills, not drop shadows.
5. **Flat Design 2.0** — Bold flat colors with subtle long shadows. No gradients, no textures. Clean vector iconography.
6. **Skeuomorphism** — Mimics real-world textures (leather, paper, metal). Photorealistic shadows and gradients. Used sparingly in niche contexts (music apps, note apps).

### Layout Paradigms
7. **Bento Grid** — Asymmetric card grid where modules vary in size (1×1, 1×2, 2×2). Made popular by Apple keynotes. Cards contain mixed content types. CSS Grid `grid-template-areas` based.
8. **Spatial UI** — Depth layers with parallax scrolling, z-index hierarchy, and 3D transforms. Elements at different perceived distances. Used in Apple Vision Pro-inspired interfaces.
9. **Brutalism** — Raw, intentionally unconventional. Bold typography (600–900 weight), stark contrast, visible grid lines, monospace fonts, asymmetric layouts. No polish — the rawness is the aesthetic.
10. **Swiss/International** — Grid-strict layout, limited color palette (often 1 accent + black/white), Helvetica or similar neutral typeface, mathematical white space.
11. **Editorial** — Magazine-inspired. Large photography, overlapping text/image, varied column widths, pull quotes, dramatic type scale differences.
12. **Dashboard Grid** — Data-dense, information hierarchy clear. Charts, KPI cards, tables, filters. Compact spacing, monospace for numbers, clear section headers.

### Aesthetic Movements
13. **Minimalism** — Extreme white space, single accent color, maximum 2 typefaces, content-first hierarchy. "If in doubt, take it out."
14. **Maximalism** — Rich patterns, multiple colors, layered elements, decorative typography, illustrations. Intentionally busy.
15. **Dark Mode First** — Designed primarily for dark (#0f0f0f or #1a1a1a base), not inverted light. Elevated surfaces get lighter fills, not borders. Warm-tinted darks reduce eye strain.
16. **Cyberpunk/Neon** — Dark backgrounds (#000 or deep navy), neon accent colors (cyan, magenta, electric green), glitch effects, scanline overlays, monospace type.
17. **Vaporwave/Retrowave** — 80s aesthetic: purple-to-pink gradients, chrome text, grid lines, sun motifs, retro typography (Miami Vice palette).
18. **Memphis Design** — Bold geometric shapes, primary + pastel colors, squiggles, stars, dots as decorative elements. Retro-fun.
19. **Y2K Aesthetic** — Early 2000s nostalgia: chrome, translucent plastic, bubbly type, stark gradients, pixel elements mixed with 3D.
20. **Cottagecore/Organic** — Earthy tones, organic shapes (no sharp corners), botanical illustrations, handwritten fonts, texture overlays (paper, grain).

### Interaction & Motion Styles
21. **Microinteraction-Rich** — Every interaction has a purposeful animation: hover lifts, press sinks, loading skeletons, success morphs, error shakes. Choreographed motion hierarchy.
22. **Scroll Storytelling** — Content revealed through scroll progress. Pinned sections, scroll-triggered animations, horizontal scroll panels within vertical scroll.
23. **3D WebGL** — Three.js or Spline scenes embedded in UI. Product rotations, abstract 3D backgrounds, particle systems.

### Typography-Led Styles
24. **Kinetic Typography** — Type as the primary visual element. Animated words, staggered letter reveals, morphing between states.
25. **Big Type / Loud Branding** — Oversized headlines (vw units), minimal supporting content. Single focus per screen.
26. **Variable Fonts** — Weight, width, slant animated on interaction or scroll. Creates fluid typographic expression.

### Industry-Specific Styles
27. **Enterprise/B2B SaaS** — Dense information, sidebar nav, data tables, badge statuses, neutral palette with single brand accent, compact spacing.
28. **Consumer Mobile-First** — Bottom nav, large touch targets, full-bleed images, infinite scroll, swipe gestures, haptic-equivalent visual feedback.
29. **Luxury/Premium** — Black, white, and one metallic accent (gold/silver). Generous white space, serif headings, photography-led, minimal UI chrome.
30. **Playful/Gamified** — Rounded everything, bright colors, mascots, progress bars, achievement badges, confetti animations, sound design hooks.
31. **Accessibility-First** — WCAG 2.2 AA compliant by design. High contrast (≥4.5:1 text), visible focus rings, skip links, semantic HTML, screen-reader annotations in specs.
32. **Glassmorphism Dark** — Glassmorphism applied to dark backgrounds. Semi-transparent dark panels (`rgba(0,0,0,0.4)`) with blur, bright accent neon borders, stars/gradient background.

---

## 10 Priority-Ordered UX Guidelines

### 1. Accessibility First (WCAG 2.2 AA)
- Color contrast: ≥4.5:1 for body text, ≥3:1 for large text and UI components
- All interactive elements keyboard-navigable with visible focus indicators
- ARIA labels on icon-only buttons, form inputs, and complex widgets
- Alt text for all meaningful images
- Never use color alone to convey information

### 2. Touch Targets ≥ 44px
- All clickable/tappable areas minimum 44×44px (Apple HIG) or 48×48dp (Material)
- Spacing between targets ≥ 8px to prevent mis-taps
- Apply padding rather than making the visual element larger
- Mobile: prefer bottom navigation over top for thumb reach zones

### 3. Performance & Lazy Loading
- Lazy-load images below the fold (`loading="lazy"`)
- Use skeleton screens instead of spinners for content loading
- Critical CSS inlined; non-critical deferred
- Fonts: `font-display: swap`, subset to used characters
- Compress images to WebP/AVIF, use `srcset` for responsive images
- Target Core Web Vitals: LCP <2.5s, INP <200ms, CLS <0.1

### 4. Visual Coherence & Design System
- Consistent spacing scale (4px base: 4, 8, 12, 16, 24, 32, 48, 64)
- Single color palette with defined semantic roles (primary, secondary, error, success, warning, info)
- Typography scale with clear hierarchy (max 3 typefaces, usually 2)
- Reusable component library — no one-off styles

### 5. Responsive Layouts
- Mobile-first CSS: design 320px → expand up
- Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl), 1536px (2xl)
- Fluid typography with `clamp()`: `font-size: clamp(1rem, 2.5vw, 1.5rem)`
- No horizontal scroll on any viewport
- Content readable without zoom on mobile

### 6. Typography Hierarchy
- Max 2 typefaces: one display (headings), one text (body)
- Establish clear scale: H1 > H2 > H3 > body > caption
- Line height: 1.4–1.6 for body, 1.1–1.2 for headings
- Line length: 50–75 characters for comfortable reading
- Sufficient weight contrast between heading and body

### 7. Purposeful Animation
- Duration: micro-interactions 100–200ms, transitions 200–300ms, page transitions 300–500ms
- Easing: ease-out for entering elements, ease-in for exiting, ease-in-out for state changes
- Respect `prefers-reduced-motion`: wrap animations in media query
- Animate 1–2 properties max per element (transform + opacity)
- Never animate for decoration alone — each animation communicates state

### 8. Form Validation UX
- Inline validation: validate on blur (not on keypress for most fields)
- Show errors below the field with red text + icon (never replace the label)
- Error messages: specific and actionable ("Password must be 8+ characters" not "Invalid password")
- Success state: green checkmark on valid fields
- Preserve entered data on validation error
- Autofocus on first field, tab order logical

### 9. Clear Navigation
- Current location always visible (active state, breadcrumb, or highlighted nav item)
- Max 7±2 items in primary navigation
- Mobile: hamburger only if necessary; prefer bottom tabs for 3–5 main sections
- Search always accessible (header position or shortcut ⌘K)
- Back navigation never relies solely on browser back

### 10. Appropriate Data Visualization
- Choose chart type by data relationship: comparison→bar, trend→line, part-of-whole→donut/pie (≤5 segments), distribution→histogram, relationship→scatter
- Label data directly on charts when possible (avoid legends requiring eye movement)
- Colorblind-safe palettes (use shape/pattern redundancy)
- Empty states: explain what data will appear here and how to generate it
- Loading states for async data: skeleton charts not blank spaces

---

## Industry Design Rules

### SaaS (B2B Software)
- **Principles**: Clean, functional, information-dense without feeling overwhelming
- **Colors**: Neutral base (white/light gray), single brand accent (blue, purple, or teal), semantic status colors
- **Layout**: Persistent sidebar navigation, content area, optional right panel
- **Typography**: System fonts or Inter/DM Sans for readability at small sizes
- **Key Components**: Data tables with sort/filter, status badges, multi-step forms, empty states, onboarding flows
- **Tone**: Professional, confident, efficient

### Fintech (Financial Technology)
- **Principles**: Trust signals, security clarity, regulatory compliance visible
- **Colors**: Navy or dark blue (trust), green (positive/growth), red only for genuine losses/errors
- **Layout**: Card-based for accounts/assets, charts prominent, transaction lists clean
- **Trust Signals**: SSL badges, regulatory text, 2FA prompts styled non-intrusively, audit trails
- **Key Components**: Candlestick/line charts, balance displays (large number typography), transfer flows, portfolio allocation
- **Tone**: Authoritative, calm, precise

### Healthcare
- **Principles**: Calm, clear, accessible — reduce patient anxiety
- **Colors**: Soft blues, greens, whites. Avoid clinical sterility (add warmth). Red only for genuine urgency.
- **Accessibility**: WCAG AA minimum, prefer AAA. Large default font sizes. High contrast.
- **Layout**: Large tap targets, minimal cognitive load per screen, progress indicators for multi-step flows
- **Key Components**: Appointment calendars, medication lists, health metric charts, telemedicine video UI
- **Tone**: Warm, reassuring, clear (avoid medical jargon in patient-facing UI)

### E-commerce
- **Principles**: Conversion-focused, product hero, reduce friction to purchase
- **Colors**: Brand palette + high-contrast CTA (often orange, green, or red for buy buttons)
- **Product Hero**: Large imagery, zoom capability, multiple views, video support
- **Conversion Elements**: Clear price, sale price strikethrough, scarcity indicators ("3 left"), trust badges, review scores prominent
- **Checkout**: Progress indicator, minimal fields, guest checkout, multiple payment methods, auto-fill support
- **Tone**: Aspirational for luxury, value-focused for deals, community-focused for lifestyle brands

### Creative / Portfolio
- **Principles**: Expressive, distinctive, the design IS the message
- **Colors**: Determined by brand identity — can be anything, but intentional
- **Layout**: Unconventional layouts acceptable, but usability still required
- **Key Components**: Fullscreen project showcases, case study narratives, smooth page transitions, custom cursors (desktop)
- **Performance**: Optimize heavy media — lazy load portfolios, use video poster frames
- **Tone**: Voice and tone match the creator's personality

### Gaming
- **Principles**: Immersive, dark themes, excitement and energy
- **Colors**: Dark bases (#0a0a0a to #1a1a2e), vivid accent colors (electric blue, neon green, fire orange)
- **Typography**: Display/gaming fonts for headings, readable sans for UI text
- **UI Chrome**: HUD-inspired elements, progress bars, level/XP indicators, achievement pop-ups
- **Key Components**: Game lobbies, leaderboards, inventory grids, character selection, match history
- **Motion**: High-energy transitions, particle effects, screen shake feedback
- **Tone**: Epic, urgent, community-focused

---

## Design System Generation Process

### Step 1: Discovery
1. Define industry, target user, device priority (mobile/desktop/both)
2. Identify brand personality (3–5 adjectives)
3. Gather visual references / mood board

### Step 2: Foundation
1. **Color System**: Pick seed color → generate 5 tonal variants (10%, 30%, 50%, 70%, 90%) + semantic tokens (primary, on-primary, primary-container, on-primary-container, secondary, tertiary, error, surface, on-surface, outline)
2. **Typography Scale**: Select 1–2 typefaces → define 10–12 size/weight combinations with semantic names
3. **Spacing Scale**: 4px base, define t-shirt sizes (xs:4, sm:8, md:16, lg:24, xl:32, 2xl:48, 3xl:64)
4. **Elevation**: 0 (flat), 1 (card), 2 (dropdown), 3 (modal), 4 (toast)
5. **Border Radius**: Consistent scale (sm:4px, md:8px, lg:12px, xl:16px, full:9999px)

### Step 3: Components
Define in order: Button variants → Input/Form → Card → Navigation → Feedback (toast, dialog, progress) → Data display (table, chart) → Layout (grid, container, divider)

### Step 4: Patterns
Document: Auth flows, Onboarding, Empty states, Error states, Loading states, Form patterns, Data table patterns

### Step 5: Governance
- Component changelog
- Usage do/don't examples
- Accessibility annotations
- Motion principles

---

## Tech Stack Guidance

### React + Tailwind CSS
```jsx
// Component pattern
const Button = ({ variant = 'primary', children, ...props }) => {
  const base = 'inline-flex items-center justify-center rounded-lg px-4 py-2.5 text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50';
  const variants = {
    primary: 'bg-indigo-600 text-white hover:bg-indigo-700 focus-visible:ring-indigo-500',
    secondary: 'bg-white text-gray-900 border border-gray-300 hover:bg-gray-50',
    ghost: 'text-gray-700 hover:bg-gray-100',
  };
  return <button className={`${base} ${variants[variant]}`} {...props}>{children}</button>;
};
```

### Next.js
- Use App Router with server components for data-fetching sections
- `next/image` for all images (auto WebP, lazy, srcset)
- `next/font` for zero-layout-shift font loading
- CSS Modules or Tailwind, not both
- Route groups `(marketing)` vs `(app)` for layout splitting

### Vue 3 + Vite
```vue
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
<template>
  <button @click="count++" class="btn-primary">Count: {{ count }}</button>
</template>
```

### HTML + BeerCSS (Material 3)
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.css" rel="stylesheet">
  <script type="module" src="https://cdn.jsdelivr.net/npm/beercss@3/dist/cdn/beer.min.js"></script>
</head>
<body>
  <main class="responsive">
    <article class="card">
      <h5>Card Title</h5>
      <p>Content here.</p>
      <nav>
        <button class="border">Cancel</button>
        <button>Confirm</button>
      </nav>
    </article>
  </main>
</body>
</html>
```
- Always start with `<main class="responsive">` for centered responsive layout
- Use semantic HTML5 elements — BeerCSS styles them directly
- `ui("mode", "dark")` for dark mode; `ui("theme", "#hexcolor")` for dynamic theming
