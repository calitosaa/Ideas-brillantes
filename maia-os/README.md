# Maia OS - Material 3 Expressive Linux Distribution

**Maia OS** es una distribución de Linux completa basada en Debian, diseñada desde cero con los principios de **Material 3 Expressive** de Google. Cada píxel, animación y componente ha sido cuidadosamente diseñado para replicar la experiencia de los dispositivos Google Pixel pero para PC.

## 🎨 Filosofía de Diseño: Material 3 Expressive

Basado en análisis profundo de:
- [Material Design 3 Guidelines](https://m3.material.io/)
- [Expressive Windows (Runixe786)](https://github.com/Runixe786/Expressive-Windows) - Animaciones fluidas y transiciones expresivas
- [BeerCSS](https://github.com/beercss/beercss) - Componentes Material puros y tokens de diseño
- [Exo](https://github.com/debuggyo/Exo) - Estética moderna y minimalista
- [Material 3 Expressive Catalog](https://github.com/meticha/material-3-expressive-catalog) - Paletas de colores y componentes

### Principios Clave Implementados:

1. **Color Dinámico**: Sistema de tokens de color que se adapta al wallpaper del usuario
2. **Formas Expresivas**: Bordes redondeados variables (4px a 28px) según el contexto
3. **Tipografía Escalable**: Roboto Flex con 15 niveles de escala tipográfica
4. **Animaciones con Propósito**: Curvas bezier personalizadas (Emphasized, Standard, Decelerate)
5. **Elevación y Profundidad**: Sombras dinámicas que responden a la interacción
6. **Adaptabilidad**: Modo oscuro/claro automático con transiciones suaves

## 📦 Características del Sistema

### Núcleo del Sistema
- **Base**: Debian 12 "Bookworm" estable
- **Kernel**: Linux 6.8+ con parches de rendimiento
- **Init System**: systemd optimizado
- **Display Server**: Wayland por defecto (X11 compatible)
- **Desktop Environment**: GNOME 45+ altamente personalizado

### Experiencia Visual Material 3 Expressive

#### 🎨 Sistema de Colores
- **Paleta Base**: 5 tonos (Primary, Secondary, Tertiary, Error, Neutral)
- **Tonos Derivados**: 13 variaciones por color (0-100)
- **Contraste Automático**: WCAG AA/AAA garantizado
- **Color Source**: Extracción de colores del wallpaper en tiempo real

#### ✨ Sistema de Animaciones
- **Duraciones**: 
  - Rápida: 150ms (hover, focus)
  - Estándar: 300ms (transiciones de estado)
  - Lenta: 500ms (cambios de página, apertura de apps)
- **Curvas Bezier Personalizadas**:
  - `cubic-bezier(0.2, 0.0, 0, 1.0)` - Emphasized (entrada)
  - `cubic-bezier(0.4, 0.0, 0.2, 1.0)` - Standard (general)
  - `cubic-bezier(0.0, 0.0, 0.2, 1.0)` - Decelerate (salida)
  - `cubic-bezier(0.4, 0.0, 0.6, 1.0)` - Accelerate (entrada rápida)

#### 🔲 Formas y Bordes
- **Componentes Pequeños**: 8px (botones, chips)
- **Componentes Medianos**: 12px (tarjetas, dialogs)
- **Componentes Grandes**: 16px-24px (paneles laterales)
- **Ventanas Completas**: 28px (esquinas superiores)
- **FAB (Floating Action Button)**: 50% (círculo perfecto)

#### 🌑 Elevación y Sombras
- **Nivel 0**: Sin sombra (reposo)
- **Nivel 1**: 0px 1px 2px rgba(0,0,0,0.3), 0px 1px 3px 1px rgba(0,0,0,0.15)
- **Nivel 2**: 0px 1px 2px rgba(0,0,0,0.3), 0px 2px 6px 2px rgba(0,0,0,0.15)
- **Nivel 3**: 0px 4px 8px 3px rgba(0,0,0,0.15), 0px 1px 3px rgba(0,0,0,0.3)
- **Nivel 4**: 0px 6px 10px 4px rgba(0,0,0,0.15), 0px 2px 3px rgba(0,0,0,0.3)
- **Nivel 5**: 0px 8px 12px 6px rgba(0,0,0,0.15), 0px 4px 4px rgba(0,0,0,0.3)

### Aplicaciones Nativas Material 3

Todas las aplicaciones siguen estrictamente las guías de Material 3:

1. **Maia Files** - Gestor de archivos con vista adaptable
2. **Maia Settings** - Configuración del sistema con búsqueda integrada
3. **Maia Store** - Tienda de aplicaciones con diseño de tarjetas
4. **Maia Terminal** - Terminal moderna con transparencia y efectos
5. **Maia Calculator** - Calculadora con historial y conversor
6. **Maia Editor** - Editor de texto con resaltado sintáctico
7. **Maia Browser** - Navegador web basado en Firefox con tema M3
8. **Maia Media** - Reproductor multimedia con visualizaciones

### Launcher Material 3 Expressive
- Búsqueda global con resultados en tiempo real
- Widgets personalizables (clima, calendario, notas)
- Animaciones de apertura/cierre con spring physics
- Grid adaptable (4x4 a 8x8)
- Carpetas con animación de expansión
- Dock flotante con efecto de desenfoque

### Panel de Notificaciones
- Notificaciones agrupadas por aplicación
- Controles rápidos con iconos Material Symbols
- Slider de brillo/volumen con feedback háptico visual
- Modo "No Molestar" con animación de activación
- Historial de notificaciones con scroll suave

## 🛠️ Instalación

### Requisitos Mínimos
- **CPU**: 2 núcleos (64-bit)
- **RAM**: 4 GB (8 GB recomendado)
- **Almacenamiento**: 25 GB mínimo (64 GB recomendado)
- **GPU**: Compatible con OpenGL 3.3+ (Wayland)
- **Resolución**: 1280x720 mínimo

### Métodos de Instalación

#### 1. Desde ISO (Recomendado)
```bash
# Descargar la ISO más reciente
wget https://releases.maia-os.org/stable/maia-os-1.0-x86_64.iso

# Verificar integridad
sha256sum maia-os-1.0-x86_64.iso

# Grabar en USB
sudo dd if=maia-os-1.0-x86_64.iso of=/dev/sdX bs=4M status=progress

# O usar Etcher/Ventoy para mayor facilidad
```

#### 2. Construir desde Código Fuente
```bash
git clone https://github.com/maia-os/maia-os.git
cd maia-os

# Configurar entorno de construcción
sudo ./scripts/setup-build-env.sh

# Construir ISO personalizada
./scripts/build-iso.sh --variant stable --arch x86_64

# La ISO se generará en output/maia-os-stable-x86_64.iso
```

#### 3. Instalación en Máquina Virtual
```bash
# QEMU/KVM
virt-install --name="Maia OS" \
  --memory=4096 --vcpus=2 \
  --disk path=/var/lib/libvirt/images/maia-os.qcow2,size=64 \
  --cdrom maia-os-1.0-x86_64.iso \
  --os-variant debian12 \
  --graphics spice

# VirtualBox
VBoxManage createvm --name "Maia OS" --register
VBoxManage modifyvm "Maia OS" --memory 4096 --vram 128
VBoxManage storageattach "Maia OS" --storagectl SATA --port 0 --type dvddrive --medium maia-os-1.0-x86_64.iso
```

## 🎯 Personalización Avanzada

### Dynamic Color Engine
El sistema extrae automáticamente los colores dominantes del wallpaper y genera una paleta completa de Material 3:

```bash
# Cambiar semilla de color manualmente
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings set org.maia.os.theme primary-color '#6750A4'

# O usar la herramienta gráfica
maia-theme-selector
```

### Extensiones GNOME Incluidas
1. **Material Shell** - Tiling window manager con animaciones M3
2. **Blur My Shell** - Efectos de desenfoque en overview
3. **Just Perfection** - Ajustes finos de UI
4. **Dash to Dock** - Dock flotante estilo Pixel
5. **AppIndicator** - Soporte para indicadores de aplicaciones
6. **GSConnect** - Integración con dispositivos Android
7. **Caffeine** - Evitar suspensión automática

### Temas Adicionales
- **Maia Dark**: Tema oscuro puro con contraste alto
- **Maia Light**: Tema claro con colores pastel
- **Maia AMOLED**: Negro puro para pantallas OLED
- **Maia High Contrast**: Accesibilidad mejorada

## 📊 Especificaciones Técnicas Detalladas

### Kernel y Drivers
- Kernel Linux 6.8 LTS con parches de baja latencia
- Drivers NVIDIA propietarios preinstalados (opcional)
- Soporte completo para hardware moderno (WiFi 6E, Bluetooth 5.3, Thunderbolt 4)
- Firmware actualizado automáticamente vía fwupd

### Seguridad
- Secure Boot habilitado por defecto
- Cifrado LUKS2 durante la instalación
- Firewall UFW configurado automáticamente
- Actualizaciones automáticas de seguridad
- Sandbox para aplicaciones Flatpak
- SELinux/AppArmor perfiles endurecidos

### Rendimiento
- ZRAM habilitado por defecto
- Scheduler BFQ para SSDs
- Governor de CPU "performance" adaptativo
- Compresión de memoria con zstd
- Inicio rápido con systemd-analyze optimize

### Compatibilidad
- **Hardware**: x86_64, ARM64 (Raspberry Pi 4/5, Pinebook Pro)
- **Formatos de Archivo**: Ext4, Btrfs, NTFS, exFAT, APFS (lectura)
- **Protocolos de Red**: WiFi, Ethernet, Bluetooth, NFC (hardware dependiente)
- **Multimedia**: Codecs completos (H.264, H.265, VP9, AV1, AAC, FLAC)

## 🌍 Internacionalización

Soporte completo para múltiples idiomas con traducciones nativas:
- Español (España y Latinoamérica)
- Inglés (EE.UU., Reino Unido)
- Portugués (Brasil y Portugal)
- Francés
- Alemán
- Italiano
- Japonés
- Chino Simplificado y Tradicional
- Coreano
- Ruso

Cada idioma incluye:
- Traducción completa del sistema
- Diccionarios ortográficos
- Teclados virtuales adaptados
- Formatos de fecha/hora locales
- Conversión de unidades automática

## 🧩 Ecosistema de Aplicaciones

### Repositorios Oficiales
- **Main**: Aplicaciones base del sistema (Debian main)
- **Contrib**: Aplicaciones comunitarias validadas
- **Non-free**: Drivers y firmware propietario
- **Flatpak**: Flathub integrado por defecto
- **Snap**: Snapcraft opcional

### Aplicaciones Preinstaladas
- **Ofimática**: LibreOffice Fresh con tema M3
- **Navegación**: Firefox ESR con contenedores
- **Multimedia**: Celluloid (MPV), Rhythmbox
- **Gráficos**: GIMP, Inkscape, Loupe
- **Desarrollo**: GNOME Builder, Git, Python, Node.js
- **Comunicación**: Thunderbird, Fractal (Matrix), Telegram

### Maia Store
Tienda de aplicaciones nativa con:
- Interfaz Material 3 Expressive
- Reseñas y valoraciones de usuarios
- Actualizaciones automáticas en segundo plano
- Categorías curadas por el equipo
- Aplicaciones verificadas por seguridad

## 🔮 Roadmap Futuro

### Versión 1.1 (Q2 2025)
- Soporte para tablets y modo convertible
- Gestos multitáctiles avanzados
- Integración profunda con ecosistema Android
- Asistente de voz "Maia Assistant"

### Versión 2.0 (Q4 2025)
- Kernel propio basado en Linux con optimizaciones M3
- Sistema de paquetes híbrido (APT + OCI containers)
- Escritorio remoto nativo con baja latencia
- Modo gaming con GameMode y drivers optimizados

### Visión a Largo Plazo
- Port a arquitecturas RISC-V
- Versión enterprise con soporte LTS 5 años
- Edición educativa con herramientas pedagógicas
- Maia Cloud Services sincronizados

## 🤝 Contribuir al Proyecto

Maia OS es un proyecto de código abierto bajo licencia GPL-3.0. Puedes contribuir de varias formas:

### Desarrollo
```bash
git clone https://github.com/maia-os/maia-os.git
cd maia-os
./scripts/dev-setup.sh
```

### Reportar Bugs
Usa el tracker de GitHub con la plantilla proporcionada:
- Descripción detallada del problema
- Pasos para reproducir
- Capturas de pantalla o videos
- Logs del sistema (`journalctl -xb`)

### Diseñar
- Nuevos iconos siguiendo Material Design Icons
- Wallpapers optimizados para Dynamic Color
- Prototipos de nuevas características en Figma

### Documentar
- Traducir documentación a otros idiomas
- Mejorar guías de instalación
- Crear tutoriales en video

### Financiar
- OpenCollective: https://opencollective.com/maia-os
- GitHub Sponsors: https://github.com/sponsors/maia-os
- Donaciones únicas vía PayPal

## 📜 Licencia

Maia OS está licenciado bajo **GNU General Public License v3.0**.

El código fuente completo está disponible en:
- GitHub: https://github.com/maia-os/maia-os
- GitLab: https://gitlab.com/maia-os/maia-os
- SourceHut: https://sr.ht/~maia-os/maia-os

Los assets gráficos (logos, wallpapers, iconos) están bajo **Creative Commons BY-SA 4.0**.

## 📞 Contacto y Comunidad

- **Sitio Web**: https://maia-os.org
- **Foro**: https://forum.maia-os.org
- **Discord**: https://discord.gg/maiaos
- **Matrix**: #maia-os:matrix.org
- **Twitter/X**: @MaiaOSOfficial
- **Reddit**: r/MaiaOS
- **YouTube**: Maia OS Official

## 🙏 Agradecimientos

Maia OS no sería posible sin el trabajo increíble de:
- La comunidad de Debian
- El equipo de GNOME
- Google Material Design Team
- Todos los contribuyentes de software libre
- Los diseñadores de los proyectos inspiradores mencionados

---

**Maia OS** - *Donde la elegancia de Material 3 se encuentra con el poder de Linux.*

*Última actualización: Enero 2025*
*Versión del documento: 1.0.0*
