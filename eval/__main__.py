"""CLI for the fe-deviner eval stack (Layers 1-3)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from eval.combined import (
    format_layer_result,
    format_text_report,
    layer_result_to_dict,
    report_to_dict,
    validate_source,
)
from eval.render_validator import validate_source as validate_render
from eval.structural_validator import validate_source as validate_structural
from eval.tailwind_validator import format_text_report as format_tailwind_report
from eval.tailwind_validator import validate_source as validate_tailwind
from eval.tailwind_validator.report import result_to_dict as tailwind_to_dict

LAYER_CHOICES = ("all", "tailwind", "structural", "render")


def _read_jsonl(path: Path, field: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"Warning: skipping malformed JSONL line {i}: {exc}", file=sys.stderr)
                continue
            output = record.get(field, "")
            entry_id = record.get("id", f"line-{i}")
            if isinstance(output, str) and output:
                entries.append((entry_id, output))
    return entries


def _run_layer(layer: str, source: str):
    if layer == "tailwind":
        return validate_tailwind(source)
    if layer == "structural":
        return validate_structural(source)
    if layer == "render":
        return validate_render(source)
    return validate_source(source)


def _result_violations(result) -> int:
    if hasattr(result, "violation_count"):
        return result.violation_count
    return 0


def _format_single(layer: str, result, *, verbose: bool) -> str:
    if layer == "tailwind":
        return format_tailwind_report(result, verbose=verbose)
    if layer == "all":
        return format_text_report(result, verbose=verbose)
    lines = [f"Layer — {layer}", "=" * 24]
    lines.extend(format_layer_result(result, verbose=verbose))
    return "\n".join(lines)


def _single_to_dict(layer: str, result) -> dict:
    if layer == "tailwind":
        return tailwind_to_dict(result)
    if layer == "all":
        return report_to_dict(result)
    return layer_result_to_dict(result)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate generated React/HTML output (Tailwind, structural, render).",
    )
    parser.add_argument("paths", nargs="*", help="Source files (.tsx, .jsx, .html)")
    parser.add_argument("--stdin", action="store_true", help="Read source from stdin")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show violation details")
    parser.add_argument("--jsonl", type=Path, help="Validate output field from JSONL dataset")
    parser.add_argument("--field", default="output", help="JSONL field (default: output)")
    parser.add_argument(
        "--layer",
        choices=LAYER_CHOICES,
        default="all",
        help="Which layer to run (default: all)",
    )
    parser.add_argument(
        "--fail-on-violations",
        action="store_true",
        help="Exit 1 if any violations found",
    )

    args = parser.parse_args(argv)
    layer = args.layer

    if args.jsonl:
        if not args.jsonl.exists():
            print(f"Error: JSONL file not found: {args.jsonl}", file=sys.stderr)
            return 2
        entries = _read_jsonl(args.jsonl, args.field)
        batch_entries = []
        total_violations = 0
        for entry_id, output in entries:
            result = _run_layer(layer, output)
            total_violations += _result_violations(result)
            payload = _single_to_dict(layer, result)
            payload["id"] = entry_id
            batch_entries.append(payload)

        if args.json:
            print(json.dumps({"entries": batch_entries}, indent=2))
        else:
            print(f"Eval Batch Report — layer: {layer}")
            print("=" * 36)
            for entry in batch_entries:
                vid = entry.get("id", "?")
                if layer == "all":
                    vcount = entry.get("total_violations", 0)
                else:
                    vcount = entry.get("violation_count", 0)
                print(f"  {vid}: {vcount} violations")
            print(f"\nTotal violations: {total_violations}")

        return 1 if args.fail_on_violations and total_violations > 0 else 0

    sources: list[tuple[str, str]] = []
    if args.stdin:
        sources.append(("stdin", sys.stdin.read()))
    for path_str in args.paths:
        path = Path(path_str)
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            return 2
        sources.append((str(path), path.read_text(encoding="utf-8")))

    if not sources:
        parser.print_help()
        return 2

    total_violations = 0
    for label, source in sources:
        result = _run_layer(layer, source)
        total_violations += _result_violations(result)

        if len(sources) > 1 and not args.json:
            print(f"\n--- {label} ---")

        if args.json:
            payload = _single_to_dict(layer, result)
            if len(sources) > 1:
                payload["source"] = label
            print(json.dumps(payload, indent=2))
        else:
            print(_format_single(layer, result, verbose=args.verbose))

    return 1 if args.fail_on_violations and total_violations > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
