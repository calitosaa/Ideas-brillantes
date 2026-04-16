#!/usr/bin/env python3
"""
Dataset preparation script for ideas-brillantes fine-tuning.
Reads all JSONL files, validates, deduplicates, and merges into train/val splits.
"""

import json
import random
import os
import hashlib
from pathlib import Path
from collections import Counter

DATASET_DIR = Path(__file__).parent / "dataset"
OUTPUT_DIR = Path(__file__).parent / "dataset"

EXPECTED_FILES = [
    "pc_control_linux.jsonl",
    "browser_web.jsonl",
    "automation_workflows.jsonl",
    "ui_design_material3.jsonl",
    "code_engineering.jsonl",
    "security_antivirus.jsonl",
    "memory_context.jsonl",
    "content_media.jsonl",
    "research_knowledge.jsonl",
    "communication.jsonl",
    "devops_linux.jsonl",
    "multiagent_swarms.jsonl",
    "methodology_skills.jsonl",
    "bilingual_examples.jsonl",
]


def load_jsonl(filepath: Path) -> list[dict]:
    examples = []
    with open(filepath, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                examples.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  ⚠️  JSON error in {filepath.name}:{line_num}: {e}")
    return examples


def validate_example(example: dict, filepath: str, line_num: int) -> bool:
    if "messages" not in example:
        print(f"  ❌ Missing 'messages' key in {filepath}:{line_num}")
        return False

    messages = example["messages"]
    if not isinstance(messages, list) or len(messages) < 2:
        print(f"  ❌ 'messages' must be a list with ≥2 items in {filepath}:{line_num}")
        return False

    for i, msg in enumerate(messages):
        if "role" not in msg or "content" not in msg:
            print(f"  ❌ Message {i} missing 'role' or 'content' in {filepath}:{line_num}")
            return False
        if msg["role"] not in ("user", "assistant", "system"):
            print(f"  ❌ Invalid role '{msg['role']}' in {filepath}:{line_num}")
            return False
        if not isinstance(msg["content"], str) or not msg["content"].strip():
            print(f"  ❌ Empty content in message {i} in {filepath}:{line_num}")
            return False

    if messages[0]["role"] != "user":
        print(f"  ⚠️  First message should be 'user' role in {filepath}:{line_num}")

    return True


def deduplicate(examples: list[dict]) -> tuple[list[dict], int]:
    seen_hashes = set()
    unique = []
    dupes = 0
    for ex in examples:
        # Hash based on user message content
        user_content = " ".join(
            m["content"] for m in ex["messages"] if m["role"] == "user"
        )
        h = hashlib.md5(user_content.encode()).hexdigest()
        if h not in seen_hashes:
            seen_hashes.add(h)
            unique.append(ex)
        else:
            dupes += 1
    return unique, dupes


def format_for_glm5(example: dict) -> dict:
    """Convert ChatML format to GLM-5-1 format."""
    messages = example["messages"]
    formatted = {"messages": []}

    for msg in messages:
        formatted["messages"].append({
            "role": msg["role"],
            "content": msg["content"]
        })

    return formatted


def compute_stats(examples: list[dict]) -> dict:
    total_tokens_estimate = 0
    user_lengths = []
    assistant_lengths = []

    for ex in examples:
        for msg in ex["messages"]:
            tokens = len(msg["content"]) // 4  # rough estimate
            total_tokens_estimate += tokens
            if msg["role"] == "user":
                user_lengths.append(len(msg["content"]))
            elif msg["role"] == "assistant":
                assistant_lengths.append(len(msg["content"]))

    return {
        "total_examples": len(examples),
        "estimated_tokens": total_tokens_estimate,
        "avg_user_length": sum(user_lengths) / len(user_lengths) if user_lengths else 0,
        "avg_assistant_length": sum(assistant_lengths) / len(assistant_lengths) if assistant_lengths else 0,
    }


def main():
    print("🔧 ideas-brillantes Dataset Preparation")
    print("=" * 50)

    all_examples = []
    category_counts = {}
    errors = 0

    # Load and validate all dataset files
    for filename in EXPECTED_FILES:
        filepath = DATASET_DIR / filename
        if not filepath.exists():
            print(f"  ⚠️  Missing: {filename}")
            continue

        examples = load_jsonl(filepath)
        valid = []
        for i, ex in enumerate(examples):
            if validate_example(ex, filename, i + 1):
                valid.append(ex)
                # Tag with category
                ex["_category"] = filename.replace(".jsonl", "")
            else:
                errors += 1

        category_counts[filename] = len(valid)
        all_examples.extend(valid)
        print(f"  ✅ {filename}: {len(valid)} examples")

    print(f"\n📊 Total before deduplication: {len(all_examples)}")

    # Deduplicate
    all_examples, dupes = deduplicate(all_examples)
    print(f"📊 After deduplication: {len(all_examples)} (removed {dupes} dupes)")

    # Shuffle
    random.seed(42)
    random.shuffle(all_examples)

    # Remove internal _category tag before saving
    for ex in all_examples:
        ex.pop("_category", None)

    # Train/validation split (90/10)
    split_idx = int(len(all_examples) * 0.9)
    train_examples = all_examples[:split_idx]
    val_examples = all_examples[split_idx:]

    # Save splits
    train_path = OUTPUT_DIR / "train.jsonl"
    val_path = OUTPUT_DIR / "val.jsonl"

    with open(train_path, "w", encoding="utf-8") as f:
        for ex in train_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for ex in val_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    # Stats
    stats = compute_stats(all_examples)
    print("\n📈 Dataset Statistics:")
    print(f"  Total examples:        {stats['total_examples']}")
    print(f"  Train split:           {len(train_examples)}")
    print(f"  Validation split:      {len(val_examples)}")
    print(f"  Estimated tokens:      {stats['estimated_tokens']:,}")
    print(f"  Avg user msg length:   {stats['avg_user_length']:.0f} chars")
    print(f"  Avg assistant length:  {stats['avg_assistant_length']:.0f} chars")
    print(f"  Validation errors:     {errors}")

    print("\n📂 Category breakdown:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        bar = "█" * (count // 2)
        print(f"  {cat:<40} {count:>4}  {bar}")

    print(f"\n✅ Saved: {train_path}")
    print(f"✅ Saved: {val_path}")

    if errors > 0:
        print(f"\n⚠️  {errors} validation errors found. Run validate_dataset.py for details.")
        return 1

    print("\n🎉 Dataset ready for fine-tuning!")
    return 0


if __name__ == "__main__":
    exit(main())
