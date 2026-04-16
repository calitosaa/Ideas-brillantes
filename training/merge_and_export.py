#!/usr/bin/env python3
"""
Merge LoRA adapters with base model and export to GGUF format.
Requires: unsloth, llama.cpp, CUDA GPU with ≥16GB VRAM.
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse

BASE_MODEL = "THUDM/GLM-5-1"
ADAPTER_PATH = "./output/lora_adapters"
MERGED_PATH = "./output/merged_model"
GGUF_PATH = "./output/ideas-brillantes.Q4_K_M.gguf"
OLLAMA_MODEL_NAME = "ideas-brillantes"
MODELFILE_PATH = "../model/Modelfile"


def check_gpu():
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            vram_mb = int(result.stdout.strip().replace(" MiB", ""))
            print(f"✅ GPU VRAM: {vram_mb // 1024}GB")
            if vram_mb < 8192:
                print("⚠️  Warning: <8GB VRAM. Export may fail. Use CPU offloading.")
            return True
    except FileNotFoundError:
        pass
    print("⚠️  nvidia-smi not found. Running on CPU (will be slow).")
    return False


def check_llama_cpp():
    """Check if llama.cpp's convert script is available."""
    paths_to_check = [
        "/opt/llama.cpp/convert-hf-to-gguf.py",
        "~/llama.cpp/convert-hf-to-gguf.py",
        "./llama.cpp/convert-hf-to-gguf.py",
    ]
    for p in paths_to_check:
        expanded = os.path.expanduser(p)
        if os.path.exists(expanded):
            return expanded
    return None


def merge_lora_adapters():
    """Merge LoRA adapters into the base model using Unsloth."""
    print("\n🔀 Merging LoRA adapters with base model...")

    script = f"""
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="{ADAPTER_PATH}",
    max_seq_length=32768,
    dtype=torch.float16,
    load_in_4bit=False,
)

print("Saving merged model...")
model.save_pretrained_merged(
    "{MERGED_PATH}",
    tokenizer,
    save_method="merged_16bit",
)
print("✅ Merged model saved to {MERGED_PATH}")
"""

    result = subprocess.run([sys.executable, "-c", script], capture_output=False)
    if result.returncode != 0:
        print("❌ Merge failed. Check that training was completed successfully.")
        return False
    return True


def export_to_gguf(quantization: str = "q4_k_m"):
    """Export merged model to GGUF format using llama.cpp."""
    print(f"\n📦 Exporting to GGUF ({quantization.upper()})...")

    convert_script = check_llama_cpp()
    if not convert_script:
        print("❌ llama.cpp not found. Install with:")
        print("   git clone https://github.com/ggerganov/llama.cpp ~/llama.cpp")
        print("   cd ~/llama.cpp && make")
        print("   pip install -r requirements.txt")
        return False

    # Step 1: Convert to float32 GGUF
    f32_path = GGUF_PATH.replace(".Q4_K_M.gguf", ".f32.gguf")

    convert_cmd = [
        sys.executable, convert_script,
        MERGED_PATH,
        "--outfile", f32_path,
        "--outtype", "f32"
    ]

    print(f"  Converting: {' '.join(convert_cmd)}")
    result = subprocess.run(convert_cmd, capture_output=False)
    if result.returncode != 0:
        print("❌ Conversion failed")
        return False

    # Step 2: Quantize
    quantize_binary = os.path.expanduser("~/llama.cpp/llama-quantize")
    if not os.path.exists(quantize_binary):
        quantize_binary = os.path.expanduser("~/llama.cpp/quantize")  # older name

    if os.path.exists(quantize_binary):
        quant_cmd = [quantize_binary, f32_path, GGUF_PATH, quantization.upper()]
        print(f"  Quantizing: {' '.join(quant_cmd)}")
        result = subprocess.run(quant_cmd, capture_output=False)
        if result.returncode != 0:
            print(f"❌ Quantization failed. The f32 GGUF is available at: {f32_path}")
            return False

        # Remove intermediate f32
        os.remove(f32_path)
        print(f"✅ GGUF saved: {GGUF_PATH}")
    else:
        print(f"⚠️  quantize binary not found. F32 GGUF available at: {f32_path}")
        print("   Rename it manually or build llama.cpp first.")
        return False

    return True


def create_ollama_model():
    """Create Ollama model from GGUF + Modelfile."""
    print(f"\n🦙 Creating Ollama model '{OLLAMA_MODEL_NAME}'...")

    if not Path(GGUF_PATH).exists():
        print(f"❌ GGUF not found: {GGUF_PATH}")
        return False

    modelfile_path = Path(__file__).parent.parent / "model" / "Modelfile"
    if not modelfile_path.exists():
        print(f"❌ Modelfile not found: {modelfile_path}")
        return False

    # Update GGUF path in Modelfile temporarily
    with open(modelfile_path) as f:
        modelfile_content = f.read()

    # Replace FROM line to point to local GGUF
    import re
    modified = re.sub(
        r'^FROM .*$',
        f'FROM {os.path.abspath(GGUF_PATH)}',
        modelfile_content,
        flags=re.MULTILINE
    )

    tmp_modelfile = "/tmp/ideas-brillantes-Modelfile"
    with open(tmp_modelfile, "w") as f:
        f.write(modified)

    result = subprocess.run(
        ["ollama", "create", OLLAMA_MODEL_NAME, "-f", tmp_modelfile],
        capture_output=False
    )

    os.remove(tmp_modelfile)

    if result.returncode != 0:
        print("❌ Ollama model creation failed")
        return False

    print(f"✅ Ollama model created: {OLLAMA_MODEL_NAME}")
    return True


def verify_model():
    """Run basic verification tests."""
    print(f"\n🧪 Verifying model '{OLLAMA_MODEL_NAME}'...")

    test_prompts = [
        ("Hola, ¿qué puedes hacer?", "ideas-brillantes"),
        ("Open the terminal", "tool_call"),
        ("Crea un botón Material 3", "button"),
    ]

    for prompt, expected_keyword in test_prompts:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL_NAME, prompt],
            capture_output=True, text=True, timeout=60
        )

        output = result.stdout.lower()
        if expected_keyword.lower() in output or result.returncode == 0:
            print(f"  ✅ '{prompt[:40]}...'")
        else:
            print(f"  ⚠️  '{prompt[:40]}...' — Response may be unexpected")
            print(f"      Got: {result.stdout[:100]}")


def main():
    parser = argparse.ArgumentParser(description="Merge LoRA adapters and export to GGUF")
    parser.add_argument("--skip-merge", action="store_true", help="Skip merging (use existing merged model)")
    parser.add_argument("--skip-gguf", action="store_true", help="Skip GGUF export")
    parser.add_argument("--skip-ollama", action="store_true", help="Skip Ollama model creation")
    parser.add_argument("--quantization", default="q4_k_m", choices=["q4_k_m", "q5_k_m", "q8_0", "f16"],
                       help="GGUF quantization type")
    parser.add_argument("--verify", action="store_true", help="Run verification tests")
    args = parser.parse_args()

    print("🚀 ideas-brillantes — Merge & Export Pipeline")
    print("=" * 50)
    check_gpu()

    # Check adapter exists
    if not args.skip_merge and not Path(ADAPTER_PATH).exists():
        print(f"❌ LoRA adapters not found at: {ADAPTER_PATH}")
        print("   Run finetune.py first to generate adapters.")
        return 1

    # Step 1: Merge LoRA
    if not args.skip_merge:
        if not merge_lora_adapters():
            return 1
    else:
        print("⏭️  Skipping merge (using existing)")

    # Step 2: Export GGUF
    if not args.skip_gguf:
        if not export_to_gguf(args.quantization):
            return 1
    else:
        print("⏭️  Skipping GGUF export")

    # Step 3: Create Ollama model
    if not args.skip_ollama:
        if not create_ollama_model():
            return 1
    else:
        print("⏭️  Skipping Ollama model creation")

    # Step 4: Verify
    if args.verify:
        verify_model()

    print("\n" + "=" * 50)
    print("🎉 Export complete!")
    print(f"\n📋 Run the model:")
    print(f"   ollama run {OLLAMA_MODEL_NAME}")
    print(f"\n📋 Test it:")
    print(f"   ollama run {OLLAMA_MODEL_NAME} 'Hola, ¿qué puedes hacer?'")
    print(f"   ollama run {OLLAMA_MODEL_NAME} 'Abre el terminal'")
    print(f"   ollama run {OLLAMA_MODEL_NAME} 'Create a Material 3 button'")

    return 0


if __name__ == "__main__":
    sys.exit(main())
