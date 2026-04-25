#!/bin/bash
# Maia OS - Post Installation Script
# Este script se ejecuta después de instalar el sistema para configuración final

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     Maia OS - Post Installation Setup       ║"
echo "║        Material 3 Expressive Edition        ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Verificar si se ejecuta como root
if [ "$EUID" -ne 0 ]; then
    log_error "Este script debe ejecutarse como root (sudo)"
fi

# Actualizar repositorios
log_info "Actualizando repositorios..."
apt update
apt upgrade -y

# Instalar codecs multimedia
log_info "Instalando codecs multimedia..."
apt install -y \
    ubuntu-restricted-extras \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libavcodec-extra \
    libheif-plugin-aomdec \
    libheif-plugin-libde265

# Configurar Flatpak
log_info "Configurando Flatpak..."
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak update -y

# Instalar aplicaciones Flatpak recomendadas
log_info "Instalando aplicaciones Flatpak recomendadas..."
flatpak install -y flathub \
    org.telegram.desktop \
    org.spotify.Client \
    com.discordapp.Discord \
    com.visualstudio.code \
    com.google.Chrome \
    org.gimp.GIMP \
    org.inkscape.Inkscape \
    com.obsproject.Studio \
    com.getpostman.Postman \
    md.obsidian.Obsidian \
    com.slack.Slack || true

# Habilitar Snap
log_info "Habilitando Snap..."
systemctl enable snapd
systemctl start snapd

# Instalar paquetes Snap populares
snap install --classic code || true
snap install telegram-desktop || true
snap install spotify || true

# Configurar temas Material 3 Expressive
log_info "Aplicando tema Material 3 Expressive..."

# Crear directorios de configuración
mkdir -p /home/maia/.config/gtk-3.0
mkdir -p /home/maia/.config/gtk-4.0

# Copiar configuración GTK
cat > /home/maia/.config/gtk-3.0/settings.ini << 'GTK3_CONFIG'
[Settings]
gtk-theme-name=Materia-dark
gtk-icon-theme-name=Material-Icons
gtk-font-name=Roboto Flex 11
gtk-cursor-theme-name=Maia-Cursor
gtk-cursor-theme-size=24
gtk-toolbar-style=GTK_TOOLBAR_ICONS
gtk-toolbar-icon-size=GTK_ICON_SIZE_LARGE_TOOLBAR
gtk-button-images=0
gtk-menu-images=0
gtk-enable-event-sounds=1
gtk-enable-input-feedback-sounds=0
gtk-xft-antialias=1
gtk-xft-hinting=1
gtk-xft-hintstyle=hintslight
gtk-xft-rgba=rgb
gtk-application-prefer-dark-theme=true
GTK3_CONFIG

cp /home/maia/.config/gtk-3.0/settings.ini /home/maia/.config/gtk-4.0/settings.ini

# Configurar GNOME
log_info "Configurando GNOME con Material 3 Expressive..."

# Establecer tema oscuro por defecto
gsettings set org.gnome.desktop.interface gtk-theme 'Materia-dark' 2>/dev/null || true
gsettings set org.gnome.desktop.interface icon-theme 'Material-Icons' 2>/dev/null || true
gsettings set org.gnome.desktop.interface font-name 'Roboto Flex 11' 2>/dev/null || true
gsettings set org.gnome.desktop.interface document-font-name 'Roboto Flex 11' 2>/dev/null || true
gsettings set org.gnome.desktop.interface monospace-font-name 'Roboto Mono 10' 2>/dev/null || true
gsettings set org.gnome.desktop.interface cursor-theme 'Maia-Cursor' 2>/dev/null || true
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark' 2>/dev/null || true

# Configurar dock
gsettings set org.gnome.shell.extensions.dash-to-dock dock-position BOTTOM 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock transparency-mode FIXED 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock background-opacity 0.8 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock dash-max-icon-size 48 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock extend-height false 2>/dev/null || true

# Configurar animaciones
gsettings set org.gnome.desktop.interface enable-animations true 2>/dev/null || true

# Habilitar extensiones
log_info "Habilitando extensiones de GNOME..."
gnome-extensions enable dash-to-dock@micxgx.gmail.com 2>/dev/null || true
gnome-extensions enable user-theme@gnome-shell-extensions.gcampax.github.com 2>/dev/null || true
gnome-extensions enable burn-my-windows@schneegans.github.com 2>/dev/null || true
gnome-extensions enable compiz-alike-magic-lamp-effect@ilya.biz 2>/dev/null || true
gnome-extensions enable impatience@gfxmonk.net 2>/dev/null || true
gnome-extensions enable blur-my-shell@aunetx.github.com 2>/dev/null || true

# Configurar fondo de pantalla
log_info "Configurando fondo de pantalla..."
gsettings set org.gnome.desktop.background picture-uri 'file:///usr/share/backgrounds/maia-os/default.jpg' 2>/dev/null || true
gsettings set org.gnome.desktop.background picture-uri-dark 'file:///usr/share/backgrounds/maia-os/default-dark.jpg' 2>/dev/null || true

# Configurar fuentes
log_info "Descargando fuentes Roboto Flex y Roboto Mono..."
mkdir -p /usr/share/fonts/truetype/roboto
cd /tmp
wget -q https://github.com/google/fonts/raw/main/apache/robotoflex/RobotoFlex%5BGRAD%2CXOPQ%2CXTRA%2CYOPQ%2CYTAS%2CYTDE%2CYTFI%2CYTLC%2CYTUC%2Copsz%2Cslnt%2Cwdth%2Cwght%5D.ttf -O RobotoFlex.ttf || true
wget -q https://github.com/google/fonts/raw/main/apache/robotomono/RobotoMono%5Bwght%5D.ttf -O RobotoMono.ttf || true
cp RobotoFlex.ttf RobotoMono.ttf /usr/share/fonts/truetype/roboto/ || true
fc-cache -fv /usr/share/fonts/truetype/roboto || true

# Limpiar caché del sistema
log_info "Limpiando caché del sistema..."
apt clean
apt autoremove -y
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/*

# Mensaje final
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║          ¡Instalación Completada!           ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "Maia OS ha sido configurado exitosamente con:"
echo "  ✓ Tema Material 3 Expressive aplicado"
echo "  ✓ Extensiones de GNOME habilitadas"
echo "  ✓ Fuentes Roboto instaladas"
echo "  ✓ Aplicaciones recomendadas instaladas"
echo "  ✓ Flatpak y Snap configurados"
echo ""
echo "Usuario por defecto: maia"
echo "Contraseña: maia"
echo ""
echo "¡Reinicia el sistema para aplicar todos los cambios!"
echo ""
echo "Visita https://maia-os.org para más información"
echo ""
