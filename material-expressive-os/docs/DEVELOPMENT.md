# Material 3 Expressive OS - Documentación de Desarrollo

## 📋 Índice

1. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
2. [Estructura de Directorios](#estructura-de-directorios)
3. [Desarrollo Local](#desarrollo-local)
4. [Componentes Principales](#componentes-principales)
5. [API y Interfaces](#api-e-interfaces)
6. [Testing](#testing)
7. [Build y Deploy](#build-y-deploy)

---

## Arquitectura del Proyecto

Material 3 Expressive OS sigue una arquitectura modular basada en componentes:

```
┌─────────────────────────────────────────┐
│         Aplicaciones (apps/)            │
├─────────────────────────────────────────┤
│    Shell Extensions (configs/gnome/)    │
├─────────────────────────────────────────┤
│         Temas (themes/)                 │
├─────────────────────────────────────────┤
│      Scripts de Instalación             │
└─────────────────────────────────────────┘
```

### Capas del Sistema

1. **Capa Base**: Distribución Linux (Ubuntu/Fedora/Debian)
2. **Capa GNOME**: Desktop Environment personalizado
3. **Capa Material 3**: Tema, colores y animaciones
4. **Capa Aplicaciones**: Apps personalizadas

---

## Estructura de Directorios

```
material-expressive-os/
├── themes/                      # Temas GTK/GNOME
│   └── material-3-expressive/   # Tema principal
│       ├── gtk-4.0/            # Estilos GTK 4
│       ├── gtk-3.0/            # Estilos GTK 3 (opcional)
│       └── index.theme         # Metadatos del tema
│
├── configs/                     # Configuraciones del sistema
│   └── gnome/                  # Configuraciones GNOME
│       ├── extensions/         # Extensiones recomendadas
│       └── *.conf             # Archivos de configuración
│
├── apps/                        # Aplicaciones personalizadas
│   ├── launcher/              # App Launcher estilo Pixel
│   │   ├── src/              # Código fuente
│   │   ├── package.json      # Dependencias
│   │   └── README.md         # Documentación específica
│   └── settings/             # App de configuración (futuro)
│
├── scripts/                     # Scripts de automatización
│   ├── install.sh            # Instalación principal
│   ├── build.sh              # Compilación
│   └── deploy.sh             # Despliegue
│
├── assets/                      # Recursos gráficos
│   ├── logos/                # Logotipos
│   │   └── svg/             # Vectores
│   └── wallpapers/           # Fondos de pantalla
│
├── docs/                        # Documentación
│   ├── development/          # Guías de desarrollo
│   └── user/                 # Guías de usuario
│
├── package.json               # Configuración del proyecto
├── README.md                  # Documentación principal
└── LICENSE                    # Licencia MIT
```

---

## Desarrollo Local

### Prerrequisitos

- Node.js 18+
- npm o yarn
- Git
- GNOME Desktop Environment (recomendado para testing)

### Instalación del Entorno

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/material-expressive-os.git
cd material-expressive-os

# Instalar dependencias
npm install

# Instalar dependencias de cada app
npm install --workspaces
```

### Modo Desarrollo

```bash
# Iniciar launcher en modo desarrollo
cd apps/launcher
npm run dev

# Ver logs del sistema
journalctl -f | grep -i material
```

### Hot Reload

Para cambios en tiempo real:

```bash
# GTK Themes
watch -n 1 'cp themes/material-3-expressive/gtk-4.0/gtk.css ~/.themes/material-3-expressive/gtk-4.0/'

# Apps
npm run dev --workspaces
```

---

## Componentes Principales

### 1. Theme Engine

Ubicación: `themes/material-3-expressive/`

El motor de temas implementa:

- **Colores dinámicos**: Basados en Material You
- **Bordes redondeados**: 8px - 28px según componente
- **Elevaciones**: 5 niveles de sombra
- **Animaciones**: Curvas bezier Material 3

Variables CSS principales:

```css
--md-sys-color-primary: #D0BCFF;
--md-sys-color-on-primary: #381E72;
--md-sys-shape-large: 16px;
--md-sys-elevation-3: 0px 4px 8px 3px rgba(0,0,0,0.15);
--md-sys-animation-duration-medium: 300ms;
```

### 2. App Launcher

Ubicación: `apps/launcher/`

Características:

- Búsqueda en tiempo real
- Animaciones fluidas
- Soporte para categorías
- Accesos rápidos
- Integración con sistema

Estructura de archivos:

```
launcher/
├── src/
│   ├── main.js           # Punto de entrada
│   ├── launcher.js       # Lógica del launcher
│   ├── theme.js          # Gestor de temas
│   └── utils.js          # Utilidades
├── public/
│   └── index.html        # HTML base
└── package.json
```

### 3. GNOME Extensions

Ubicación: `configs/gnome/extensions/`

Extensiones configuradas:

| Extensión | UUID | Propósito |
|-----------|------|-----------|
| Material You | material-you@yilozt | Colores dinámicos |
| Blur My Shell | blur-my-shell@aunetx | Efectos blur |
| Just Perfection | just-perfection-desktop@just-perfection | Personalización |

---

## API y Interfaces

### Theme API

```javascript
import { MaterialTheme } from './theme.js';

const theme = new MaterialTheme();

// Cargar tema
await theme.load();

// Obtener color
const primaryColor = theme.getColor('primary');

// Obtener elevación
const shadow = theme.getElevation(3);

// Obtener duración de animación
const duration = theme.getAnimation('durationMedium');
```

### Launcher API

```javascript
import { AppLauncher } from './launcher.js';

const launcher = new AppLauncher();

// Inicializar
await launcher.setup();

// Mostrar/Ocultar
launcher.display();
launcher.hide();
launcher.toggle();

// Estado
const isVisible = launcher.isVisible();
```

---

## Testing

### Tests Unitarios

```bash
# Ejecutar todos los tests
npm test

# Tests específicos
npm test -- apps/launcher

# Coverage
npm run test:coverage
```

### Tests Visuales

Para probar el tema visualmente:

1. Instalar tema en sistema
2. Aplicar desde GNOME Tweaks
3. Probar diferentes aplicaciones GTK
4. Verificar consistencia de colores

### Tests de Integración

```bash
# Script de prueba de integración
./scripts/test-integration.sh

# Verificar extensiones GNOME
gnome-extensions list --enabled
```

---

## Build y Deploy

### Build de Producción

```bash
# Construir todas las apps
npm run build

# Construir tema
./scripts/build-theme.sh

# Generar documentación
npm run docs
```

### Crear Paquete de Instalación

```bash
# Empaquetar para distribución
./scripts/package.sh

# Salida: material-expressive-os-v1.0.0.tar.gz
```

### Deploy a Sistema

```bash
# Instalación local
./scripts/install.sh

# Verificar instalación
./scripts/verify-installation.sh
```

### Publicar Actualizaciones

```bash
# Incrementar versión
npm version patch  # o minor, o major

# Publicar
git push origin main --tags

# Crear release en GitHub
gh release create v1.0.0
```

---

## Contribuir

### Flujo de Trabajo

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcion`)
3. Implementar cambios
4. Escribir tests
5. Commit (`git commit -m 'feat: descripción'`)
6. Push (`git push origin feature/nueva-funcion`)
7. Pull Request

### Convención de Commits

- `feat:` Nueva característica
- `fix:` Corrección de bugs
- `docs:` Cambios en documentación
- `style:` Cambios de formato/estilo
- `refactor:` Refactorización
- `test:` Añadir/modificar tests
- `chore:` Tareas de mantenimiento

---

## Recursos Adicionales

- [Material Design 3 Guidelines](https://m3.material.io/)
- [GNOME Developer Documentation](https://developer.gnome.org/)
- [GTK 4 Reference](https://docs.gtk.org/gtk4/)
- [Libadwaita Documentation](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/)

---

## Soporte

- Issues: [GitHub Issues](https://github.com/tu-usuario/material-expressive-os/issues)
- Discusiones: [GitHub Discussions](https://github.com/tu-usuario/material-expressive-os/discussions)
- Email: soporte@material-expressive.dev
