#!/bin/bash
# Maia OS - Setup Build Environment
# Este script instala todas las dependencias necesarias para construir Maia OS

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║  Maia OS - Setup Build Environment       ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Detectar distribución
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    log_error "No se pudo detectar la distribución"
fi

log_info "Detectada distribución: $DISTRO"

case $DISTRO in
    ubuntu|debian|linuxmint|pop)
        log_info "Actualizando paquetes..."
        sudo apt update
        
        log_info "Instalando dependencias de construcción..."
        sudo apt install -y \
            debootstrap \
            xorriso \
            isolinux \
            syslinux-efi \
            grub-pc-bin \
            grub-efi-amd64-bin \
            mtools \
            squashfs-tools \
            fakeroot \
            genisoimage \
            build-essential \
            devscripts \
            debhelper \
            git \
            wget \
            curl \
            rsync \
            locales \
            tzdata
        ;;
    
    fedora|rhel|centos)
        log_info "Actualizando paquetes..."
        sudo dnf update -y
        
        log_info "Instalando dependencias de construcción..."
        sudo dnf install -y \
            debootstrap \
            xorriso \
            syslinux \
            grub2-pc \
            grub2-efi-x64 \
            mtools \
            squashfs-tools \
            fakeroot \
            genisoimage \
            gcc \
            make \
            rpm-build \
            git \
            wget \
            curl \
            rsync
        ;;
    
    arch|manjaro|endeavouros)
        log_info "Actualizando paquetes..."
        sudo pacman -Sy --noconfirm
        
        log_info "Instalando dependencias de construcción..."
        sudo pacman -S --noconfirm \
            debootstrap \
            libisoburn \
            syslinux \
            grub \
            mtools \
            squashfs-tools \
            fakeroot \
            cdrkit \
            base-devel \
            git \
            wget \
            curl \
            rsync
        ;;
    
    opensuse*)
        log_info "Actualizando paquetes..."
        sudo zypper refresh
        
        log_info "Instalando dependencias de construcción..."
        sudo zypper install -y \
            debootstrap \
            xorriso \
            syslinux \
            grub2 \
            mtools \
            squashfs \
            fakeroot \
            genisoimage \
            patterns-devel-base-devel_basis \
            git \
            wget \
            curl \
            rsync
        ;;
    
    *)
        log_error "Distribución no soportada: $DISTRO"
        ;;
esac

log_success "Entorno de construcción configurado correctamente"
echo ""
echo "Ahora puedes ejecutar:"
echo "  ./scripts/build-iso.sh"
echo ""
