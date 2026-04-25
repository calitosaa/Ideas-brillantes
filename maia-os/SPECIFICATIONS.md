# Maia OS - Especificaciones Técnicas

## Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Maia OS |
| **Versión** | 1.0.0 "Stella" |
| **Basado en** | Debian 12 "Bookworm" |
| **Arquitectura** | x86_64 (amd64) |
| **Kernel** | Linux 6.8+ |
| **Init System** | systemd |
| **Display Server** | Wayland (X11 compatible) |
| **Entorno** | GNOME 45+ personalizado |
| **Licencia** | GPL-3.0 / CC-BY-SA-4.0 |

## Requisitos del Sistema

### Mínimos
- **CPU**: Dual-core 64-bit 2.0 GHz
- **RAM**: 4 GB
- **Almacenamiento**: 25 GB
- **GPU**: OpenGL 3.3+
- **Resolución**: 1280x720

### Recomendados
- **CPU**: Quad-core 64-bit 2.5 GHz+
- **RAM**: 8 GB+
- **Almacenamiento**: 50 GB+ SSD
- **GPU**: Dedicada con 2GB VRAM
- **Resolución**: 1920x1080+

### Para Construcción
- **CPU**: Quad-core 3.0 GHz+
- **RAM**: 16 GB+ (32 GB recomendado)
- **Almacenamiento**: 100 GB libres
- **Conexión**: Internet estable

## Componentes del Sistema

### Kernel y Core
```
Linux Kernel:      6.8+ (patched para M3E)
systemd:           252+
GNU C Library:     2.36
GRUB:              2.06 (con tema M3E)
Firmware:          linux-firmware 2023
```

### Entorno Gráfico
```
GNOME Shell:       45+
Mutter:            45+ (compositor Wayland)
GTK:               4.12+ / 3.24+
Adwaita:           Modificado a M3E
GDM:               45+ (con autologin opcional)
```

### Tema Material 3 Expressive

#### Colores Principales (Dark Theme)
| Token | Valor | Uso |
|-------|-------|-----|
| Primary | #6750A4 | Elementos principales |
| On Primary | #FFFFFF | Texto sobre primary |
| Primary Container | #E8DEF8 | Fondos secundarios |
| Secondary | #625B71 | Elementos secundarios |
| Tertiary | #7D5260 | Acentos |
| Background | #141218 | Fondo principal |
| Surface | #141218 | Superficies |
| Error | #B3261E | Errores |

#### Bordes Redondeados
| Elemento | Radio (px) |
|----------|------------|
| Botones pequeños | 8 |
| Botones medianos | 12 |
| Tarjetas | 16 |
| Diálogos | 24 |
| Bottom sheets | 28 |

#### Animaciones
| Tipo | Duración | Easing |
|------|----------|--------|
| Fade | 150ms | cubic-bezier(0.2, 0.0, 0, 1.0) |
| Slide | 250ms | cubic-bezier(0.2, 0.0, 0, 1.0) |
| Scale | 250ms | cubic-bezier(0.2, 0.0, 0, 1.0) |
| Transform | 350ms | cubic-bezier(0.2, 0.0, 0, 1.0) |

### Aplicaciones Preinstaladas

#### Nativas Maia OS
| Aplicación | Tecnología | Descripción |
|------------|------------|-------------|
| Maia Files | GTK4 + Libadwaita | Gestor de archivos M3E |
| Maia Settings | GTK4 | Configuración unificada |
| Maia Terminal | GTK3 + VTE | Terminal moderna |
| Maia Store | GTK4 | Tienda de apps (APT + Flatpak) |
| Maia Calculator | GTK4 | Calculadora M3E |
| Maia Text Editor | GTK4 | Editor de texto/código |

#### Aplicaciones Base
| Aplicación | Paquete | Propósito |
|------------|---------|-----------|
| Firefox ESR | firefox-esr | Navegador web |
| Nautilus | nautilus | Gestor de archivos base |
| GNOME Terminal | gnome-terminal | Terminal |
| GNOME Software | gnome-software | Gestor de software |
| Rhythmbox | rhythmbox | Música |
| Eye of GNOME | eog | Imágenes |
| Evince | evince | Documentos PDF |
| LibreOffice | libreoffice | Suite ofimática |

#### Flatpak Preconfigurados
```
org.telegram.desktop    - Mensajería
org.spotify.Client      - Música streaming
com.discordapp.Discord  - Chat de voz/texto
com.visualstudio.code   - IDE desarrollo
com.google.Chrome       - Navegador Chrome
org.gimp.GIMP           - Edición de imagen
org.inkscape.Inkscape   - Gráficos vectoriales
com.obsproject.Studio   - Grabación/streaming
md.obsidian.Obsidian    - Notas markdown
com.slack.Slack         - Comunicación equipos
```

### Extensiones GNOME

| Extensión | ID | Función |
|-----------|----|---------|
| Dash to Dock | dash-to-dock@micxgx.gmail.com | Dock inferior M3E |
| User Themes | user-theme@gnome-shell-extensions.gcampax.github.com | Temas shell personalizados |
| Burn My Windows | burn-my-windows@schneegans.github.com | Efectos ventana |
| Magic Lamp | compiz-alike-magic-lamp-effect@ilya.biz | Minimizar estilo macOS |
| Impatience | impatience@gfxmonk.net | Acelerar animaciones |
| Blur My Shell | blur-my-shell@aunetx.github.com | Efectos desenfoque |

### Fuentes Tipográficas

| Fuente | Peso | Uso |
|--------|------|-----|
| Roboto Flex | 100-900 | UI general |
| Roboto Mono | 100-700 | Código/terminal |
| Material Icons | Regular | Iconografía |

**Configuración:**
- Tamaño base: 11pt (UI), 10pt (código)
- Hinting: Slight
- Antialias: RGB
- Line height: 1.5

## Sistema de Paquetes

### Gestores Soportados

1. **APT** (nativo)
   - Repositorios: Debian 12 main + contrib + non-free
   - Repo Maia OS: https://repo.maia-os.org
   
2. **Flatpak** (preferido para apps)
   - Remote: Flathub
   - Sandbox: Por defecto habilitado
   
3. **Snap** (soporte adicional)
   - Classic snaps: Habilitados
   - Strict snaps: Soportados

### Repositorios Configured

```bash
# Debian Bookworm
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb http://deb.debian.org/debian bookworm-updates main contrib non-free
deb http://security.debian.org/debian-security bookworm-security main contrib non-free

# Maia OS Repository
deb [signed-by=/etc/apt/keyrings/maia-os.gpg] https://repo.maia-os.org stable main

# Flathub (Flatpak)
https://flathub.org/repo/flathub.flatpakrepo
```

## Particionado por Defecto

### Esquema Automático (UEFI)

| Mount Point | Tamaño | Tipo | FS |
|-------------|--------|------|-----|
| /boot/efi | 512 MB | EFI | FAT32 |
| /boot | 1 GB | Boot | ext4 |
| / | 40 GB | Root | btrfs |
| /home | Resto | Home | btrfs |
| swap | 8 GB | Swap | swap |

### Esquema Manual Opciones

- LUKS encryption: Opcional (AES-256)
- LVM: Opcional
- Btrfs snapshots: Habilitados por defecto
- Timeshift: Configurado automáticamente

## Seguridad

### Características

✅ Secure Boot compatible  
✅ TPM 2.0 support  
✅ Full disk encryption (LUKS)  
✅ Firewall activado (UFW)  
✅ AppArmor perfiles  
✅ Automatic security updates  
✅ Sandboxed apps (Flatpak)  

### Actualizaciones

- **Security updates**: Automáticos (diarios)
- **Regular updates**: Notificación semanal
- **Major releases**: Notificación manual
- **Kernel updates**: Automáticos con reboot pendiente

## Rendimiento

### Benchmarks Objetivo

| Métrica | Objetivo |
|---------|----------|
| Boot time (cold) | < 30s |
| Boot time (warm) | < 15s |
| Time to desktop | < 20s |
| App launch (Firefox) | < 3s |
| Suspend time | < 5s |
| Resume time | < 3s |

### Optimizaciones

- **Zram**: Compresión de memoria habilitada
- **Preload**: Precarga de aplicaciones frecuentes
- **IONice**: Prioridad I/O optimizada
- **CPU Governor**: Performance on AC, powersave on battery
- **SSD TRIM**: Automático semanal

## Hardware Soportado

### Procesadores
- ✅ Intel Core (2da gen+)
- ✅ AMD Ryzen (1ra gen+)
- ✅ AMD FX / APU
- ⚠️ ARM (en desarrollo)

### Gráficos
- ✅ Intel HD/UHD/Iris
- ✅ AMD Radeon (GCN+)
- ✅ NVIDIA (drivers propietarios disponibles)
- ✅ NVIDIA Optimus (prime-select)

### WiFi/Bluetooth
- ✅ Intel WiFi
- ✅ Realtek (la mayoría)
- ✅ Qualcomm Atheros
- ✅ Broadcom (con firmware)

### Periféricos
- ✅ Touchpads multitouch
- ✅ Touchscreens
- ✅ Webcams UVC
- ✅ Audio HDA Intel
- ✅ Impresoras (CUPS + drivers)
- ✅ Scanners (SANE)

## Internacionalización

### Idiomas Soportados

| Idioma | Código | Estado |
|--------|--------|--------|
| Inglés (US) | en_US | ✅ Completo |
| Español | es_ES | ✅ Completo |
| Portugués (BR) | pt_BR | ✅ Completo |
| Francés | fr_FR | 🔄 Parcial |
| Alemán | de_DE | 🔄 Parcial |
| Italiano | it_IT | ⏳ Pendiente |
| Chino ( Simplificado) | zh_CN | ⏳ Pendiente |
| Japonés | ja_JP | ⏳ Pendiente |

### Teclados

Todos los layouts ISO soportados:
- QWERTY (US, UK, ES, PT, etc.)
- AZERTY (FR, BE)
- QWERTZ (DE, AT)
- Colemak, Dvorak
- Teclados internacionales

## Accesibilidad

### Características Incluidas

✅ Orca Screen Reader  
✅ High Contrast themes  
✅ Large Text options  
✅ Sticky Keys  
✅ Mouse Keys  
✅ Zoom magnifier  
✅ On-screen keyboard  
✅ Dictation (speech-to-text)  

### Estándares Cumplidos

- WCAG 2.1 AA
- Section 508
- EN 301 549

## Networking

### Servicios de Red

| Servicio | Implementación |
|----------|----------------|
| Network Manager | Conexiones WiFi/Ethernet |
| Bluetooth | BlueZ + Blueman GUI |
| VPN | OpenVPN, WireGuard, PPTP |
| Firewall | UFW (iptables frontend) |
| Sharing | Samba, NFS, SSH |
| Remote Desktop | RDP, VNC, GNOME Remote |

### Protocolos Soportados

- IPv4/IPv6 dual stack
- DNS over TLS (opcional)
- WPA3 WiFi security
- 802.1X enterprise auth
- mDNS/Bonjour
- SMB/CIFS file sharing

## Desarrollo

### Herramientas Incluidas

| Categoría | Herramientas |
|-----------|--------------|
| Editores | GNOME Builder, VS Code (Flatpak) |
| Compiladores | GCC, Clang, Make, CMake |
| Interpretes | Python 3, Node.js, Ruby, PHP |
| Version Control | Git, Subversion |
| Containers | Docker, Podman |
| Database | MySQL, PostgreSQL, SQLite |
| Web Dev | Apache, Nginx |

### SDK Disponible

```bash
# Instalar herramientas de desarrollo
sudo apt install build-essential devscripts debhelper
sudo apt install gnome-builder git python3 nodejs npm

# Flatpak SDK
flatpak install flathub org.gnome.Sdk
flatpak install flathub org.freedesktop.Sdk
```

## Contacto y Soporte

### Canales Oficiales

- **Website**: https://maia-os.org
- **Documentation**: https://docs.maia-os.org
- **Forum**: https://forum.maia-os.org
- **Bug Tracker**: https://github.com/maia-os/bugs
- **Telegram**: https://t.me/maiaos
- **Discord**: https://discord.gg/maiaos
- **Twitter**: @MaiaOS
- **Mastodon**: @maiaos@mastodon.social

### Email

- General: info@maia-os.org
- Soporte: support@maia-os.org
- Legal: legal@maia-os.org
- Prensa: press@maia-os.org

---

**Documento Técnico v1.0**  
*Última actualización: Enero 2024*  
*Maia OS Project - https://maia-os.org*
