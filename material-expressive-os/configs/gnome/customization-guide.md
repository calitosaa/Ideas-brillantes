# Material 3 Expressive - Guía de Personalización

## 🎨 Colores y Tema

### Cambiar Colores Dinámicos

Los colores se generan automáticamente basados en tu wallpaper:

1. Abre **Configuración** > **Apariencia**
2. Selecciona un wallpaper nuevo
3. Los colores se actualizarán automáticamente

### Paleta de Colores Manual

Si prefieres colores específicos, edita el archivo:
```
~/.themes/material-3-expressive/gtk-4.0/gtk.css
```

Variables principales:
- `@define-color accent_color`: Color principal
- `@define-color window_bg_color`: Fondo de ventanas
- `@define-color surface`: Superficies

## 🔔 Notificaciones

Las notificaciones siguen Material 3:

- Bordes redondeados (28px)
- Sombras elevadas
- Animaciones suaves de entrada/salida
- Soporte para modo oscuro/claro

Para personalizar:
```bash
gsettings set org.gnome.desktop.notifications show-banners true
```

## 🪟 Ventanas

### Bordes Redondeados

Activar bordes redondeados en todas las ventanas:
```bash
gsettings set org.gnome.mutter round-corners-on true
```

### Animaciones

Las animaciones están configuradas con curvas Material 3:
- Duración estándar: 300ms
- Curva easing: cubic-bezier(0.2, 0.0, 0, 1.0)

## ⌨️ Atajos de Teclado

Personalizados para Material 3 Expressive:

| Acción | Atajo |
|--------|-------|
| Abrir Launcher | Super (Windows) |
| Buscar | Super + A |
| Notificaciones | Super + N |
| Centro de Control | Super + C |
| Captura de pantalla | Super + Shift + S |
| Terminal | Super + T |

Para cambiar atajos:
```bash
gnome-tweaks  # Ir a Teclado y Ratón
```

## 🖥️ Dock

El dock sigue estilo Material 3:

- Flotante con bordes redondeados
- Iconos centrados
- Animaciones al abrir aplicaciones
- Auto-ocultamiento opcional

Configuración recomendada:
```bash
# Dock flotante
gsettings set org.gnome.shell.extensions.dash-to-dock dock-fixed false

# Bordes redondeados
gsettings set org.gnome.shell.extensions.dash-to-dock border-radius 28

# Animaciones
gsettings set org.gnome.shell.extensions.dash-to-dock animate-show-hide true
```

## 🌙 Modo Oscuro/Claro

### Cambio Automático

El sistema cambia automáticamente según la hora:

```bash
# Habilitar cambio automático
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
```

### Cambio Manual

```bash
# Modo oscuro
gsettings set org.gnome.desktop.interface gtk-theme 'Material-You-Dark'

# Modo claro
gsettings set org.gnome.desktop.interface gtk-theme 'Material-You-Light'
```

## 📱 Iconos

Tema de iconos Material Design:

- Iconos circulares/cuadrados con bordes redondeados
- Colores que siguen el tema
- Soporte para carpetas personalizadas

Para cambiar:
```bash
gsettings set org.gnome.desktop.interface icon-theme 'Tela-circle-dark'
```

## 🔤 Fuentes

Fuentes predeterminadas:

- **Interfaz**: Roboto Flex 11
- **Monoespaciada**: Roboto Mono 10
- **Documentos**: Roboto Regular 11

Cambiar fuentes:
```bash
gsettings set org.gnome.desktop.interface font-name 'Roboto Flex 12'
gsettings set org.gnome.desktop.interface monospace-font-name 'Roboto Mono 11'
```

## 🎭 Animaciones Personalizadas

Crear animaciones personalizadas:

1. Editar `~/.config/gtk-4.0/gtk.css`
2. Añadir reglas CSS personalizadas
3. Reiniciar aplicaciones GTK

Ejemplo de animación personalizada:
```css
@keyframes material-fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

window {
  animation: material-fade-in 300ms cubic-bezier(0.2, 0.0, 0, 1.0);
}
```

## 🧩 Extensiones GNOME

Gestionar extensiones:

```bash
# Listar extensiones instaladas
gnome-extensions list

# Habilitar extensión
gnome-extensions enable <extension-uuid>

# Deshabilitar extensión
gnome-extensions disable <extension-uuid>

# Ver configuración
gnome-extensions prefs <extension-uuid>
```

## 🛠️ Herramientas Útiles

### GNOME Tweaks
```bash
gnome-tweaks
```
Personalización avanzada del escritorio.

### Dconf Editor
```bash
dconf-editor
```
Editor de configuración profunda del sistema.

### Extension Manager
```bash
extension-manager
```
Gestor gráfico de extensiones.

## 📊 Rendimiento

Optimizaciones recomendadas:

```bash
# Reducir animaciones para mejor rendimiento
gsettings set org.gnome.desktop.interface enable-animations false

# Modo de alto rendimiento
sudo cpupower frequency-set -g performance
```

## 🐛 Solución de Problemas

### El tema no se aplica
```bash
# Reinstalar tema
rm -rf ~/.themes/material-3-expressive
# Volver a ejecutar script de instalación
```

### Extensiones no funcionan
```bash
# Reiniciar GNOME Shell
# Presionar Alt+F2, escribir 'r', Enter
```

### Colores incorrectos
```bash
# Regenerar colores Material You
# Cambiar wallpaper temporalmente y volver al original
```

## 📚 Recursos Adicionales

- [Material Design 3 Guidelines](https://m3.material.io/)
- [GNOME Extensions](https://extensions.gnome.org/)
- [GTK 4 Documentation](https://docs.gtk.org/gtk4/)
