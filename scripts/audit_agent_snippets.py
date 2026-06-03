#!/usr/bin/env python3
"""Audit ```tsx fences in agent/**/*.md against eval Layers 1-3."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval.combined import validate_source  # noqa: E402

FENCE_RE = re.compile(r"```tsx\s*\r?\n(.*?)```", re.DOTALL)


def _wrap_snippet(code: str, label: str) -> str:
    """Wrap bare JSX in a named export so structural checks have context."""
    stripped = code.strip()
    if re.search(r"\bexport\s+(?:default\s+)?function\b", stripped):
        return stripped
    if re.search(r"\bexport\s+function\b", stripped):
        return stripped
    safe = re.sub(r"[^A-Za-z0-9]", "", label) or "Snippet"
    return f"export function AgentSnippet{safe}() {{\n  return (\n{stripped}\n  );\n}}\n"


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Audit tsx fences in agent/**/*.md")
    parser.add_argument(
        "--tailwind-only",
        action="store_true",
        help="Only report Layer 1 (Tailwind) violations — reduces noise from partial snippets",
    )
    parser.add_argument(
        "--subdir",
        default="",
        help="Limit to agent subfolder (e.g. SKILLS or PATTERNS)",
    )
    args = parser.parse_args()

    agent_dir = ROOT / "agent"
    if args.subdir:
        agent_dir = agent_dir / args.subdir
    md_files = sorted(agent_dir.rglob("*.md"))
    total_blocks = 0
    failing_blocks = 0
    exit_code = 0

    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        rel = md_path.relative_to(ROOT)
        for i, block in enumerate(FENCE_RE.findall(text), 1):
            total_blocks += 1
            source = _wrap_snippet(block, f"{rel.stem}{i}")
            report = validate_source(source)
            tailwind_only = args.tailwind_only
            failed = report.tailwind.violation_count > 0 if tailwind_only else not report.passed
            if not failed:
                continue
            failing_blocks += 1
            exit_code = 1
            violation_count = (
                report.tailwind.violation_count
                if tailwind_only
                else report.total_violations
            )
            print(f"\n{rel} — block {i} ({violation_count} violations)")
            layers: list[tuple[str, object]] = (
                [("tailwind", report.tailwind)]
                if tailwind_only
                else [
                    ("tailwind", report.tailwind),
                    ("structural", report.structural),
                    ("render", report.render),
                ]
            )
            for name, layer in layers:
                violations = getattr(layer, "violations", [])
                if not violations:
                    continue
                for v in violations[:8]:
                    loc = f" (line {v.line})" if getattr(v, "line", None) else ""
                    cat = getattr(v, "category", "?")
                    msg = getattr(v, "message", str(v))
                    print(f"  [{name}] {cat}: {msg}{loc}")
                extra = len(violations) - 8
                if extra > 0:
                    print(f"  ... +{extra} more in {name}")

    print(
        f"\n---\nAudited {total_blocks} tsx blocks in {len(md_files)} files. "
        f"Failures: {failing_blocks}/{total_blocks}."
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
