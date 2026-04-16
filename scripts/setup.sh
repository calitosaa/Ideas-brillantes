#!/bin/bash
# ideas-brillantes — Full Environment Setup Script
# Run with: chmod +x setup.sh && ./setup.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo ""
echo "  ██╗██████╗ ███████╗ █████╗ ███████╗"
echo "  ██║██╔══██╗██╔════╝██╔══██╗██╔════╝"
echo "  ██║██║  ██║█████╗  ███████║███████╗"
echo "  ██║██║  ██║██╔══╝  ██╔══██║╚════██║"
echo "  ██║██████╔╝███████╗██║  ██║███████║"
echo "  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝"
echo "  BRILLANTES — Setup v1.0"
echo ""

# Detect OS
OS="linux"
DISTRO=$(lsb_release -si 2>/dev/null || echo "Unknown")
info "Detected: $DISTRO Linux"

# ====================
# 1. System Dependencies
# ====================
info "Installing system dependencies..."

sudo apt-get update -qq

PACKAGES=(
    # Core tools
    curl wget git git-lfs
    # Python
    python3 python3-pip python3-venv
    # Audio/Video
    ffmpeg
    # Security
    clamav clamav-daemon
    # Screen capture
    scrot imagemagick
    # OCR
    tesseract-ocr tesseract-ocr-spa tesseract-ocr-eng
    # PDF
    poppler-utils pandoc wkhtmltopdf
    # System monitoring
    htop nethogs
    # Notifications
    libnotify-bin
    # Network
    curl wget nmap
)

for pkg in "${PACKAGES[@]}"; do
    if ! dpkg -l "$pkg" &>/dev/null 2>&1; then
        sudo apt-get install -y -qq "$pkg" && success "Installed: $pkg" || warn "Failed to install: $pkg"
    else
        success "Already installed: $pkg"
    fi
done

# ====================
# 2. Python Environment
# ====================
info "Setting up Python environment..."

VENV_DIR="$HOME/.ideas-brillantes/venv"
mkdir -p "$HOME/.ideas-brillantes"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    success "Created virtualenv: $VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

pip install --quiet --upgrade pip

PYTHON_PACKAGES=(
    # Core
    "requests>=2.31.0"
    "httpx>=0.25.0"
    # Browser automation
    "playwright>=1.40.0"
    # Memory
    "chromadb>=0.4.0"
    "sentence-transformers>=2.2.0"
    # Audio/TTS
    "edge-tts>=6.1.9"
    "openai-whisper>=20231117"
    # Image generation (API)
    "Pillow>=10.0.0"
    "matplotlib>=3.7.0"
    # Documents
    "python-docx>=1.1.0"
    "openpyxl>=3.1.0"
    "python-pptx>=0.6.23"
    "reportlab>=4.0.0"
    # Google Workspace
    "google-auth-oauthlib>=1.2.0"
    "google-api-python-client>=2.110.0"
    "gspread>=6.0.0"
    # Database
    "psycopg2-binary>=2.9.0"
    "pymysql>=1.1.0"
    "pymongo>=4.6.0"
    "redis>=5.0.0"
    "supabase>=2.0.0"
    # Web
    "beautifulsoup4>=4.12.0"
    "aiohttp>=3.9.0"
    # Notifications
    "notify2>=0.3.1"
    # Security
    "python-magic>=0.4.27"
    # MCP
    "mcp>=0.1.0"
    # Email
    "icalendar>=5.0.0"
    "pytz>=2024.1"
)

info "Installing Python packages..."
pip install --quiet "${PYTHON_PACKAGES[@]}" && success "Python packages installed"

# Playwright browsers
info "Installing Playwright browsers..."
playwright install chromium && success "Playwright Chromium installed"

# ====================
# 3. Ollama
# ====================
info "Installing Ollama..."

if ! command -v ollama &>/dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
    success "Ollama installed"
else
    success "Ollama already installed: $(ollama --version 2>/dev/null || echo 'unknown version')"
fi

# Start Ollama service
if ! pgrep -x "ollama" > /dev/null; then
    ollama serve &>/dev/null &
    sleep 3
    success "Ollama service started"
fi

# ====================
# 4. ClamAV Update
# ====================
info "Updating ClamAV virus definitions..."
sudo freshclam 2>/dev/null && success "ClamAV updated" || warn "ClamAV update failed (may need sudo)"

# ====================
# 5. Directory Structure
# ====================
info "Creating directory structure..."

DIRS=(
    "$HOME/.ideas-brillantes"
    "$HOME/.ideas-brillantes/monitors"
    "$HOME/.ideas-brillantes/memory"
    "$HOME/Reports/security"
    "$HOME/Reports/code-reviews"
    "$HOME/Reports/weekly"
    "$HOME/Screenshots"
    "$HOME/Videos/generated"
    "$HOME/Music/tts"
    "$HOME/Backups"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$dir" && success "Created: $dir"
done

# ====================
# 6. Shell Integration (activate venv)
# ====================
info "Configuring shell integration..."

SHELL_RC="$HOME/.bashrc"
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

ALIAS_BLOCK="
# ideas-brillantes
alias ideas='source $VENV_DIR/bin/activate && ollama run ideas-brillantes'
export IDEAS_VENV='$VENV_DIR'
"

if ! grep -q "ideas-brillantes" "$SHELL_RC" 2>/dev/null; then
    echo "$ALIAS_BLOCK" >> "$SHELL_RC"
    success "Shell aliases added to $SHELL_RC"
fi

# ====================
# 7. Check if model exists in Ollama
# ====================
info "Checking if ideas-brillantes model exists in Ollama..."

if ollama list 2>/dev/null | grep -q "ideas-brillantes"; then
    success "Model 'ideas-brillantes' found in Ollama"
else
    warn "Model 'ideas-brillantes' not yet in Ollama"
    REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
    echo ""
    echo "  To create the model, run:"
    echo "  Option A (with pre-trained GGUF):"
    echo "    ollama create ideas-brillantes -f $REPO_DIR/model/Modelfile"
    echo ""
    echo "  Option B (fine-tune from scratch, requires GPU):"
    echo "    cd $REPO_DIR/training"
    echo "    python validate_dataset.py"
    echo "    python prepare_dataset.py"
    echo "    python finetune.py"
    echo "    python merge_and_export.py"
fi

# ====================
# Summary
# ====================
echo ""
echo "================================================"
success "Setup complete!"
echo ""
echo "  Quick start:"
echo "    source ~/.bashrc  (or restart terminal)"
echo "    ollama run ideas-brillantes"
echo ""
echo "  Or use the alias:"
echo "    ideas"
echo ""
echo "  Fine-tune the model:"
echo "    cd training/"
echo "    python finetune.py"
echo "================================================"
