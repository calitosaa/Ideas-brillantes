/**
 * Material 3 Expressive Launcher
 * Launcher estilo Google Pixel para GNOME
 * 
 * Este es el punto de entrada principal del launcher
 */

import { AppLauncher } from './launcher.js';
import { MaterialTheme } from './theme.js';

class LauncherApp {
  constructor() {
    this.theme = new MaterialTheme();
    this.launcher = new AppLauncher();
    this.initialized = false;
  }

  async init() {
    console.log('🎨 Initializing Material 3 Expressive Launcher...');
    
    try {
      // Inicializar tema Material 3
      await this.theme.load();
      console.log('✓ Theme loaded');
      
      // Inicializar launcher
      await this.launcher.setup();
      console.log('✓ Launcher setup complete');
      
      this.initialized = true;
      console.log('✅ Material 3 Expressive Launcher ready!');
      
      // Mostrar launcher
      this.show();
    } catch (error) {
      console.error('❌ Error initializing launcher:', error);
      throw error;
    }
  }

  show() {
    if (!this.initialized) {
      console.warn('Launcher not initialized yet');
      return;
    }
    
    this.launcher.display();
  }

  hide() {
    this.launcher.hide();
  }

  toggle() {
    if (this.launcher.isVisible()) {
      this.hide();
    } else {
      this.show();
    }
  }
}

// Exportar instancia global
const app = new LauncherApp();

// Auto-inicializar si se ejecuta directamente
if (import.meta.url === `file://${process.argv[1]}`) {
  app.init().catch(console.error);
}

export { app as default, LauncherApp };
