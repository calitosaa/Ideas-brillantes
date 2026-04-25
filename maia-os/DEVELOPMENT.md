# Guia de Desarrollo de Maia OS

## Introducción

Maia OS es una distribución de Linux completa basada en Debian, diseñada con Material 3 Expressive como filosofía de diseño principal. Esta guía te ayudará a entender cómo construir, personalizar y contribuir al proyecto.

## Arquitectura del Proyecto

```
maia-os/
├── README.md                 # Documentación principal
├── DEVELOPMENT.md           # Esta guía
├── scripts/                 # Scripts de construcción
│   ├── build-iso.sh         # Construye la imagen ISO
│   ├── setup-build-env.sh   # Configura el entorno
│   └── post-install.sh      # Post-instalación
├── configs/                 # Configuraciones del sistema
│   ├── gtk-theme.conf       # Tema GTK Material 3
│   └── distro-config.yaml   # Configuración de la distro
├── assets/                  # Recursos gráficos
│   └── logo.svg             # Logo oficial
├── packages/                # Paquetes .deb personalizados
├── root-overlay/            # Archivos para el sistema instalado
│   ├── etc/skel/            # Perfil de usuario por defecto
│   └── usr/share/           # Recursos del sistema
├── iso/                     # Configuración de la ISO
└── output/                  # ISO generada (gitignore)
```

## Requisitos de Desarrollo

### Hardware Recomendado
- **CPU**: Quad-core 2.5 GHz o superior
- **RAM**: 16 GB mínimo (32 GB recomendado)
- **Almacenamiento**: 100 GB libres mínimo
- **Conexión**: Internet estable para descargar paquetes

### Software Requerido
- Linux (Debian/Ubuntu/Fedora/Arch)
- Git
- Herramientas de construcción de ISO (ver setup-build-env.sh)

## Construcción Rápida

### 1. Configurar entorno
```bash
cd maia-os
sudo ./scripts/setup-build-env.sh
```

### 2. Construir ISO
```bash
sudo ./scripts/build-iso.sh
```

### 3. Probar en máquina virtual
```bash
# Con QEMU/KVM
qemu-system-x86_64 \
  -m 4096 \
  -cdrom output/maia-os-stable-x86_64.iso \
  -boot d \
  -enable-kvm \
  -cpu host

# O usar VirtualBox / VMware
```

## Personalización

### Cambiar el Tema de Colores

Edita `configs/gtk-theme.conf`:

```ini
[colors]
primary=#TU_COLOR_HEX
on-primary=#COLOR_CONTRASTANTE
primary-container=#COLOR_SUAVE
```

Los colores deben seguir las guías de Material 3:
- Primary: Color principal (ej: #6750A4)
- On-primary: Texto sobre primary (generalmente blanco/negro)
- Primary container: Versión suave del primary
- On-primary-container: Texto sobre container

### Agregar Aplicaciones Preinstaladas

Edita `configs/distro-config.yaml`:

```yaml
[packages]
base-packages=paquete1,paquete2,paquete3
custom-apps=mi-app1,mi-app2
```

Para aplicaciones que no están en los repositorios de Debian:
1. Crea un paquete .deb en `packages/`
2. Agrega el script de instalación en `root-overlay/usr/bin/`

### Modificar el Logo

Reemplaza `assets/logo.svg` con tu diseño. El logo debe:
- Ser SVG preferiblemente
- Tener fondo transparente
- Seguir principios Material Design
- Funcir en tamaños pequeños (favicon) y grandes (splash screen)

### Personalizar Wallpapers

Coloca tus wallpapers en:
```
root-overlay/usr/share/backgrounds/maia-os/
```

Formatos soportados: JPG, PNG, WEBP
Resolución recomendada: 1920x1080, 2560x1440, 3840x2160

### Modificar Extensiones de GNOME

El script `post-install.sh` configura las extensiones. Para cambiar:

```bash
# Habilitar extensión
gnome-extensions enable nombre-extension@id

# Deshabilitar extensión
gnome-extensions disable nombre-extension@id

# Configurar extensión
gsettings set org.gnome.shell.extensions.nombre-extension clave valor
```

Extensiones recomendadas para Material 3 Expressive:
- `dash-to-dock` - Dock personalizado
- `burn-my-windows` - Efectos de ventana
- `blur-my-shell` - Efectos de desenfoque
- `impatience` - Acelerar animaciones
- `magic-lamp` - Efecto minimizar estilo macOS

## Crear Aplicaciones "Maia"

Las aplicaciones nativas de Maia OS siguen estos patrones:

### Estructura de Aplicación GTK

```python
#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Adw

class MaiaApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='org.maiaos.appname')
    
    def do_activate(self):
        win = self.active_window or Adw.ApplicationWindow(application=self)
        win.set_title("Maia App")
        win.set_default_size(800, 600)
        win.present()

def main():
    app = MaiaApp()
    app.run()

if __name__ == '__main__':
    main()
```

### Principios de Diseño M3E

1. **Bordes redondeados**: Usa `border-radius: 12px` mínimo
2. **Elevación**: Sombras suaves para profundidad
3. **Color dinámico**: Adapta colores al contexto
4. **Animaciones**: Transiciones de 250ms con easing estándar
5. **Tipografía**: Roboto Flex para texto, Roboto Mono para código

## Testing y QA

### Pruebas Obligatorias

Antes de cada release:

1. **Instalación limpia**
   - Probar en hardware real
   - Probar en VirtualBox/VMware/QEMU
   - Verificar particionado automático/manual

2. **Hardware compatibility**
   - WiFi/Ethernet
   - Bluetooth
   - Audio
   - Gráficos (NVIDIA, AMD, Intel)
   - Impresoras
   - Scanners

3. **Funcionalidad**
   - Boot time < 30 segundos
   - Suspender/hibernar funciona
   - Actualizaciones sin errores
   - Backup/restore funciona

4. **UI/UX**
   - Todas las apps abren correctamente
   - Tema consistente en todas partes
   - Animaciones fluidas (60 FPS)
   - No hay glitches visuales

### Reportar Bugs

Usa GitHub Issues con esta plantilla:

```markdown
**Descripción**
Descripción clara del bug

**Pasos para reproducir**
1. Ir a '...'
2. Click en '....'
3. Ver error

**Comportamiento esperado**
Qué debería pasar

**Capturas de pantalla**
Si aplica

**Información del sistema:**
- Hardware: [CPU, RAM, GPU]
- Versión Maia OS: [1.0.0]
- Kernel: [uname -r]
```

## Publicación de Releases

### Versionado

Semántico: `MAJOR.MINOR.PATCH`
- MAJOR: Cambios incompatibles
- MINOR: Nuevas features compatibles
- PATCH: Bug fixes compatibles

### Proceso de Release

1. Congelar código (`git tag -a vX.Y.Z`)
2. Build de ISO final
3. Testing intensivo (1 semana mínimo)
4. Generar checksums
5. Publicar en GitHub Releases
6. Anunciar en foro/redes sociales

### Canales de Distribución

- **Stable**: Para usuarios generales
- **Beta**: Para testers
- **Nightly**: Builds diarios automáticos

## Contribuir

### Tipos de Contribución

1. **Código**: Features, bug fixes, optimizaciones
2. **Diseño**: Iconos, wallpapers, temas
3. **Documentación**: Guías, tutoriales, traducciones
4. **Testing**: Reportar bugs, verificar fixes
5. **Comunidad**: Ayudar en foro, redes sociales

### Pull Requests

1. Fork del repositorio
2. Crear branch feature (`git checkout -b feature/mi-feature`)
3. Commitear cambios (`git commit -am 'Add mi feature'`)
4. Push al branch (`git push origin feature/mi-feature`)
5. Abrir Pull Request

### Convenciones de Código

- Commits en inglés o español (consistente)
- Mensajes de commit descriptivos
- Código comentado en español
- Tests para nuevas features

## Recursos Útiles

### Documentación Oficial
- [Debian Developer Documentation](https://www.debian.org/doc/manuals/developers-reference/)
- [GNOME Developer Documentation](https://developer.gnome.org/)
- [Material Design 3 Guidelines](https://m3.material.io/)

### Herramientas
- [GIMP](https://www.gimp.org/) - Edición de imágenes
- [Inkscape](https://inkscape.org/) - Gráficos vectoriales
- [GTK Inspector](https://wiki.gnome.org/Projects/GTK/Inspector) - Debugging GTK

### Comunidades
- [Foro Maia OS](https://forum.maia-os.org)
- [Telegram](https://t.me/maiaos)
- [Discord](https://discord.gg/maiaos)

## Licencia

Maia OS es GPL-3.0. Los assets visuales son CC-BY-SA-4.0.

---

**¡Gracias por contribuir a Maia OS!**

*"Diseñado para humanos, construido para el futuro"*
