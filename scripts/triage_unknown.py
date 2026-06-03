"""Triage unknown/invalid validator categories across all agent doc snippets."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.tailwind_validator import extract_classes, validate_class
from eval.tailwind_validator.validator import ViolationCategory

AGENT_DIR = Path(__file__).parent.parent / "agent"
BLOCK_RE = re.compile(r"```tsx\n(.*?)```", re.DOTALL)

buckets: dict[str, dict[str, int]] = {
    "unknown_utility": {},
    "primitive_color": {},
    "forbidden_color": {},
    "invalid_spacing": {},
    "invalid_radius": {},
    "invalid_shadow": {},
    "invalid_typography": {},
    "invalid_transition": {},
    "invalid_z_index": {},
    "arbitrary_value": {},
    "important_modifier": {},
}

for md in sorted(AGENT_DIR.rglob("*.md")):
    source = md.read_text(encoding="utf-8")
    for block in BLOCK_RE.findall(source):
        for cls, _ in extract_classes(block):
            for v in validate_class(cls):
                key = v.category.value if hasattr(v.category, "value") else str(v.category)
                if key in buckets:
                    buckets[key][cls] = buckets[key].get(cls, 0) + 1

for label, items in buckets.items():
    if not items:
        continue
    print(f"\n=== {label.upper().replace('_', ' ')} ({len(items)} unique) ===")
    for cls, n in sorted(items.items(), key=lambda x: -x[1]):
        print(f"  {n:3d}  {cls}")
