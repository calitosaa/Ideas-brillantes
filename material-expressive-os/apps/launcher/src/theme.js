/**
 * Material 3 Expressive Theme Manager
 * Gestiona los colores y estilos Material 3
 */

export class MaterialTheme {
  constructor() {
    // Colores base Material 3 Expressive (Dark Mode)
    this.colors = {
      primary: '#D0BCFF',
      onPrimary: '#381E72',
      primaryContainer: '#4F378B',
      onPrimaryContainer: '#EADDFF',
      
      secondary: '#CCC2DC',
      onSecondary: '#332D41',
      secondaryContainer: '#4A4458',
      onSecondaryContainer: '#E8DEF8',
      
      tertiary: '#EFB8C8',
      onTertiary: '#492532',
      tertiaryContainer: '#633B48',
      onTertiaryContainer: '#FFD9E3',
      
      background: '#141218',
      onBackground: '#E6E1E5',
      
      surface: '#141218',
      onSurface: '#E6E1E5',
      surfaceVariant: '#49454F',
      onSurfaceVariant: '#CAC4D0',
      
      outline: '#938F99',
      shadow: 'rgba(0, 0, 0, 0.36)',
      
      error: '#FFB4AB',
      onError: '#690005',
      errorContainer: '#93000A',
      onErrorContainer: '#FFDAD6',
    };

    // Animaciones Material 3
    this.animations = {
      durationShort: 150,
      durationMedium: 300,
      durationLong: 500,
      
      easingStandard: 'cubic-bezier(0.2, 0.0, 0, 1.0)',
      easingEmphasized: 'cubic-bezier(0.05, 0.7, 0.1, 1.0)',
      easingDecelerate: 'cubic-bezier(0.0, 0.0, 0.2, 1)',
      easingAccelerate: 'cubic-bezier(0.4, 0.0, 1, 1)',
    };

    // Border radius Material 3
    this.borderRadius = {
      small: '8px',
      medium: '12px',
      large: '16px',
      extraLarge: '28px',
      full: '9999px',
    };

    // Elevaciones/Sombras
    this.elevation = {
      0: 'none',
      1: '0px 1px 2px rgba(0,0,0,0.3), 0px 1px 3px 1px rgba(0,0,0,0.15)',
      2: '0px 1px 2px rgba(0,0,0,0.3), 0px 2px 6px 2px rgba(0,0,0,0.15)',
      3: '0px 4px 8px 3px rgba(0,0,0,0.15), 0px 1px 3px rgba(0,0,0,0.3)',
      4: '0px 6px 10px 4px rgba(0,0,0,0.15), 0px 2px 3px rgba(0,0,0,0.3)',
      5: '0px 8px 12px 6px rgba(0,0,0,0.15), 0px 4px 4px rgba(0,0,0,0.3)',
    };
  }

  async load() {
    console.log('Loading Material 3 theme...');
    
    // Aplicar variables CSS
    this.applyCSSVariables();
    
    // Cargar fuentes
    await this.loadFonts();
    
    return Promise.resolve();
  }

  applyCSSVariables() {
    const root = document.documentElement;
    
    // Aplicar colores
    Object.entries(this.colors).forEach(([key, value]) => {
      root.style.setProperty(`--md-sys-color-${this.toKebabCase(key)}`, value);
    });
    
    // Aplicar animaciones
    Object.entries(this.animations).forEach(([key, value]) => {
      if (typeof value === 'number') {
        root.style.setProperty(`--md-sys-animation-${this.toKebabCase(key)}`, `${value}ms`);
      } else {
        root.style.setProperty(`--md-sys-animation-${this.toKebabCase(key)}`, value);
      }
    });
    
    // Aplicar border radius
    Object.entries(this.borderRadius).forEach(([key, value]) => {
      root.style.setProperty(`--md-sys-shape-${key}`, value);
    });
    
    // Aplicar elevaciones
    Object.entries(this.elevation).forEach(([key, value]) => {
      root.style.setProperty(`--md-sys-elevation-${key}`, value);
    });
  }

  async loadFonts() {
    // Cargar fuentes de Google
    const fontLinks = [
      'https://fonts.googleapis.com/css2?family=Roboto+Flex:wght@100..1000&display=swap',
      'https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@100..700&display=swap',
      'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined&display=swap',
    ];

    const loadPromises = fontLinks.map(href => {
      return new Promise((resolve, reject) => {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        link.onload = resolve;
        link.onerror = reject;
        document.head.appendChild(link);
      });
    });

    try {
      await Promise.all(loadPromises);
      console.log('✓ Fonts loaded successfully');
    } catch (error) {
      console.warn('⚠ Some fonts failed to load:', error);
    }
  }

  toKebabCase(str) {
    return str.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
  }

  getColor(name) {
    return this.colors[name] || null;
  }

  getElevation(level) {
    return this.elevation[level] || this.elevation[0];
  }

  getAnimation(type) {
    return this.animations[type] || null;
  }
}
