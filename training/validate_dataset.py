#!/usr/bin/env python3
"""
Dataset quality validation for ideas-brillantes.
Checks format, length, balance, and quality metrics.
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

DATASET_DIR = Path(__file__).parent / "dataset"
MAX_TOKENS_PER_EXAMPLE = 4096  # GLM-4 context limit for training
MIN_TOKENS_PER_EXAMPLE = 20
MIN_EXAMPLES_PER_CATEGORY = 10

ISSUES = []
WARNINGS = []


def report_issue(level: str, file: str, line: int, message: str):
    entry = f"  [{level}] {file}:{line} — {message}"
    if level == "ERROR":
        ISSUES.append(entry)
    else:
        WARNINGS.append(entry)


def estimate_tokens(text: str) -> int:
    return len(text) // 4


def check_tool_call_format(content: str, file: str, line: int):
    """Check tool_call JSON is valid."""
    import re
    tool_calls = re.findall(r'<tool_call>(.*?)</tool_call>', content, re.DOTALL)
    for tc in tool_calls:
        try:
            parsed = json.loads(tc.strip())
            if "name" not in parsed:
                report_issue("WARNING", file, line, f"tool_call missing 'name': {tc[:50]}")
        except json.JSONDecodeError:
            report_issue("ERROR", file, line, f"Invalid JSON in tool_call: {tc[:50]}")


def validate_file(filepath: Path) -> dict:
    stats = {
        "name": filepath.name,
        "total": 0,
        "valid": 0,
        "too_long": 0,
        "too_short": 0,
        "languages": Counter(),
        "has_tool_calls": 0,
    }

    with open(filepath, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            stats["total"] += 1

            # JSON validity
            try:
                example = json.loads(line)
            except json.JSONDecodeError as e:
                report_issue("ERROR", filepath.name, line_num, f"JSON decode error: {e}")
                continue

            # Structure
            if "messages" not in example:
                report_issue("ERROR", filepath.name, line_num, "Missing 'messages' key")
                continue

            messages = example["messages"]
            if not isinstance(messages, list):
                report_issue("ERROR", filepath.name, line_num, "'messages' must be a list")
                continue

            if len(messages) < 2:
                report_issue("ERROR", filepath.name, line_num, "Must have ≥2 messages")
                continue

            # Role checks
            roles = [m.get("role", "") for m in messages]
            if roles[0] != "user":
                report_issue("WARNING", filepath.name, line_num, "First message should be 'user'")

            valid_roles = {"user", "assistant", "system"}
            for i, (msg, role) in enumerate(zip(messages, roles)):
                if role not in valid_roles:
                    report_issue("ERROR", filepath.name, line_num, f"Invalid role '{role}' in message {i}")

                content = msg.get("content", "")
                if not content or not content.strip():
                    report_issue("ERROR", filepath.name, line_num, f"Empty content in message {i}")

                # Check tool_call format in assistant messages
                if role == "assistant" and "<tool_call>" in content:
                    stats["has_tool_calls"] += 1
                    check_tool_call_format(content, filepath.name, line_num)

            # Token length check
            total_content = " ".join(m.get("content", "") for m in messages)
            tokens = estimate_tokens(total_content)

            if tokens > MAX_TOKENS_PER_EXAMPLE:
                stats["too_long"] += 1
                report_issue("WARNING", filepath.name, line_num,
                             f"Example too long: ~{tokens} tokens (max {MAX_TOKENS_PER_EXAMPLE})")

            if tokens < MIN_TOKENS_PER_EXAMPLE:
                stats["too_short"] += 1
                report_issue("WARNING", filepath.name, line_num,
                             f"Example very short: ~{tokens} tokens")

            # Language detection (basic)
            user_content = " ".join(m["content"] for m in messages if m["role"] == "user")
            spanish_words = sum(1 for w in ["el", "la", "los", "las", "de", "que", "en", "un", "una", "por", "con", "para"] if f" {w} " in user_content.lower())
            if spanish_words >= 2:
                stats["languages"]["es"] += 1
            else:
                stats["languages"]["en"] += 1

            stats["valid"] += 1

    return stats


def check_balance(all_stats: list[dict]):
    """Check dataset balance across categories."""
    counts = {s["name"]: s["valid"] for s in all_stats}
    total = sum(counts.values())

    if total == 0:
        report_issue("ERROR", "dataset", 0, "No valid examples found!")
        return

    # Check minimum per category
    for name, count in counts.items():
        if count < MIN_EXAMPLES_PER_CATEGORY:
            report_issue("WARNING", name, 0,
                        f"Only {count} valid examples (minimum recommended: {MIN_EXAMPLES_PER_CATEGORY})")

    # Check language balance
    total_es = sum(s["languages"]["es"] for s in all_stats)
    total_en = sum(s["languages"]["en"] for s in all_stats)
    es_ratio = total_es / total if total > 0 else 0

    if es_ratio < 0.2:
        report_issue("WARNING", "dataset", 0, f"Low Spanish examples: {es_ratio:.1%} (recommended: >20%)")
    if es_ratio > 0.8:
        report_issue("WARNING", "dataset", 0, f"Low English examples: {1-es_ratio:.1%} (recommended: >20%)")


def main():
    print("🔍 ideas-brillantes Dataset Validation")
    print("=" * 50)

    all_stats = []
    total_valid = 0
    total_examples = 0

    jsonl_files = sorted(DATASET_DIR.glob("*.jsonl"))
    if not jsonl_files:
        print(f"❌ No .jsonl files found in {DATASET_DIR}")
        return 1

    for filepath in jsonl_files:
        if filepath.name in ("train.jsonl", "val.jsonl"):
            continue

        stats = validate_file(filepath)
        all_stats.append(stats)
        total_valid += stats["valid"]
        total_examples += stats["total"]

        status = "✅" if stats["valid"] == stats["total"] else "⚠️"
        print(f"\n{status} {stats['name']}")
        print(f"   Total: {stats['total']} | Valid: {stats['valid']} | "
              f"Too long: {stats['too_long']} | Tool calls: {stats['has_tool_calls']}")
        print(f"   Languages: ES={stats['languages']['es']} EN={stats['languages']['en']}")

    # Balance checks
    check_balance(all_stats)

    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary")
    print(f"  Total files:    {len(all_stats)}")
    print(f"  Total examples: {total_examples}")
    print(f"  Valid examples: {total_valid}")
    print(f"  Error rate:     {(total_examples - total_valid) / max(total_examples, 1):.1%}")

    if ISSUES:
        print(f"\n❌ ERRORS ({len(ISSUES)}):")
        for issue in ISSUES[:20]:  # Show first 20
            print(issue)
        if len(ISSUES) > 20:
            print(f"  ... and {len(ISSUES) - 20} more errors")
    else:
        print("\n✅ No errors found!")

    if WARNINGS:
        print(f"\n⚠️  WARNINGS ({len(WARNINGS)}):")
        for w in WARNINGS[:10]:
            print(w)
        if len(WARNINGS) > 10:
            print(f"  ... and {len(WARNINGS) - 10} more warnings")
    else:
        print("✅ No warnings!")

    if not ISSUES:
        print("\n🎉 Dataset validation passed! Ready to run prepare_dataset.py")
        return 0
    else:
        print(f"\n💥 Validation failed with {len(ISSUES)} errors. Fix them before training.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
