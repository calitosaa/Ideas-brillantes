# Material 3 Expressive OS

Un sistema operativo basado en Linux con una interfaz gráfica completamente diseñada con **Material 3 Expressive**, inspirado en el diseño de Google Pixel pero para PC.

## 🎨 Características

- **Base Linux**: Utiliza una distribución Linux estable como base (recomendado Ubuntu/Debian o Fedora)
- **Material 3 Expressive**: Tema visual completo inspirado en los diseños expresivos de Google
- **Animaciones fluidas**: Transiciones suaves y animaciones modernas
- **Apps personalizadas**: Aplicaciones predeterminadas con diseño Material 3
- **Iconografía moderna**: Iconos adaptados al lenguaje de diseño Material

## 📁 Estructura del Proyecto

```
material-expressive-os/
├── themes/                 # Temas GTK/GNOME Material 3
├── configs/               # Configuraciones del sistema
│   └── gnome/            # Configuraciones específicas de GNOME
├── apps/                  # Aplicaciones personalizadas
├── scripts/              # Scripts de instalación y configuración
├── assets/               # Recursos gráficos
│   └── logos/           # Logotipos del sistema
└── README.md            # Este archivo
```

## 🚀 Instalación

### Requisitos previos

- Distribución Linux basada en GNOME (Ubuntu 22.04+, Fedora 38+, etc.)
- Node.js 18+ (para algunas aplicaciones web)
- Python 3.8+

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/material-expressive-os.git
cd material-expressive-os
```

### Paso 2: Ejecutar script de instalación

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Paso 3: Reiniciar sesión

Cerrar sesión y volver a iniciar para aplicar todos los cambios.

## 🎯 Componentes Principales

### 1. Tema GTK Material 3 Expressive
- Colores dinámicos basados en el wallpaper
- Bordes redondeados personalizados
- Sombras y elevaciones Material Design
- Soporte para modo claro/oscuro automático

### 2. Shell de GNOME Personalizado
- Animaciones expressivas en transiciones
- Panel superior rediseñado
- Launcher estilo Pixel
- Notificaciones Material 3

### 3. Aplicaciones Predeterminadas
- **Explorador de archivos**: Diseño Material 3
- **Terminal**: Tema personalizado con transparencias
- **Configuración**: Interfaz rediseñada
- **Navegador**: Extensiones y tema Material
- **Reproductor multimedia**: UI moderna

## 🛠️ Tecnologías Utilizadas

- **GTK 4 + Libadwaita**: Para aplicaciones nativas
- **GNOME Shell Extensions**: Personalización del shell
- **CSS/SCSS**: Estilos personalizados
- **JavaScript/TypeScript**: Extensiones y aplicaciones
- **Python**: Scripts de automatización
- **Figma**: Diseño de interfaces (archivos disponibles en `/design`)

## 📦 Paquetes Incluidos

El script de instalación configura:

- `gnome-tweaks` - Personalización avanzada
- `extension-manager` - Gestión de extensiones
- `dconf-editor` - Editor de configuración
- Temas GTK Material 3
- Iconos Material Design
- Fuentes Google Sans/Roboto Flex

## 🎨 Paleta de Colores

Basada en Material 3 Expressive:

- **Primary**: Color principal dinámico
- **Secondary**: Color secundario complementario
- **Tertiary**: Color terciario para acentos
- **Surface**: Fondos con tonalidad sutil
- **Background**: Fondo principal
- **Error**: Color para errores

Los colores se adaptan automáticamente al wallpaper del usuario.

## 📱 Inspiración

Este proyecto está inspirado en:

- [Expressive Windows](https://github.com/Runixe786/Expressive-Windows)
- [BeerCSS](https://github.com/beercss/beercss)
- [Exo](https://github.com/debuggyo/Exo)
- [Material 3 Expressive Catalog](https://github.com/meticha/material-3-expressive-catalog)
- Google Pixel UI

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- Comunidad Material Design
- Proyecto GNOME
- Contribuidores de BeerCSS
- Diseñadores de Google Pixel

---

**Nota**: Este es un proyecto en desarrollo. Algunas características pueden estar incompletas o en proceso de implementación.
