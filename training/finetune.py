#!/usr/bin/env python3
"""
ideas-brillantes Fine-tuning Script
Uses Unsloth for efficient LoRA/QLoRA training on GLM-5-1

Usage:
    python training/finetune.py
    python training/finetune.py --dry-run          # Validate config only
    python training/finetune.py --config custom.yaml
    python training/finetune.py --resume-from-checkpoint output/checkpoints/checkpoint-500
"""

import argparse
import json
import os
import sys
from pathlib import Path

import yaml


def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune GLM-5-1 for ideas-brillantes")
    parser.add_argument("--config", default="training/finetune_config.yaml", help="Config file path")
    parser.add_argument("--dry-run", action="store_true", help="Validate config and dataset without training")
    parser.add_argument("--resume-from-checkpoint", default=None, help="Resume from checkpoint path")
    parser.add_argument("--dataset-only", action="store_true", help="Only prepare dataset, don't train")
    return parser.parse_args()


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def check_gpu():
    """Check GPU availability and VRAM."""
    try:
        import torch
        if not torch.cuda.is_available():
            print("❌ No CUDA GPU detected. Fine-tuning requires GPU.")
            print("   For CPU inference only, use the Modelfile with Ollama.")
            sys.exit(1)

        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"✅ GPU: {gpu_name} ({vram_gb:.1f}GB VRAM)")

        if vram_gb < 14:
            print(f"⚠️  Warning: {vram_gb:.1f}GB VRAM may be insufficient.")
            print("   Minimum recommended: 16GB. Training may OOM.")
        elif vram_gb >= 24:
            print("✅ Sufficient VRAM for full fp16 training")
        else:
            print("✅ Sufficient VRAM for QLoRA (4-bit) training")

        return vram_gb
    except ImportError:
        print("❌ PyTorch not installed. Run: ./scripts/install_training_deps.sh")
        sys.exit(1)


def load_dataset(config: dict) -> list:
    """Load and combine all JSONL dataset files."""
    dataset_dir = Path(config["data"]["dataset_dir"])
    all_examples = []
    stats = {}

    for filename in config["data"]["dataset_files"]:
        filepath = dataset_dir / filename
        if not filepath.exists():
            print(f"⚠️  Dataset file not found: {filepath}")
            print("   Run: python training/prepare_dataset.py")
            continue

        examples = []
        with open(filepath) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    example = json.loads(line)
                    examples.append(example)
                except json.JSONDecodeError as e:
                    print(f"⚠️  Invalid JSON in {filename} line {line_num}: {e}")

        stats[filename] = len(examples)
        all_examples.extend(examples)
        print(f"   📄 {filename}: {len(examples)} examples")

    total = len(all_examples)
    print(f"\n✅ Total training examples: {total:,}")

    if total < 100:
        print("⚠️  Very few examples. Run prepare_dataset.py to generate more.")

    return all_examples, stats


def validate_examples(examples: list, max_seq_length: int = 4096) -> tuple:
    """Validate dataset format and statistics."""
    valid = []
    invalid = []
    token_lengths = []

    for i, example in enumerate(examples):
        if "messages" not in example:
            invalid.append((i, "Missing 'messages' key"))
            continue

        messages = example["messages"]
        if not isinstance(messages, list) or len(messages) < 2:
            invalid.append((i, "messages must be list with >= 2 items"))
            continue

        # Check message structure
        has_user = any(m.get("role") == "user" for m in messages)
        has_assistant = any(m.get("role") == "assistant" for m in messages)

        if not has_user or not has_assistant:
            invalid.append((i, "Must have both user and assistant messages"))
            continue

        # Estimate token length (rough: 4 chars per token)
        total_chars = sum(len(m.get("content", "")) for m in messages)
        estimated_tokens = total_chars // 4
        token_lengths.append(estimated_tokens)

        if estimated_tokens > max_seq_length:
            invalid.append((i, f"Estimated {estimated_tokens} tokens > max {max_seq_length}"))
            continue

        valid.append(example)

    return valid, invalid, token_lengths


def format_for_glm5(examples: list) -> list:
    """Format examples in ChatML format for GLM-4."""
    formatted = []
    for example in examples:
        messages = example["messages"]

        # Build ChatML string
        text = ""
        if "system" in example:
            text += f"[gMASK]<sop><|system|>\n{example['system']}\n"

        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                text += f"<|user|>\n{content}\n"
            elif role == "assistant":
                text += f"<|assistant|>\n{content}\n"

        formatted.append({"text": text, "messages": messages})

    return formatted


def train(config: dict, examples: list, resume_from: str = None):
    """Run the actual fine-tuning."""
    try:
        from unsloth import FastLanguageModel
        from trl import SFTTrainer, SFTConfig
        from datasets import Dataset
        import torch
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: ./scripts/install_training_deps.sh")
        sys.exit(1)

    print("\n🔧 Loading base model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=config["model"]["name"],
        max_seq_length=config["data"]["max_seq_length"],
        dtype=torch.float16,
        load_in_4bit=config["model"]["load_in_4bit"],
        trust_remote_code=config["model"]["trust_remote_code"],
    )

    print("🔧 Adding LoRA adapters...")
    lora_cfg = config["lora"]
    model = FastLanguageModel.get_peft_model(
        model,
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["lora_alpha"],
        lora_dropout=lora_cfg["lora_dropout"],
        target_modules=lora_cfg["target_modules"],
        bias=lora_cfg["bias"],
        use_rslora=lora_cfg.get("use_rslora", True),
        use_gradient_checkpointing="unsloth",
    )

    print(f"✅ Model loaded. Trainable params: {model.num_parameters(only_trainable=True):,}")

    # Prepare dataset
    print("\n📦 Preparing dataset...")
    formatted = format_for_glm5(examples)

    # Split train/val
    val_size = int(len(formatted) * config["data"]["val_split_ratio"])
    train_data = formatted[val_size:]
    val_data = formatted[:val_size]

    train_dataset = Dataset.from_list(train_data)
    val_dataset = Dataset.from_list(val_data)

    print(f"   Train: {len(train_dataset):,} examples")
    print(f"   Val:   {len(val_dataset):,} examples")

    # Training arguments
    t_cfg = config["training"]
    training_args = SFTConfig(
        output_dir=t_cfg["output_dir"],
        num_train_epochs=t_cfg["num_train_epochs"],
        per_device_train_batch_size=t_cfg["per_device_train_batch_size"],
        per_device_eval_batch_size=t_cfg["per_device_eval_batch_size"],
        gradient_accumulation_steps=t_cfg["gradient_accumulation_steps"],
        learning_rate=t_cfg["learning_rate"],
        lr_scheduler_type=t_cfg["lr_scheduler_type"],
        warmup_ratio=t_cfg["warmup_ratio"],
        weight_decay=t_cfg["weight_decay"],
        max_grad_norm=t_cfg["max_grad_norm"],
        fp16=t_cfg["fp16"],
        evaluation_strategy=t_cfg["evaluation_strategy"],
        eval_steps=t_cfg["eval_steps"],
        save_strategy=t_cfg["save_strategy"],
        save_steps=t_cfg["save_steps"],
        save_total_limit=t_cfg["save_total_limit"],
        load_best_model_at_end=t_cfg["load_best_model_at_end"],
        logging_steps=t_cfg["logging_steps"],
        report_to=t_cfg.get("report_to", ["tensorboard"]),
        dataloader_num_workers=t_cfg["dataloader_num_workers"],
        group_by_length=t_cfg["group_by_length"],
        optim=t_cfg.get("optim", "adamw_8bit"),
        max_seq_length=config["data"]["max_seq_length"],
        dataset_text_field="text",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        args=training_args,
    )

    print("\n🚀 Starting training...")
    print(f"   Epochs: {t_cfg['num_train_epochs']}")
    print(f"   Effective batch size: {t_cfg['per_device_train_batch_size'] * t_cfg['gradient_accumulation_steps']}")
    print(f"   Learning rate: {t_cfg['learning_rate']}")
    print(f"   Output: {t_cfg['output_dir']}\n")

    trainer.train(resume_from_checkpoint=resume_from)

    print("\n✅ Training complete!")
    return model, tokenizer


def export_model(model, tokenizer, config: dict):
    """Merge LoRA and export to GGUF."""
    export_cfg = config["export"]

    if export_cfg.get("merge_adapter", True):
        print("\n🔧 Merging LoRA adapters into base model...")
        from unsloth import FastLanguageModel
        model.save_pretrained_merged(
            export_cfg["output_dir"],
            tokenizer,
            save_method="merged_16bit",
        )
        print(f"✅ Merged model saved to: {export_cfg['output_dir']}")

    if export_cfg.get("save_gguf", True):
        print(f"\n🔧 Exporting to GGUF ({export_cfg['gguf_quantization']})...")
        gguf_dir = Path(export_cfg["gguf_output"]).parent
        gguf_dir.mkdir(parents=True, exist_ok=True)

        model.save_pretrained_gguf(
            export_cfg["gguf_output"].replace(".gguf", ""),
            tokenizer,
            quantization_method=export_cfg["gguf_quantization"].lower(),
        )
        print(f"✅ GGUF exported to: {export_cfg['gguf_output']}")
        print(f"\n📋 To use with Ollama:")
        print(f"   ollama create ideas-brillantes -f model/Modelfile")


def main():
    args = parse_args()

    print("=" * 60)
    print("  ideas-brillantes Fine-tuning")
    print("  Base: GLM-5-1 + LoRA")
    print("=" * 60)

    # Load config
    print(f"\n📋 Loading config: {args.config}")
    config = load_config(args.config)

    if args.dry_run:
        print("\n🔍 DRY RUN MODE — validating without training\n")

    # Check GPU
    print("\n🖥️  Checking GPU...")
    vram_gb = check_gpu()

    # Adjust config for available VRAM
    if vram_gb < 20 and not args.dry_run:
        print("   Adjusting config for limited VRAM...")
        config["model"]["load_in_4bit"] = True
        config["training"]["per_device_train_batch_size"] = 2

    # Load dataset
    print(f"\n📦 Loading dataset from {config['data']['dataset_dir']}/")
    examples, stats = load_dataset(config)

    if not examples:
        print("❌ No training examples found. Run: python training/prepare_dataset.py")
        sys.exit(1)

    # Validate
    print("\n🔍 Validating examples...")
    valid, invalid, lengths = validate_examples(examples, config["data"]["max_seq_length"])

    print(f"   Valid:   {len(valid):,}")
    print(f"   Invalid: {len(invalid):,}")
    if lengths:
        import statistics
        print(f"   Avg tokens (estimated): {statistics.mean(lengths):.0f}")
        print(f"   Max tokens (estimated): {max(lengths)}")

    if invalid:
        print(f"\n⚠️  {len(invalid)} invalid examples:")
        for idx, reason in invalid[:5]:
            print(f"   [{idx}] {reason}")
        if len(invalid) > 5:
            print(f"   ... and {len(invalid) - 5} more")

    if args.dry_run:
        print("\n✅ Dry run complete. Config and dataset are valid.")
        print(f"   Ready to train with {len(valid):,} examples.")
        print(f"   Estimated training time: {len(valid) * 3 // 3600 + 1}+ hours on RTX 4090")
        return

    if args.dataset_only:
        print("\n✅ Dataset prepared successfully.")
        return

    # Train
    model, tokenizer = train(config, valid, resume_from=args.resume_from_checkpoint)

    # Export
    export_model(model, tokenizer, config)

    print("\n" + "=" * 60)
    print("  ✅ ideas-brillantes training complete!")
    print(f"  Model: {config['export']['output_dir']}")
    print(f"  GGUF:  {config['export']['gguf_output']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
