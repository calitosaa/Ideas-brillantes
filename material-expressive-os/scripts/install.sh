#!/bin/bash

# Material 3 Expressive OS - Installation Script
# Este script configura un sistema Linux con Material 3 Expressive

set -e

echo "🎨 Material 3 Expressive OS - Instalación"
echo "=========================================="
echo ""

# Detectar distribución
if [ -f /etc/debian_version ]; then
    DISTRO="debian"
    echo "✓ Distribución detectada: Debian/Ubuntu"
elif [ -f /etc/fedora-release ]; then
    DISTRO="fedora"
    echo "✓ Distribución detectada: Fedora"
else
    echo "⚠ Distribución no soportada automáticamente"
    echo "Continuando con configuración genérica..."
    DISTRO="generic"
fi

# Función para instalar paquetes en Debian/Ubuntu
install_debian() {
    echo "📦 Actualizando repositorios..."
    sudo apt update
    
    echo "📦 Instalando paquetes base..."
    sudo apt install -y \
        gnome-tweaks \
        extension-manager \
        dconf-editor \
        git \
        curl \
        wget \
        build-essential \
        libgtk-4-dev \
        libadwaita-1-dev \
        nodejs \
        npm \
        python3 \
        python3-pip
}

# Función para instalar paquetes en Fedora
install_fedora() {
    echo "📦 Actualizando repositorios..."
    sudo dnf update -y
    
    echo "📦 Instalando paquetes base..."
    sudo dnf install -y \
        gnome-tweaks \
        dconf-editor \
        git \
        curl \
        wget \
        gcc \
        gtk4-devel \
        libadwaita-devel \
        nodejs \
        npm \
        python3 \
        python3-pip
}

# Instalar según distribución
case $DISTRO in
    debian)
        install_debian
        ;;
    fedora)
        install_fedora
        ;;
    *)
        echo "⚠ Configuración manual requerida para esta distribución"
        ;;
esac

# Crear directorios de temas
echo "📁 Creando estructura de directorios..."
THEME_DIR="$HOME/.themes"
ICONS_DIR="$HOME/.icons"
FONTS_DIR="$HOME/.fonts"
GNOME_SHELL_DIR="$HOME/.local/share/gnome-shell"

mkdir -p "$THEME_DIR"
mkdir -p "$ICONS_DIR"
mkdir -p "$FONTS_DIR"
mkdir -p "$GNOME_SHELL_DIR/extensions"

# Descargar e instalar tema Material You
echo "🎨 Instalando tema Material You..."
MATERIAL_YOU_URL="https://github.com/vinceliuice/Material-You-GTK/archive/main.zip"
if command -v wget &> /dev/null; then
    wget -q --show-progress "$MATERIAL_YOU_URL" -O /tmp/material-you.zip || true
    if [ -f /tmp/material-you.zip ]; then
        unzip -q /tmp/material-you.zip -d /tmp/
        cp -r /tmp/Material-You-GTK-main/src/* "$THEME_DIR/" 2>/dev/null || echo "⚠ Tema Material You no disponible, usando alternativas"
        rm -rf /tmp/material-you.zip /tmp/Material-You-GTK-main
    fi
fi

# Descargar iconos Material Design
echo "🔲 Instalando iconos Material Design..."
TELOSAA_ICONS_URL="https://github.com/vinceliuice/Tela-icon-theme/archive/master.zip"
wget -q --show-progress "$TELOSAA_ICONS_URL" -O /tmp/tela-icons.zip || true
if [ -f /tmp/tela-icons.zip ]; then
    unzip -q /tmp/tela-icons.zip -d /tmp/
    cd /tmp/Tela-icon-theme-master && ./install.sh -d "$ICONS_DIR" 2>/dev/null || echo "⚠ Iconos Tela no disponibles"
    rm -rf /tmp/tela-icons.zip /tmp/Tela-icon-theme-master
fi

# Instalar fuentes Google
echo "🔤 Instalando fuentes Google..."
GOOGLE_FONTS_URL="https://github.com/google/fonts/archive/main.zip"
wget -q --show-progress "$GOOGLE_FONTS_URL" -O /tmp/google-fonts.zip || true
if [ -f /tmp/google-fonts.zip ]; then
    unzip -q /tmp/google-fonts.zip -d /tmp/
    mkdir -p "$FONTS_DIR/Google"
    find /tmp/fonts-main -name "*.ttf" -exec cp {} "$FONTS_DIR/Google/" \; 2>/dev/null || echo "⚠ Fuentes no completas"
    fc-cache -fv "$FONTS_DIR" 2>/dev/null || true
    rm -rf /tmp/google-fonts.zip /tmp/fonts-main
fi

# Configurar GNOME Shell Extensions
echo "🔌 Configurando extensiones de GNOME..."

# Lista de extensiones recomendadas
EXTENSIONS=(
    "user-theme@gnome-shell-extensions.gcampax.github.com"
    "dash-to-dock@micxgx.gmail.com"
    "blur-my-shell@aunetx"
    "just-perfection-desktop@just-perfection"
    "material-you@yilozt"
)

# Instalar Extension Manager si está disponible
if command -v gnome-extensions &> /dev/null; then
    echo "✅ Gestor de extensiones disponible"
else
    echo "⚠ Instala Extension Manager manualmente desde software center"
fi

# Aplicar configuración de GNOME
echo "⚙️ Aplicando configuración de GNOME..."
gsettings set org.gnome.desktop.interface gtk-theme "Material-You-Dark" 2>/dev/null || echo "⚠ Tema GTK no aplicado"
gsettings set org.gnome.desktop.interface icon-theme "Tela-circle-dark" 2>/dev/null || echo "⚠ Tema de iconos no aplicado"
gsettings set org.gnome.desktop.interface font-name "Roboto Flex 11" 2>/dev/null || echo "⚠ Fuente no aplicada"
gsettings set org.gnome.desktop.interface monospace-font-name "Roboto Mono 10" 2>/dev/null || echo "⚠ Fuente monoespaciada no aplicada"
gsettings set org.gnome.desktop.wm.preferences button-layout ":minimize,maximize,close" 2>/dev/null || echo "⚠ Botones de ventana no configurados"

# Habilitar animaciones personalizadas
echo "🎬 Configurando animaciones..."
gsettings set org.gnome.desktop.interface enable-animations true 2>/dev/null || true

# Copiar configuraciones personalizadas
echo "📋 Copiando configuraciones personalizadas..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

if [ -d "$PARENT_DIR/configs/gnome" ]; then
    cp -r "$PARENT_DIR/configs/gnome/"* "$HOME/.config/gnome-control-center/" 2>/dev/null || echo "⚠ Algunas configs no se copiaron"
fi

# Instalar aplicaciones personalizadas
echo "📱 Preparando aplicaciones personalizadas..."
if [ -d "$PARENT_DIR/apps" ]; then
    echo "✓ Directorio de apps encontrado"
    # Aquí iría la lógica para compilar/instalar apps personalizadas
fi

# Crear script de post-instalación
POST_INSTALL="$HOME/.material-expressive-post-install.sh"
cat > "$POST_INSTALL" << 'EOF'
#!/bin/bash
echo "🎉 ¡Instalación completada!"
echo ""
echo "Siguientes pasos:"
echo "1. Reinicia tu sesión (logout/login)"
echo "2. Abre 'Ajustes' > 'Apariencia' y selecciona el tema Material You"
echo "3. Personaliza los colores desde la app 'Material You'"
echo "4. Disfruta de tu nuevo sistema Material 3 Expressive!"
echo ""
echo "Para más información, visita el README.md"
EOF

chmod +x "$POST_INSTALL"

echo ""
echo "=========================================="
echo "✅ Instalación completada exitosamente"
echo "=========================================="
echo ""
echo "📝 Próximos pasos:"
echo "   1. Cierra sesión y vuelve a iniciar"
echo "   2. Ejecuta: ~/.material-expressive-post-install.sh"
echo "   3. Personaliza desde Ajustes > Apariencia"
echo ""
echo "🎨 ¡Disfruta de Material 3 Expressive OS!"
echo ""
