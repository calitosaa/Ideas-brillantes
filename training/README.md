# Training Guide — ideas-brillantes

## Requisitos

### Hardware Mínimo
- GPU: NVIDIA con **≥16GB VRAM** (RTX 3090, 4090, A100, H100)
- RAM: ≥32GB
- Disco: ≥100GB libres (modelo base + adapters + merged + GGUF)

### Hardware Recomendado
- GPU: NVIDIA A100 40GB o 2× RTX 4090
- RAM: 64GB
- Disco SSD: 200GB+

### Software
```bash
# CUDA 12.1+
nvidia-smi  # verificar driver CUDA

# Python 3.10+
python3 --version
```

---

## Instalación de Dependencias

```bash
# Opción 1: Script automático
chmod +x ../scripts/install_training_deps.sh
../scripts/install_training_deps.sh

# Opción 2: Manual
pip install unsloth[cu121-torch230]
pip install transformers datasets trl peft bitsandbytes
pip install accelerate wandb tensorboard
pip install sentencepiece protobuf

# llama.cpp para exportar GGUF
git clone https://github.com/ggerganov/llama.cpp ~/llama.cpp
cd ~/llama.cpp && make -j$(nproc)
pip install -r ~/llama.cpp/requirements.txt
```

---

## Pipeline Completo

### Paso 1: Preparar el Dataset
```bash
cd training/

# Validar calidad de los JSONL
python validate_dataset.py

# Generar train.jsonl y val.jsonl (90/10 split)
python prepare_dataset.py
```

Salida esperada:
```
✅ 14 dataset files loaded
📊 Total examples: ~1,200
📊 Train: ~1,080 | Val: ~120
🎉 Dataset ready!
```

### Paso 2: Fine-tuning (LoRA sobre GLM-5-1)
```bash
# Dry-run (verifica config sin entrenar)
python finetune.py --dry-run

# Entrenamiento completo (~4-8 horas en A100)
python finetune.py

# Si tienes poco VRAM, usar parámetros más conservadores
python finetune.py --batch-size 1 --grad-accum 32

# Reanudar desde checkpoint si se interrumpió
python finetune.py --resume-from-checkpoint output/checkpoints/checkpoint-500
```

### Paso 3: Exportar el Modelo
```bash
# Mergear adapters + exportar GGUF Q4_K_M + crear en Ollama
python merge_and_export.py --verify

# Solo exportar GGUF (si el merge ya está hecho)
python merge_and_export.py --skip-merge --quantization q5_k_m

# Opciones de cuantización:
# q4_k_m — Recomendado: mejor balance calidad/tamaño (~5GB)
# q5_k_m — Mejor calidad, más grande (~6GB)
# q8_0   — Alta calidad, para GPUs con más memoria (~9GB)
# f16    — Sin cuantizar, máxima calidad (~18GB)
```

### Paso 4: Probar el Modelo
```bash
# Crear en Ollama (si no se hizo en paso 3)
ollama create ideas-brillantes -f ../model/Modelfile

# Tests básicos
ollama run ideas-brillantes "Hola, ¿qué puedes hacer?"
ollama run ideas-brillantes "Abre el terminal"
ollama run ideas-brillantes "Create a Material 3 button with BeerCSS"
ollama run ideas-brillantes "Cada hora revisa si hay actualizaciones"

# Test de tool call format
ollama run ideas-brillantes "Haz una captura de pantalla"
# Debe generar: <tool_call>{"name": "screenshot", "arguments": {...}}</tool_call>

# Test de seguridad proactiva
ollama run ideas-brillantes "Acabo de instalar un programa"
# Debe ofrecer escanear el ejecutable automáticamente

# Test bilingüe
ollama run ideas-brillantes "What can you help me with?"
# Debe responder EN inglés automáticamente
```

---

## Configuración de Training (finetune_config.yaml)

```yaml
base_model: THUDM/GLM-5-1

lora:
  r: 64              # rank — más alto = más capacidad, más VRAM
  alpha: 128         # escala los gradientes LoRA
  dropout: 0.05      # regularización leve
  target_modules:    # capas donde aplicar LoRA
    - q_proj
    - v_proj
    - k_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj

training:
  epochs: 3
  batch_size: 4      # reducir a 2 o 1 si hay OOM
  grad_accum: 8      # pasos para acumular gradientes
  learning_rate: 2e-4
  warmup_ratio: 0.03
  max_seq_length: 2048
  bf16: true         # usar bfloat16 en Ampere+ GPUs
```

---

## Monitoreo del Entrenamiento

```bash
# TensorBoard
tensorboard --logdir output/runs/

# Wandb (si configurado)
export WANDB_API_KEY=your_key
python finetune.py --wandb-project ideas-brillantes

# Checkpoints guardados en:
ls output/checkpoints/
```

---

## Estimación de Tiempo

| Hardware | Tiempo estimado |
|---|---|
| RTX 4090 (24GB) | ~4-6 horas |
| A100 40GB | ~2-3 horas |
| 2× A100 80GB | ~1-1.5 horas |
| RTX 3090 (24GB) | ~6-8 horas |
| CPU (sin GPU) | No recomendado (días) |

---

## Resolución de Problemas

### CUDA Out of Memory
```bash
# Reducir batch size
python finetune.py --batch-size 1 --grad-accum 32

# Usar 4-bit quantization más agresiva
# En finetune_config.yaml: load_in_4bit: true
```

### Training Loss No Baja
- Verifica que el dataset tiene formato correcto (`validate_dataset.py`)
- Prueba con learning_rate más bajo: 1e-4
- Verifica que los ejemplos son variados y de calidad

### Modelo Genera Respuestas Extrañas
- El template GLM-5-1 usa `[gMASK]<sop>` — verificar Modelfile
- Revisar stop tokens: `<|endoftext|>`, `<|user|>`, `<|assistant|>`
- Probar con temperatura más baja: `PARAMETER temperature 0.3`

### GGUF Export Falla
```bash
# Verificar llama.cpp está compilado
~/llama.cpp/llama-quantize --help

# Verificar que el modelo merged está completo
ls -la output/merged_model/
# Debe contener: config.json, tokenizer.json, *.safetensors
```

---

## Dataset Format Reference (ChatML para GLM-5-1)

```jsonl
{"messages": [
  {"role": "user", "content": "Pregunta del usuario"},
  {"role": "assistant", "content": "Respuesta del asistente"}
]}

{"messages": [
  {"role": "system", "content": "Contexto especial (opcional)"},
  {"role": "user", "content": "Pregunta"},
  {"role": "assistant", "content": "Respuesta con <tool_call>{\"name\": \"...\", \"arguments\": {...}}</tool_call>"}
]}
```

**Reglas críticas:**
- Cada línea es un JSON completo (JSONL = JSON Lines)
- El primer mensaje DEBE ser `"role": "user"` (o `"system"` seguido de `"user"`)
- El último mensaje DEBE ser `"role": "assistant"`
- Contenido no puede estar vacío
- Sin comas ni objetos al final del archivo
