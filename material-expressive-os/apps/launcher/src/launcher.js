/**
 * Material 3 Expressive App Launcher
 * Implementación del launcher estilo Pixel
 */

export class AppLauncher {
  constructor() {
    this.visible = false;
    this.apps = [];
    this.searchQuery = '';
    this.container = null;
  }

  async setup() {
    // Cargar aplicaciones disponibles
    await this.loadApps();
    
    // Crear interfaz
    this.createUI();
    
    // Configurar eventos
    this.setupEventListeners();
    
    return Promise.resolve();
  }

  async loadApps() {
    // Simulación de carga de aplicaciones
    // En producción, esto leería desde el sistema
    this.apps = [
      { id: 'browser', name: 'Navegador', icon: 'language', category: 'internet' },
      { id: 'files', name: 'Archivos', icon: 'folder', category: 'system' },
      { id: 'settings', name: 'Configuración', icon: 'settings', category: 'system' },
      { id: 'terminal', name: 'Terminal', icon: 'terminal', category: 'utilities' },
      { id: 'store', name: 'Tienda', icon: 'shopping_bag', category: 'system' },
      { id: 'camera', name: 'Cámara', icon: 'camera_alt', category: 'multimedia' },
      { id: 'photos', name: 'Fotos', icon: 'photo_library', category: 'multimedia' },
      { id: 'music', name: 'Música', icon: 'music_note', category: 'multimedia' },
      { id: 'calendar', name: 'Calendario', icon: 'calendar_today', category: 'productivity' },
      { id: 'mail', name: 'Correo', icon: 'mail', category: 'communication' },
      { id: 'messages', name: 'Mensajes', icon: 'message', category: 'communication' },
      { id: 'contacts', name: 'Contactos', icon: 'people', category: 'communication' },
      { id: 'calculator', name: 'Calculadora', icon: 'calculate', category: 'utilities' },
      { id: 'clock', name: 'Reloj', icon: 'schedule', category: 'utilities' },
      { id: 'weather', name: 'Clima', icon: 'wb_sunny', category: 'utilities' },
      { id: 'maps', name: 'Mapas', icon: 'map', category: 'navigation' },
      { id: 'notes', name: 'Notas', icon: 'note', category: 'productivity' },
      { id: 'tasks', name: 'Tareas', icon: 'task', category: 'productivity' },
    ];
    
    console.log(`✓ Loaded ${this.apps.length} apps`);
  }

  createUI() {
    // Crear contenedor principal
    this.container = document.createElement('div');
    this.container.className = 'material-launcher';
    this.container.innerHTML = `
      <div class="launcher-overlay"></div>
      <div class="launcher-content">
        <div class="search-bar">
          <span class="material-symbols-outlined search-icon">search</span>
          <input 
            type="text" 
            class="search-input" 
            placeholder="Buscar aplicaciones..."
            autocomplete="off"
          />
        </div>
        <div class="apps-grid" id="appsGrid"></div>
        <div class="quick-actions">
          <button class="action-btn" data-action="settings">
            <span class="material-symbols-outlined">settings</span>
          </button>
          <button class="action-btn" data-action="power">
            <span class="material-symbols-outlined">power_settings_new</span>
          </button>
        </div>
      </div>
    `;
    
    document.body.appendChild(this.container);
    
    // Aplicar estilos
    this.applyStyles();
  }

  applyStyles() {
    const styles = `
      .material-launcher {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 9999;
        display: none;
        opacity: 0;
        transition: opacity var(--md-sys-animation-duration-medium, 300ms) var(--md-sys-animation-easing-emphasized, cubic-bezier(0.05, 0.7, 0.1, 1));
      }
      
      .material-launcher.visible {
        display: flex;
        opacity: 1;
      }
      
      .launcher-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(8px);
      }
      
      .launcher-content {
        position: relative;
        margin: auto;
        width: 90%;
        max-width: 800px;
        max-height: 80vh;
        background: var(--md-sys-color-surface, #141218);
        border-radius: var(--md-sys-shape-extra-large, 28px);
        padding: 24px;
        box-shadow: var(--md-sys-elevation-3, 0px 4px 8px 3px rgba(0,0,0,0.15));
        overflow-y: auto;
      }
      
      .search-bar {
        display: flex;
        align-items: center;
        gap: 12px;
        background: var(--md-sys-color-surface-variant, #49454F);
        border-radius: var(--md-sys-shape-full, 9999px);
        padding: 12px 20px;
        margin-bottom: 24px;
      }
      
      .search-icon {
        color: var(--md-sys-color-on-surface-variant, #CAC4D0);
      }
      
      .search-input {
        flex: 1;
        border: none;
        background: transparent;
        color: var(--md-sys-color-on-surface, #E6E1E5);
        font-size: 16px;
        font-family: 'Roboto Flex', sans-serif;
        outline: none;
      }
      
      .apps-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
      }
      
      .app-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 16px;
        border-radius: var(--md-sys-shape-large, 16px);
        cursor: pointer;
        transition: background-color var(--md-sys-animation-duration-short, 150ms) var(--md-sys-animation-easing-standard, cubic-bezier(0.2, 0.0, 0, 1.0));
      }
      
      .app-item:hover {
        background: var(--md-sys-color-surface-variant, #49454F);
      }
      
      .app-icon {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--md-sys-color-primary-container, #4F378B);
        border-radius: var(--md-sys-shape-medium, 12px);
        margin-bottom: 8px;
      }
      
      .app-icon .material-symbols-outlined {
        color: var(--md-sys-color-on-primary-container, #EADDFF);
        font-size: 24px;
      }
      
      .app-name {
        color: var(--md-sys-color-on-surface, #E6E1E5);
        font-size: 12px;
        font-family: 'Roboto Flex', sans-serif;
        text-align: center;
      }
      
      .quick-actions {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
      }
      
      .action-btn {
        width: 48px;
        height: 48px;
        border: none;
        background: var(--md-sys-color-surface-variant, #49454F);
        border-radius: var(--md-sys-shape-full, 9999px);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform var(--md-sys-animation-duration-short, 150ms) var(--md-sys-animation-easing-standard, cubic-bezier(0.2, 0.0, 0, 1.0));
      }
      
      .action-btn:hover {
        transform: scale(1.1);
      }
      
      .action-btn .material-symbols-outlined {
        color: var(--md-sys-color-on-surface-variant, #CAC4D0);
      }
    `;
    
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
  }

  setupEventListeners() {
    // Click en overlay para cerrar
    const overlay = this.container.querySelector('.launcher-overlay');
    overlay.addEventListener('click', () => this.hide());
    
    // Búsqueda
    const searchInput = this.container.querySelector('.search-input');
    searchInput.addEventListener('input', (e) => {
      this.searchQuery = e.target.value.toLowerCase();
      this.filterApps();
    });
    
    // Tecla Escape para cerrar
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.visible) {
        this.hide();
      }
    });
    
    // Botones de acción rápida
    const actionBtns = this.container.querySelectorAll('.action-btn');
    actionBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        this.handleAction(action);
      });
    });
  }

  filterApps() {
    const appsGrid = this.container.querySelector('#appsGrid');
    const filteredApps = this.apps.filter(app => 
      app.name.toLowerCase().includes(this.searchQuery) ||
      app.category.toLowerCase().includes(this.searchQuery)
    );
    
    this.renderApps(filteredApps);
  }

  renderApps(appsToRender = this.apps) {
    const appsGrid = this.container.querySelector('#appsGrid');
    appsGrid.innerHTML = '';
    
    appsToRender.forEach(app => {
      const appElement = document.createElement('div');
      appElement.className = 'app-item';
      appElement.innerHTML = `
        <div class="app-icon">
          <span class="material-symbols-outlined">${app.icon}</span>
        </div>
        <span class="app-name">${app.name}</span>
      `;
      
      appElement.addEventListener('click', () => {
        this.launchApp(app);
      });
      
      appsGrid.appendChild(appElement);
    });
  }

  display() {
    this.container.classList.add('visible');
    this.visible = true;
    
    // Renderizar apps
    this.renderApps();
    
    // Focar input de búsqueda
    setTimeout(() => {
      const searchInput = this.container.querySelector('.search-input');
      searchInput.focus();
    }, 100);
  }

  hide() {
    this.container.classList.remove('visible');
    this.visible = false;
    
    // Limpiar búsqueda
    this.searchQuery = '';
    const searchInput = this.container.querySelector('.search-input');
    if (searchInput) {
      searchInput.value = '';
    }
  }

  isVisible() {
    return this.visible;
  }

  launchApp(app) {
    console.log(`Launching app: ${app.name}`);
    // Aquí iría la lógica real para lanzar la aplicación
    this.hide();
  }

  handleAction(action) {
    console.log(`Handling action: ${action}`);
    // Aquí iría la lógica para cada acción rápida
    this.hide();
  }
}
