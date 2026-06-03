"""Reference samples must pass all eval layers (agent polish gate)."""

from __future__ import annotations

from pathlib import Path

import pytest

from eval.combined import validate_source

SAMPLES_DIR = Path(__file__).parent.parent / "samples"


@pytest.mark.parametrize(
    "path",
    sorted(SAMPLES_DIR.glob("*.tsx")),
    ids=lambda p: p.name,
)
def test_sample_passes_eval(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    report = validate_source(source, source_label=str(path))
    assert report.passed, (
        f"{path.name}: {report.total_violations} violations "
        f"(tailwind={report.tailwind.violation_count}, "
        f"structural={report.structural.violation_count}, "
        f"render={report.render.violation_count})"
    )
