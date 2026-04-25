#!/bin/bash
# =============================================================================
# Maia OS - Build Script for Bootable ISO
# Material 3 Expressive Linux Distribution
# Basado en Debian 12 Bookworm
# =============================================================================

set -euo pipefail

# Colores para output (Material 3 colors)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables de configuración
VERSION="1.0"
CODENAME="stable"
ARCH="x86_64"
DEBIAN_MIRROR="deb.debian.org"
OUTPUT_DIR="$(pwd)/output"
WORK_DIR="$(pwd)/work"
ISO_LABEL="MAIA_OS"

# Funciones de logging con estilo Material
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "\n${PURPLE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  $1${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════${NC}\n"
}

# Verificar si se ejecuta como root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "Este script debe ejecutarse como root"
        exit 1
    fi
}

# Verificar dependencias
check_dependencies() {
    log_step "Verificando dependencias"
    
    local deps=(
        debootstrap genisoimage xorriso isolinux
        squashfs-tools rsync wget gnupg curl
        fdisk parted dosfstools grub-pc-bin
        grub-efi-amd64-bin mtools syslinux-utils
    )
    
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_warning "Faltan dependencias: ${missing[*]}"
        log_info "Instalando dependencias faltantes..."
        apt-get update
        apt-get install -y "${missing[@]}"
        log_success "Dependencias instaladas"
    else
        log_success "Todas las dependencias están instaladas"
    fi
}

# Limpiar directorios de trabajo
cleanup() {
    log_step "Limpiando directorios de trabajo"
    
    rm -rf "$WORK_DIR"
    rm -rf "$OUTPUT_DIR"
    
    mkdir -p "$WORK_DIR"/{iso,root,chroot}
    mkdir -p "$OUTPUT_DIR"
    
    log_success "Directorios limpios y creados"
}

# Configurar repositorios Debian
setup_repositories() {
    log_step "Configurando repositorios Debian"
    
    cat > "$WORK_DIR/chroot/etc/apt/sources.list" << EOF
deb http://$DEBIAN_MIRROR/debian bookworm main contrib non-free non-free-firmware
deb http://$DEBIAN_MIRROR/debian bookworm-updates main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
EOF
    
    log_success "Repositorios configurados"
}

# Bootstrap del sistema base
bootstrap_system() {
    log_step "Creando sistema base Debian"
    
    debootstrap --arch amd64 \
        --include=systemd,sudo,gnupg,curl,wget,locales,tzdata \
        bookworm "$WORK_DIR/chroot" \
        "http://$DEBIAN_MIRROR/debian/"
    
    log_success "Sistema base creado"
}

# Configurar sistema base
configure_base_system() {
    log_step "Configurando sistema base"
    
    # Montar sistemas de archivos virtuales
    mount -t proc /proc "$WORK_DIR/chroot/proc"
    mount -t sysfs /sys "$WORK_DIR/chroot/sys"
    mount --rbind /dev "$WORK_DIR/chroot/dev"
    mount --rbind /run "$WORK_DIR/chroot/run"
    
    # Copiar DNS
    cp /etc/resolv.conf "$WORK_DIR/chroot/etc/resolv.conf"
    
    # Configurar hostname
    echo "maia-os" > "$WORK_DIR/chroot/etc/hostname"
    
    # Configurar hosts
    cat > "$WORK_DIR/chroot/etc/hosts" << EOF
127.0.0.1   localhost
127.0.1.1   maia-os
::1         localhost ip6-localhost ip6-loopback
ff02::1     ip6-allnodes
ff02::2     ip6-allrouters
EOF
    
    # Configurar locale
    cat > "$WORK_DIR/chroot/etc/locale.gen" << EOF
en_US.UTF-8 UTF-8
es_ES.UTF-8 UTF-8
pt_BR.UTF-8 UTF-8
fr_FR.UTF-8 UTF-8
de_DE.UTF-8 UTF-8
it_IT.UTF-8 UTF-8
ja_JP.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8
ko_KR.UTF-8 UTF-8
ru_RU.UTF-8 UTF-8
EOF
    
    # Configurar timezone
    echo "America/New_York" > "$WORK_DIR/chroot/etc/timezone"
    
    log_success "Sistema base configurado"
}

# Instalar entorno de escritorio GNOME personalizado
install_desktop_environment() {
    log_step "Instalando entorno de escritorio Material 3 Expressive"
    
    chroot "$WORK_DIR/chroot" bash -xe << 'CHROOT_SCRIPT'
    
# Actualizar paquetes
apt-get update

# Instalar GNOME Desktop base
apt-get install -y task-gnome-desktop gnome-shell gnome-session gdm3

# Instalar extensiones GNOME para Material 3
apt-get install -y \
    gnome-shell-extensions \
    gnome-tweaks \
    dconf-editor

# Instalar aplicaciones base con tema Material
apt-get install -y \
    nautilus \
    gnome-terminal \
    gedit \
    eog \
    evince \
    file-roller \
    gnome-calculator \
    gnome-system-monitor \
    gnome-disk-utility \
    baobab \
    loupe \
    snapshot \
    celluloid \
    rhythmbox \
    thunderbird \
    firefox-esr \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress

# Instalar codecs multimedia
apt-get install -y \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libavcodec-extra \
    gstreamer1.0-vaapi \
    gstreamer1.0-v4l2 \
    gstreamer1.0-tools

# Instalar fuentes Material Design
apt-get install -y \
    fonts-roboto \
    fonts-roboto-unhinted \
    fonts-material-design-icons-iconfont

# Descargar Roboto Flex
mkdir -p /usr/share/fonts/truetype/roboto
wget -q https://github.com/google/fonts/raw/main/apache/robotoflex/RobotoFlex%5BGRAD%2CXOPQ%2CXTRA%2CYPIC%2CYOPQ%2CYTAS%2CYTDE%2CYTFI%2CYTLC%2CYTUC%2Copsz%2Cslnt%2Cwdth%2Cwght%5D.ttf \
    -O /usr/share/fonts/truetype/roboto/RobotoFlex.ttf || true

# Actualizar cache de fuentes
fc-cache -fv

# Instalar herramientas de red
apt-get install -y \
    network-manager \
    network-manager-gnome \
    wireless-tools \
    wpasupplicant

# Instalar soporte para impresoras
apt-get install -y \
    cups \
    cups-client \
    cups-bsd \
    system-config-printer

# Instalar soporte Bluetooth
apt-get install -y \
    bluez \
    bluez-tools \
    blueman

# Instalar utilidades del sistema
apt-get install -y \
    htop \
    neofetch \
    git \
    vim \
    curl \
    wget \
    zip \
    unzip \
    p7zip-full \
    unrar

# Instalar Flatpak
apt-get install -y flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Instalar Snap (opcional)
apt-get install -y snapd

# Limpiar caché
apt-get clean
rm -rf /var/lib/apt/lists/*

CHROOT_SCRIPT
    
    log_success "Entorno de escritorio instalado"
}

# Instalar tema Material 3 Expressive
install_material_theme() {
    log_step "Instalando tema Material 3 Expressive"
    
    # Copiar archivos del tema al chroot
    cp -r "$(pwd)/themes" "$WORK_DIR/chroot/usr/share/themes/"
    cp -r "$(pwd)/icons" "$WORK_DIR/chroot/usr/share/icons/"
    cp -r "$(pwd)/wallpapers" "$WORK_DIR/chroot/usr/share/backgrounds/"
    cp -r "$(pwd)/assets" "$WORK_DIR/chroot/usr/share/maia-assets/"
    
    # Copiar aplicaciones personalizadas
    mkdir -p "$WORK_DIR/chroot/opt/maia-apps"
    cp -r "$(pwd)/apps"/* "$WORK_DIR/chroot/opt/maia-apps/" || true
    
    # Configurar tema por defecto
    chroot "$WORK_DIR/chroot" bash -xe << 'CHROOT_SCRIPT'

# Crear directorio de configuración global
mkdir -p /etc/skel/.config/gtk-4.0
mkdir -p /etc/skel/.config/gtk-3.0

# Configurar GTK4 para usar tema Material 3
cat > /etc/skel/.config/gtk-4.0/settings.ini << EOF
[Settings]
gtk-application-prefer-dark-theme=false
gtk-cursor-theme-name=Bibata-Modern-Ice
gtk-font-name=Roboto Flex 11
gtk-icon-theme-name=Maia-Icons
gtk-theme-name=Maia-Material3
EOF

# Configurar GTK3
cat > /etc/skel/.config/gtk-3.0/settings.ini << EOF
[Settings]
gtk-application-prefer-dark-theme=false
gtk-cursor-theme-name=Bibata-Modern-Ice
gtk-font-name=Roboto Flex 11
gtk-icon-theme-name=Maia-Icons
gtk-theme-name=Maia-Material3
gtk-xft-antialias=1
gtk-xft-hinting=1
gtk-xft-hintstyle=hintslight
gtk-xft-rgba=rgb
EOF

# Configurar GNOME para Material 3
dconf write /org/gnome/desktop/interface/gtk-theme "'Maia-Material3'" 2>/dev/null || true
dconf write /org/gnome/desktop/interface/icon-theme "'Maia-Icons'" 2>/dev/null || true
dconf write /org/gnome/desktop/interface/font-name "'Roboto Flex 11'" 2>/dev/null || true
dconf write /org/gnome/desktop/interface/document-font-name "'Roboto Flex 11'" 2>/dev/null || true
dconf write /org/gnome/desktop/interface/monospace-font-name "'Roboto Mono 11'" 2>/dev/null || true

# Configurar fondo de pantalla Material 3
dconf write /org/gnome/desktop/background/picture-uri "'file:///usr/share/backgrounds/maia-default.jpg'" 2>/dev/null || true
dconf write /org/gnome/desktop/background/picture-uri-dark "'file:///usr/share/backgrounds/maia-default-dark.jpg'" 2>/dev/null || true

CHROOT_SCRIPT
    
    log_success "Tema Material 3 instalado"
}

# Configurar GRUB con tema Material 3
configure_grub() {
    log_step "Configurando GRUB con tema Material 3"
    
    # Copiar tema GRUB
    cp -r "$(pwd)/grub-theme" "$WORK_DIR/chroot/boot/grub/themes/maia"
    
    chroot "$WORK_DIR/chroot" bash -xe << 'CHROOT_SCRIPT'

# Configurar GRUB para usar tema Material 3
cat > /etc/default/grub << EOF
GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="Maia OS"
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""
GRUB_THEME=/boot/grub/themes/maia/theme.txt
GRUB_GFXMODE=1920x1080,auto
GRUB_GFXPAYLOAD_LINUX=keep
EOF

# Actualizar GRUB
update-grub

CHROOT_SCRIPT
    
    log_success "GRUB configurado"
}

# Configurar usuario por defecto
configure_default_user() {
    log_step "Configurando usuario por defecto"
    
    chroot "$WORK_DIR/chroot" bash -xe << 'CHROOT_SCRIPT'

# Crear usuario 'maia' con contraseña temporal
useradd -m -s /bin/bash -G sudo,audio,video,plugdev maia
echo "maia:maia" | chpasswd

# Configurar autologin para live session
mkdir -p /etc/gdm3
cat > /etc/gdm3/custom.conf << EOF
[daemon]
AutomaticLoginEnable=true
AutomaticLogin=maia

[security]

[xdmcp]

[chooser]

[debug]
EOF

CHROOT_SCRIPT
    
    log_success "Usuario configurado"
}

# Instalar kernel y firmware
install_kernel_firmware() {
    log_step "Instalando kernel y firmware"
    
    chroot "$WORK_DIR/chroot" bash -xe << 'CHROOT_SCRIPT'

# Instalar kernel Linux más reciente desde backports
echo "deb http://deb.debian.org/debian bookworm-backports main contrib non-free" >> /etc/apt/sources.list
apt-get update
apt-get install -y -t bookworm-backports linux-image-amd64 linux-headers-amd64

# Instalar firmware para hardware común
apt-get install -y \
    firmware-linux \
    firmware-linux-nonfree \
    firmware-misc-nonfree \
    firmware-realtek \
    firmware-iwlwifi \
    firmware-atheros \
    firmware-amd-graphics \
    firmware-nvidia-gsp \
    intel-media-va-driver \
    vainfo

CHROOT_SCRIPT
    
    log_success "Kernel y firmware instalados"
}

# Configurar live session
configure_live_session() {
    log_step "Configurando live session"
    
    # Copiar configuración de live
    cp -r "$(pwd)/live-config"/* "$WORK_DIR/chroot/" 2>/dev/null || true
    
    # Crear script de post-instalación
    cat > "$WORK_DIR/chroot/usr/bin/maia-post-install" << 'SCRIPT'
#!/bin/bash
# Script de post-instalación de Maia OS

echo "╔════════════════════════════════════════════════╗"
echo "║     Maia OS - Post Installation Setup         ║"
echo "║     Material 3 Expressive Experience          ║"
echo "╚════════════════════════════════════════════════╝"

# Detectar hardware y configurar drivers
echo "[1/5] Detectando hardware..."
# Aquí iría la detección automática de hardware

# Configurar actualizaciones automáticas
echo "[2/5] Configurando actualizaciones..."
cat > /etc/apt/apt.conf.d/50unattended-upgrades << EOF
Unattended-Upgrade::Allowed-Origins::
    "\${distro_id}:\${distro_codename}-security";
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
EOF

# Habilitar servicios esenciales
echo "[3/5] Habilitando servicios..."
systemctl enable NetworkManager
systemctl enable bluetooth
systemctl enable cups

# Optimizar rendimiento SSD
echo "[4/5] Optimizando para SSD..."
if [ -d /sys/block/sda/queue ]; then
    echo "discard" >> /etc/fstab
fi

# Mensaje final
echo "[5/5] ¡Configuración completada!"
echo ""
echo "═══════════════════════════════════════════════"
echo "  ¡Bienvenido a Maia OS!"
echo "  Disfruta de la experiencia Material 3"
echo "═══════════════════════════════════════════════"
SCRIPT
    
    chmod +x "$WORK_DIR/chroot/usr/bin/maia-post-install"
    
    log_success "Live session configurada"
}

# Crear estructura de la ISO
create_iso_structure() {
    log_step "Creando estructura de la ISO"
    
    # Crear directorios de la ISO
    mkdir -p "$WORK_DIR/iso"/{live,isolinux,boot/grub}
    
    # Copiar sistema al chroot comprimido
    mksquashfs "$WORK_DIR/chroot" "$WORK_DIR/iso/live/filesystem.squashfs" \
        -comp xz -Xbcj x86 -b 1M -no-progress
    
    # Copiar kernel e initrd
    cp "$WORK_DIR/chroot/boot/vmlinuz-"* "$WORK_DIR/iso/live/vmlinuz" 2>/dev/null || true
    cp "$WORK_DIR/chroot/boot/initrd.img-"* "$WORK_DIR/iso/live/initrd.lz" 2>/dev/null || true
    
    log_success "Estructura de ISO creada"
}

# Configurar bootloader de la ISO
configure_iso_bootloader() {
    log_step "Configurando bootloader de la ISO"
    
    # Crear configuración de isolinux
    cat > "$WORK_DIR/iso/isolinux/isolinux.cfg" << 'ISOLINUX'
UI menu.c32
PROMPT 0
MENU TITLE Maia OS - Material 3 Expressive
TIMEOUT 100
DEFAULT live

LABEL live
    MENU LABEL ^Iniciar Maia OS
    KERNEL /live/vmlinuz
    INITRD /live/initrd.lz
    APPEND boot=live components quiet splash

LABEL live-failsafe
    MENU LABEL ^Modo seguro
    KERNEL /live/vmlinuz
    INITRD /live/initrd.lz
    APPEND boot=live components nomodeset

LABEL install
    MENU LABEL ^Instalar Maia OS
    KERNEL /live/vmlinuz
    INITRD /live/initrd.lz
    APPEND boot=live components install quiet splash

LABEL memtest
    MENU LABEL ^Memtest86+
    KERNEL /live/memtest

ISOLINUX
    
    # Copiar archivos de boot
    cp /usr/lib/ISOLINUX/isolinux.bin "$WORK_DIR/iso/isolinux/" 2>/dev/null || true
    cp /usr/lib/syslinux/modules/bios/menu.c32 "$WORK_DIR/iso/isolinux/" 2>/dev/null || true
    
    # Crear configuración GRUB para EFI
    cat > "$WORK_DIR/iso/boot/grub/grub.cfg" << 'GRUB'
set timeout=10
set default=0

menuentry "Iniciar Maia OS" {
    linux /live/vmlinuz boot=live components quiet splash
    initrd /live/initrd.lz
}

menuentry "Modo seguro" {
    linux /live/vmlinuz boot=live components nomodeset
    initrd /live/initrd.lz
}

menuentry "Instalar Maia OS" {
    linux /live/vmlinuz boot=live components install quiet splash
    initrd /live/initrd.lz
}

menuentry "Memtest86+" {
    linux /live/memtest
}
GRUB
    
    log_success "Bootloader configurado"
}

# Generar ISO final
generate_iso() {
    log_step "Generando ISO final"
    
    local iso_name="maia-os-${VERSION}-${CODENAME}-${ARCH}.iso"
    
    # Crear ISO híbrida (BIOS + UEFI)
    xorriso -as mkisofs \
        -iso-level 3 \
        -rock \
        -joliet \
        -max-size 4G \
        -V "$ISO_LABEL" \
        -preparer "Maia OS Team" \
        -publisher "Maia OS Project" \
        -A "Maia OS ${VERSION} Material 3 Expressive" \
        -input-charset utf-8 \
        -b isolinux/isolinux.bin \
        -c isolinux/boot.cat \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        -eltorito-alt-boot \
        -e boot/grub/efi.img \
        -no-emul-boot \
        -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
        -output "$OUTPUT_DIR/$iso_name" \
        "$WORK_DIR/iso" 2>/dev/null || \
    genisoimage -o "$OUTPUT_DIR/$iso_name" \
        -V "$ISO_LABEL" \
        -J -R \
        -b isolinux/isolinux.bin \
        -c isolinux/boot.cat \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        "$WORK_DIR/iso"
    
    # Calcular checksum
    cd "$OUTPUT_DIR"
    sha256sum "$iso_name" > "${iso_name}.sha256" 2>/dev/null || sha256sum "$iso_name"
    
    log_success "ISO generada: $OUTPUT_DIR/$iso_name"
    log_info "SHA256: $(cat ${iso_name}.sha256 2>/dev/null || echo 'Calculando...')"
}

# Mostrar resumen final
show_summary() {
    log_step "Construcción completada"
    
    echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     Maia OS Build Complete!                    ║${NC}"
    echo -e "${GREEN}║     Material 3 Expressive Experience           ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Ubicación de la ISO: $OUTPUT_DIR/maia-os-${VERSION}-${CODENAME}-${ARCH}.iso"
    echo ""
    echo "Para instalar en USB:"
    echo "  sudo dd if=output/maia-os-${VERSION}-${CODENAME}-${ARCH}.iso of=/dev/sdX bs=4M status=progress"
    echo ""
    echo "Para probar en QEMU:"
    echo "  qemu-system-x86_64 -cdrom output/maia-os-${VERSION}-${CODENAME}-${ARCH}.iso -m 4096 -enable-kvm"
    echo ""
    echo "¡Gracias por usar Maia OS!"
}

# Limpieza al finalizar
cleanup_mounts() {
    log_info "Desmontando sistemas de archivos..."
    umount -l "$WORK_DIR/chroot"/{proc,sys,dev,run} 2>/dev/null || true
}

# Trap para limpieza en caso de error
trap cleanup_mounts EXIT

# Función principal
main() {
    log_step "🚀 Iniciando construcción de Maia OS"
    echo "Versión: $VERSION"
    echo "Arquitectura: $ARCH"
    echo "Fecha: $(date)"
    
    check_root
    check_dependencies
    cleanup
    bootstrap_system
    configure_base_system
    setup_repositories
    install_desktop_environment
    install_material_theme
    configure_grub
    configure_default_user
    install_kernel_firmware
    configure_live_session
    create_iso_structure
    configure_iso_bootloader
    generate_iso
    show_summary
}

# Ejecutar script
main "$@"
