# GNOME Shell Extensions Configuration
# Extensiones recomendadas para Material 3 Expressive OS

## Extensiones Principales

### 1. Material You Dynamic Color
- **UUID**: material-you@yilozt
- **Descripción**: Aplica colores dinámicos basados en el wallpaper
- **URL**: https://extensions.gnome.org/extension/4880/material-you-dynamic-color/
- **Estado**: Recomendada (Esencial)

### 2. Blur My Shell
- **UUID**: blur-my-shell@aunetx
- **Descripción**: Añade efectos de desenfoque al shell
- **URL**: https://extensions.gnome.org/extension/3193/blur-my-shell/
- **Estado**: Recomendada

### 3. Just Perfection
- **UUID**: just-perfection-desktop@just-perfection
- **Descripción**: Personalización avanzada del shell
- **URL**: https://extensions.gnome.org/extension/3843/just-perfection/
- **Estado**: Opcional

### 4. Dash to Dock
- **UUID**: dash-to-dock@micxgx.gmail.com
- **Descripción**: Convierte el dash en un dock flotante
- **URL**: https://extensions.gnome.org/extension/307/dash-to-dock/
- **Estado**: Opcional

### 5. User Themes
- **UUID**: user-theme@gnome-shell-extensions.gcampax.github.com
- **Descripción**: Permite cargar temas del shell desde ~/.themes
- **URL**: https://extensions.gnome.org/extension/19/user-themes/
- **Estado**: Requerida

### 6. Rounded Corners
- **UUID**: rounded-corners@fxn
- **Descripción**: Bordes redondeados en ventanas
- **URL**: https://extensions.gnome.org/extension/5450/rounded-corners/
- **Estado**: Recomendada

### 7. Tiling Assistant
- **UUID**: tiling-assistant@leleat-on-github
- **Descripción**: Mejora el tiling de ventanas estilo Windows
- **URL**: https://extensions.gnome.org/extension/4843/tiling-assistant/
- **Estado**: Opcional

## Instalación Automática

```bash
# Instalar extension-manager si no está disponible
sudo apt install extension-manager  # Debian/Ubuntu
sudo dnf install extension-manager  # Fedora

# Instalar extensiones desde línea de comandos
gnome-extensions install material-you@yilozt
gnome-extensions install blur-my-shell@aunetx
gnome-extensions install just-perfection-desktop@just-perfection
gnome-extensions enable material-you@yilozt
gnome-extensions enable blur-my-shell@aunetx
gnome-extensions enable just-perfection-desktop@just-perfection
```

## Configuración Recomendada

### Material You
- Activar: Sí
- Seguir wallpaper: Sí
- Aplicar a GTK: Sí
- Aplicar a Iconos: Sí

### Blur My Shell
- Panel: Blur activado, Opacidad 0.8
- Overview: Blur activado
- AppGrid: Blur activado
- Lockscreen: Blur activado

### Just Perfection
- Ocultar botón de actividades: Sí
- Animaciones personalizadas: Habilitadas
- Espaciado reducido: Sí

## Notas

- Algunas extensiones pueden requerir reiniciar el shell (Alt+F2, luego 'r')
- La compatibilidad varía según la versión de GNOME
- Para GNOME 45+, verificar compatibilidad de cada extensión
