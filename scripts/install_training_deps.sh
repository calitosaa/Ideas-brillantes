#!/bin/bash
# Install training dependencies for ideas-brillantes fine-tuning
# Requires: NVIDIA GPU with CUDA 11.8+ or 12.1+

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo "🧠 ideas-brillantes — Training Dependencies Installer"
echo "======================================================"

# Check GPU
echo ""
echo "Checking GPU..."
if ! command -v nvidia-smi &>/dev/null; then
    warn "nvidia-smi not found. Training will run on CPU (very slow)."
else
    VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader | head -1 | tr -d ' MiB')
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
    ok "GPU: $GPU_NAME (${VRAM}MB VRAM)"

    CUDA_VER=$(nvcc --version 2>/dev/null | grep "release" | awk '{print $5}' | tr -d ',' || echo "unknown")
    ok "CUDA: $CUDA_VER"

    if [ "$VRAM" -lt 8000 ]; then
        warn "Less than 8GB VRAM detected. Use --load_in_4bit and batch_size=1"
    fi
fi

# Detect CUDA version for correct Unsloth install
CUDA_SHORT=$(nvcc --version 2>/dev/null | grep "release" | awk '{print $5}' | tr -d ',' | tr -d '.' | cut -c1-3 || echo "121")

echo ""
echo "Installing Unsloth and training stack..."
echo "(This may take 5-15 minutes depending on bandwidth)"

# 1. PyTorch with CUDA
if [ "$CUDA_SHORT" = "118" ]; then
    pip install torch==2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
elif [ "$CUDA_SHORT" = "121" ] || [ "$CUDA_SHORT" = "122" ]; then
    pip install torch==2.3.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
else
    warn "Unknown CUDA version, installing torch for cu121"
    pip install torch==2.3.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
fi
ok "PyTorch installed"

# 2. Unsloth (2x faster LoRA training)
echo "Installing Unsloth..."
if [ "$CUDA_SHORT" = "118" ]; then
    pip install "unsloth[cu118-torch210]"
else
    pip install "unsloth[cu121-torch230]"
fi
ok "Unsloth installed"

# 3. Training libraries
pip install \
    transformers>=4.38.0 \
    datasets>=2.16.0 \
    trl>=0.7.9 \
    peft>=0.8.0 \
    bitsandbytes>=0.43.0 \
    accelerate>=0.26.0
ok "Transformers/TRL/PEFT stack installed"

# 4. Monitoring & logging
pip install \
    wandb>=0.16.0 \
    tensorboard>=2.15.0 \
    tqdm>=4.66.0
ok "Monitoring tools installed"

# 5. Data processing
pip install \
    sentencepiece>=0.1.99 \
    protobuf>=4.25.0 \
    tokenizers>=0.15.0
ok "Tokenizers installed"

# 6. llama.cpp for GGUF export
echo ""
echo "Installing llama.cpp for GGUF export..."

LLAMA_DIR="$HOME/llama.cpp"

if [ ! -d "$LLAMA_DIR" ]; then
    git clone --depth 1 https://github.com/ggerganov/llama.cpp "$LLAMA_DIR"
    ok "llama.cpp cloned"
else
    cd "$LLAMA_DIR" && git pull --quiet
    ok "llama.cpp updated"
fi

# Build llama.cpp
cd "$LLAMA_DIR"
if command -v nvcc &>/dev/null; then
    echo "Building with CUDA support..."
    LLAMA_CUDA=1 make -j$(nproc) -s 2>&1 | tail -5
    ok "llama.cpp built with CUDA"
else
    make -j$(nproc) -s 2>&1 | tail -5
    ok "llama.cpp built (CPU only)"
fi

# Install Python requirements for convert script
pip install -r "$LLAMA_DIR/requirements.txt" -q
ok "llama.cpp Python requirements installed"

# 7. Optional: DeepSpeed for multi-GPU
if [ "$(nvidia-smi -L 2>/dev/null | wc -l)" -gt 1 ]; then
    echo "Multiple GPUs detected, installing DeepSpeed..."
    pip install deepspeed>=0.13.0
    ok "DeepSpeed installed"
fi

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "
import torch
import transformers
import peft
import trl
print(f'  torch: {torch.__version__}')
print(f'  transformers: {transformers.__version__}')
print(f'  peft: {peft.__version__}')
print(f'  trl: {trl.__version__}')
print(f'  CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'  GPU: {torch.cuda.get_device_name(0)}')
    print(f'  VRAM: {torch.cuda.get_device_properties(0).total_memory // 1024**3}GB')
"

# Memory estimate
echo ""
echo "================================================"
ok "Training dependencies installed!"
echo ""
echo "📊 Estimated memory for GLM-5-1 fine-tuning:"
echo "   LoRA rank=64, QLoRA 4-bit: ~12-14GB VRAM"
echo "   LoRA rank=32, QLoRA 4-bit: ~10-12GB VRAM"
echo "   LoRA rank=64, bf16:        ~18-20GB VRAM"
echo ""
echo "📋 Next steps:"
echo "   cd training/"
echo "   python validate_dataset.py"
echo "   python prepare_dataset.py"
echo "   python finetune.py --dry-run"
echo "   python finetune.py"
echo "================================================"
