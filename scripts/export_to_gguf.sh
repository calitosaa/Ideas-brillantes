#!/bin/bash
# Export ideas-brillantes fine-tuned model to GGUF format and register in Ollama
# Usage: ./export_to_gguf.sh [quantization] [adapter_path]
# Example: ./export_to_gguf.sh q4_k_m ./training/output/lora_adapters

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

QUANTIZATION="${1:-q4_k_m}"
ADAPTER_PATH="${2:-./training/output/lora_adapters}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$REPO_DIR/training/output"
MERGED_DIR="$OUTPUT_DIR/merged_model"
GGUF_PATH="$OUTPUT_DIR/ideas-brillantes.${QUANTIZATION}.gguf"
LLAMA_CPP="$HOME/llama.cpp"
MODEL_NAME="ideas-brillantes"

echo "🔧 ideas-brillantes GGUF Export"
echo "======================================"
echo "  Adapter:       $ADAPTER_PATH"
echo "  Quantization:  $QUANTIZATION"
echo "  Output:        $GGUF_PATH"
echo ""

# Checks
[ -d "$ADAPTER_PATH" ] || err "Adapter path not found: $ADAPTER_PATH. Run finetune.py first."
[ -d "$LLAMA_CPP" ] || err "llama.cpp not found at $HOME/llama.cpp. Run install_training_deps.sh first."
command -v ollama &>/dev/null || err "Ollama not installed. Run setup.sh first."

mkdir -p "$OUTPUT_DIR"

# Step 1: Merge LoRA into base model
echo "Step 1/4: Merging LoRA adapters..."
python3 "$REPO_DIR/training/merge_and_export.py" \
    --skip-gguf \
    --skip-ollama \
    2>&1
ok "Merge complete: $MERGED_DIR"

# Step 2: Convert to f32 GGUF
echo ""
echo "Step 2/4: Converting to GGUF (float32)..."
F32_PATH="$OUTPUT_DIR/ideas-brillantes.f32.gguf"

python3 "$LLAMA_CPP/convert-hf-to-gguf.py" \
    "$MERGED_DIR" \
    --outfile "$F32_PATH" \
    --outtype f32
ok "F32 GGUF: $F32_PATH"

# Step 3: Quantize
echo ""
echo "Step 3/4: Quantizing to $QUANTIZATION..."

QUANTIZE_BIN="$LLAMA_CPP/llama-quantize"
[ -f "$QUANTIZE_BIN" ] || QUANTIZE_BIN="$LLAMA_CPP/quantize"  # older name

if [ ! -f "$QUANTIZE_BIN" ]; then
    warn "Quantize binary not found. Using F32 GGUF as-is."
    GGUF_PATH="$F32_PATH"
else
    "$QUANTIZE_BIN" "$F32_PATH" "$GGUF_PATH" "${QUANTIZATION^^}"
    rm -f "$F32_PATH"
    ok "Quantized GGUF: $GGUF_PATH ($(du -sh "$GGUF_PATH" | cut -f1))"
fi

# Step 4: Register in Ollama
echo ""
echo "Step 4/4: Registering in Ollama..."

MODELFILE_TMP="/tmp/ideas-brillantes-Modelfile-$$"
MODELFILE_SRC="$REPO_DIR/model/Modelfile"

# Replace FROM line with absolute GGUF path
sed "s|^FROM .*|FROM $GGUF_PATH|" "$MODELFILE_SRC" > "$MODELFILE_TMP"

ollama create "$MODEL_NAME" -f "$MODELFILE_TMP"
rm -f "$MODELFILE_TMP"
ok "Ollama model '$MODEL_NAME' created"

# Quick verification
echo ""
echo "Running quick verification tests..."

TESTS_PASSED=0
TESTS_TOTAL=3

run_test() {
    local prompt="$1"
    local expected="$2"

    response=$(ollama run "$MODEL_NAME" "$prompt" 2>/dev/null | head -5)

    if [ -n "$response" ]; then
        echo "  ✅ '$prompt'"
        ((TESTS_PASSED++))
    else
        echo "  ❌ '$prompt' — No response"
    fi
}

run_test "Hola" "greeting"
run_test "Open the terminal" "tool"
run_test "What can you do?" "capabilities"

echo ""
echo "======================================"
ok "Export complete!"
echo ""
echo "  Model:  $MODEL_NAME"
echo "  GGUF:   $GGUF_PATH"
echo "  Size:   $(du -sh "$GGUF_PATH" | cut -f1)"
echo "  Tests:  $TESTS_PASSED/$TESTS_TOTAL passed"
echo ""
echo "  Run: ollama run $MODEL_NAME"
echo ""
echo "  Full test suite:"
echo "    ollama run $MODEL_NAME 'Hola, ¿qué puedes hacer?'"
echo "    ollama run $MODEL_NAME 'Abre el terminal'"
echo "    ollama run $MODEL_NAME 'Cada hora verifica el sistema'"
echo "    ollama run $MODEL_NAME 'Create a Material 3 card'"
echo "======================================"
