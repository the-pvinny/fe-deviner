"""Tests for structural and render validators and combined eval."""

from __future__ import annotations

from pathlib import Path

import pytest

from eval.combined import validate_source as validate_all
from eval.render_validator import validate_source as validate_render
from eval.structural_validator import validate_source as validate_structural
from eval.structural_validator.validator import StructuralCategory
from eval.render_validator.validator import RenderCategory

FIXTURES = Path(__file__).parent / "fixtures"


class TestStructuralValidator:
    def test_valid_form_passes(self):
        source = (FIXTURES / "valid-form.tsx").read_text(encoding="utf-8")
        result = validate_structural(source)
        assert result.passed
        assert result.violation_count == 0

    def test_invalid_structural_fixture(self):
        source = (FIXTURES / "invalid-structural.tsx").read_text(encoding="utf-8")
        result = validate_structural(source)
        categories = {v.category for v in result.violations}
        assert StructuralCategory.INLINE_STYLE.value in categories
        assert StructuralCategory.NON_SEMANTIC_INTERACTIVE.value in categories
        assert StructuralCategory.MISSING_ALT.value in categories
        assert StructuralCategory.MISSING_LABEL.value in categories
        assert StructuralCategory.DEFAULT_EXPORT.value in categories
        assert not result.passed

    def test_detects_missing_focus_state(self):
        source = '<button className="p-2">Click</button>'
        result = validate_structural(source)
        assert any(v.category == StructuralCategory.MISSING_FOCUS_STATE.value for v in result.violations)

    def test_jsx_expression_children_not_icon_only(self):
        source = (
            '<button type="button" className="focus-visible:ring-2 focus-visible:ring-ring">'
            "{primaryLabel}</button>"
        )
        result = validate_structural(source)
        assert not any(
            v.category == StructuralCategory.MISSING_ARIA_LABEL.value for v in result.violations
        )


class TestRenderValidator:
    def test_valid_form_passes(self):
        source = (FIXTURES / "valid-form.tsx").read_text(encoding="utf-8")
        result = validate_render(source)
        assert result.passed

    def test_invalid_render_fixture(self):
        source = (FIXTURES / "invalid-render.tsx").read_text(encoding="utf-8")
        result = validate_render(source)
        categories = {v.category for v in result.violations}
        assert RenderCategory.UNCLOSED_TAG.value in categories or RenderCategory.MISMATCHED_TAG.value in categories
        assert RenderCategory.UNCLOSED_STRING.value in categories or RenderCategory.INVALID_IMPORT.value in categories
        assert not result.passed

    def test_detects_unbalanced_braces(self):
        source = "export function X() { return <div></div>"
        result = validate_render(source)
        assert any(v.category == RenderCategory.UNBALANCED_BRACES.value for v in result.violations)


class TestCombinedEval:
    def test_valid_form_all_layers_pass(self):
        source = (FIXTURES / "valid-form.tsx").read_text(encoding="utf-8")
        report = validate_all(source)
        assert report.passed
        assert report.tailwind.violation_count == 0
        assert report.structural.passed
        assert report.render.passed

    def test_invalid_card_fails_tailwind(self):
        source = (FIXTURES / "invalid-card.tsx").read_text(encoding="utf-8")
        report = validate_all(source)
        assert not report.passed
        assert report.tailwind.violation_count > 0

    def test_overall_violation_rate(self):
        source = (FIXTURES / "invalid-structural.tsx").read_text(encoding="utf-8")
        report = validate_all(source)
        assert report.total_violations > 0
        assert report.overall_violation_rate > 0
