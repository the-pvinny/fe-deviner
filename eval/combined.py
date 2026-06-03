"""Unified eval runner for all validation layers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from eval.render_validator import validate_source as validate_render
from eval.shared.parser import BaseResult
from eval.structural_validator import validate_source as validate_structural
from eval.tailwind_validator import validate_source as validate_tailwind
from eval.tailwind_validator.validator import ValidationResult as TailwindResult


@dataclass
class EvalReport:
    """Combined report from Layers 1-3."""

    tailwind: TailwindResult
    structural: BaseResult
    render: BaseResult
    source_label: str | None = None

    @property
    def passed(self) -> bool:
        return (
            self.tailwind.violation_count == 0
            and self.structural.passed
            and self.render.passed
        )

    @property
    def total_violations(self) -> int:
        return (
            self.tailwind.violation_count
            + self.structural.violation_count
            + self.render.violation_count
        )

    @property
    def total_checks(self) -> int:
        return (
            self.tailwind.total_classes
            + self.structural.total_checks
            + self.render.total_checks
        )

    @property
    def overall_violation_rate(self) -> float:
        if self.total_checks == 0:
            return 0.0
        return self.total_violations / self.total_checks


def validate_source(source: str, *, source_label: str | None = None) -> EvalReport:
    """Run all three eval layers on source code."""
    return EvalReport(
        tailwind=validate_tailwind(source),
        structural=validate_structural(source),
        render=validate_render(source),
        source_label=source_label,
    )


def layer_result_to_dict(result: BaseResult) -> dict[str, Any]:
    return {
        "layer": result.layer,
        "total_checks": result.total_checks,
        "violation_count": result.violation_count,
        "violation_rate": round(result.violation_rate, 4),
        "pass_rate": round(result.pass_rate, 4),
        "passed": result.passed,
        "violations_by_category": result.violations_by_category(),
        "metadata": result.metadata,
        "violations": [
            {
                "category": v.category,
                "message": v.message,
                "line": v.line,
                "column": v.column,
                "snippet": v.snippet,
            }
            for v in result.violations
        ],
    }


def report_to_dict(report: EvalReport) -> dict[str, Any]:
    from eval.tailwind_validator.report import result_to_dict as tailwind_to_dict

    payload: dict[str, Any] = {
        "passed": report.passed,
        "total_violations": report.total_violations,
        "total_checks": report.total_checks,
        "overall_violation_rate": round(report.overall_violation_rate, 4),
        "layers": {
            "tailwind": tailwind_to_dict(report.tailwind),
            "structural": layer_result_to_dict(report.structural),
            "render": layer_result_to_dict(report.render),
        },
    }
    if report.source_label:
        payload["source"] = report.source_label
    return payload


def format_text_report(report: EvalReport, *, verbose: bool = False) -> str:
    from eval.tailwind_validator.report import format_text_report as format_tailwind

    lines: list[str] = []
    lines.append("fe-deviner Eval Report (Layers 1-3)")
    lines.append("=" * 36)
    status = "PASS" if report.passed else "FAIL"
    lines.append(f"Overall:          {status}")
    lines.append(f"Total violations: {report.total_violations}")
    lines.append(f"Violation rate:   {report.overall_violation_rate:.2%}")
    lines.append("")

    lines.append("Layer 1 - Tailwind Classes")
    lines.append("-" * 28)
    lines.append(format_tailwind(report.tailwind, verbose=verbose))
    lines.append("")

    lines.append("Layer 2 - Structural (METHOD.md)")
    lines.append("-" * 28)
    lines.extend(format_layer_result(report.structural, verbose=verbose))
    lines.append("")

    lines.append("Layer 3 - Render Validity")
    lines.append("-" * 28)
    lines.extend(format_layer_result(report.render, verbose=verbose))

    return "\n".join(lines)


def format_layer_result(result: BaseResult, *, verbose: bool) -> list[str]:
    lines = [
        f"Checks:           {result.total_checks}",
        f"Violations:       {result.violation_count}",
        f"Violation rate:   {result.violation_rate:.2%}",
        f"Status:           {'PASS' if result.passed else 'FAIL'}",
    ]
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
            lines.append(f"  [{v.category}]{loc}")
            lines.append(f"    {v.message}")
            if v.snippet:
                lines.append(f"    > {v.snippet[:80]}")

    return lines
