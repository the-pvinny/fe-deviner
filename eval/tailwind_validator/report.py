"""Format validation results for CLI and training eval pipelines."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from .validator import ValidationResult, Violation


def result_to_dict(result: ValidationResult) -> dict[str, Any]:
    return {
        "layer": "tailwind",
        "total_classes": result.total_classes,
        "valid_classes": result.valid_classes,
        "violation_count": result.violation_count,
        "violation_rate": round(result.violation_rate, 4),
        "pass_rate": round(result.pass_rate, 4),
        "violations_by_category": result.violations_by_category(),
        "violations": [
            {
                "class": v.cls,
                "category": v.category.value,
                "message": v.message,
                "line": v.line,
                "column": v.column,
                "source": v.source,
            }
            for v in result.violations
        ],
    }


def format_text_report(result: ValidationResult, *, verbose: bool = False) -> str:
    lines: list[str] = []
    lines.append("Tailwind Class Validator Report")
    lines.append("=" * 32)
    lines.append(f"Total classes:    {result.total_classes}")
    lines.append(f"Valid classes:    {result.valid_classes}")
    lines.append(f"Violations:       {result.violation_count}")
    lines.append(f"Violation rate:   {result.violation_rate:.2%}")
    lines.append(f"Pass rate:        {result.pass_rate:.2%}")

    by_category = result.violations_by_category()
    if by_category:
        lines.append("")
        lines.append("Violations by category:")
        for category, count in sorted(by_category.items(), key=lambda x: -x[1]):
            lines.append(f"  {category}: {count}")

    if verbose and result.violations:
        lines.append("")
        lines.append("Details:")
        for v in result.violations:
            loc = ""
            if v.line is not None:
                loc = f" (line {v.line}"
                if v.column is not None:
                    loc += f", col {v.column}"
                loc += ")"
            lines.append(f"  [{v.category.value}] {v.cls}{loc}")
            lines.append(f"    {v.message}")

    return "\n".join(lines)


def format_json_report(result: ValidationResult) -> str:
    return json.dumps(result_to_dict(result), indent=2)
