"""Tests for Tailwind class validator."""

from __future__ import annotations

from pathlib import Path

import pytest

from eval.tailwind_validator import (
    extract_classes,
    validate_class,
    validate_source,
)
from eval.tailwind_validator.validator import ViolationCategory

FIXTURES = Path(__file__).parent / "fixtures"


class TestExtractor:
    def test_extracts_classname_strings(self):
        source = '<div className="flex gap-4 p-6" />'
        tokens = extract_classes(source)
        assert [t[0] for t in tokens] == ["flex", "gap-4", "p-6"]

    def test_extracts_cn_arguments(self):
        source = 'className={cn("rounded-lg border", "bg-card", className)}'
        tokens = extract_classes(source)
        assert "rounded-lg" in [t[0] for t in tokens]
        assert "bg-card" in [t[0] for t in tokens]

    def test_extracts_html_class_attribute(self):
        source = '<section class="grid grid-cols-2 gap-4"></section>'
        tokens = extract_classes(source)
        assert [t[0] for t in tokens] == ["grid", "grid-cols-2", "gap-4"]


class TestValidClasses:
    @pytest.mark.parametrize(
        "cls",
        [
            "bg-primary",
            "text-muted-foreground",
            "border-border",
            "ring-ring",
            "bg-destructive/10",
            "hover:bg-accent",
            "focus-visible:ring-2",
            "md:grid-cols-2",
            "motion-safe:transition-all",
            "size-4",
            "min-h-11",
            "max-w-prose",
            "rounded-lg",
            "shadow-sm",
            "duration-200",
            "ease-out",
            "z-50",
            "-z-10",
            "accent-primary",
            "-translate-y-0.5",
            "group-hover:shadow-md",
        ],
    )
    def test_allowed_classes_pass(self, cls: str):
        assert validate_class(cls) == []

    def test_valid_fixture_has_no_violations(self):
        source = (FIXTURES / "valid-card.tsx").read_text(encoding="utf-8")
        result = validate_source(source)
        assert result.violation_count == 0
        assert result.total_classes > 0


class TestViolations:
    @pytest.mark.parametrize(
        "cls,category",
        [
            ("w-[247px]", ViolationCategory.ARBITRARY_VALUE),
            ("text-[13px]", ViolationCategory.ARBITRARY_VALUE),
            ("bg-neutral-100", ViolationCategory.PRIMITIVE_COLOR),
            ("text-blue-500", ViolationCategory.PRIMITIVE_COLOR),
            ("text-black", ViolationCategory.FORBIDDEN_COLOR),
            ("bg-white", ViolationCategory.FORBIDDEN_COLOR),
            ("text-gray-500", ViolationCategory.FORBIDDEN_COLOR),
            ("!p-4", ViolationCategory.IMPORTANT_MODIFIER),
            ("bg-[#ff5733]", ViolationCategory.ARBITRARY_VALUE),
        ],
    )
    def test_detects_violations(self, cls: str, category: ViolationCategory):
        violations = validate_class(cls)
        assert any(v.category == category for v in violations)

    def test_invalid_fixture_catches_expected_violations(self):
        source = (FIXTURES / "invalid-card.tsx").read_text(encoding="utf-8")
        result = validate_source(source)
        categories = {v.category for v in result.violations}
        assert ViolationCategory.ARBITRARY_VALUE in categories
        assert ViolationCategory.PRIMITIVE_COLOR in categories
        assert ViolationCategory.FORBIDDEN_COLOR in categories
        assert ViolationCategory.IMPORTANT_MODIFIER in categories
        assert result.violation_rate > 0

    def test_violation_rate_calculation(self):
        source = '<div className="flex bg-neutral-50 text-black" />'
        result = validate_source(source)
        assert result.total_classes == 3
        assert result.violation_count >= 2
        assert 0 < result.violation_rate < 1

    def test_violations_by_category(self):
        source = '<div className="w-[100px] bg-red-500 text-white" />'
        result = validate_source(source)
        by_cat = result.violations_by_category()
        assert by_cat.get("arbitrary_value", 0) >= 1
        assert by_cat.get("forbidden_color", 0) >= 1


class TestValidateClasses:
    def test_batch_class_validation(self):
        from eval.tailwind_validator.validator import validate_classes

        valid = ["flex", "gap-4", "p-6", "bg-primary", "text-muted-foreground"]
        result = validate_classes(valid)
        assert result.total_classes == 5
        assert result.violation_count == 0
        assert result.pass_rate == 1.0

    def test_batch_class_validation_with_violations(self):
        from eval.tailwind_validator.validator import validate_classes

        classes = ["flex", "bg-neutral-100", "text-black", "p-4"]
        result = validate_classes(classes)
        assert result.total_classes == 4
        assert result.violation_count >= 2
        categories = {v.category.value for v in result.violations}
        assert "primitive_color" in categories
        assert "forbidden_color" in categories

    def test_ring_offset_spacing_is_valid(self):
        """ring-offset-{N} spacing variants must not be flagged as INVALID_COLOR."""
        from eval.tailwind_validator.validator import validate_classes

        result = validate_classes(
            ["ring-offset-0", "ring-offset-1", "ring-offset-2", "ring-offset-4", "ring-offset-8"]
        )
        assert result.violation_count == 0, (
            f"Unexpected violations for ring-offset-* classes: {result.violations}"
        )


class TestJsonOutput:
    def test_tailwind_result_dict_has_layer_key(self):
        from eval.tailwind_validator.report import result_to_dict
        from eval.tailwind_validator.validator import ValidationResult

        d = result_to_dict(ValidationResult())
        assert d["layer"] == "tailwind"

    def test_combined_report_all_layers_have_layer_key(self):
        from eval.combined import report_to_dict, validate_source as validate_all

        source = (FIXTURES / "valid-card.tsx").read_text(encoding="utf-8")
        d = report_to_dict(validate_all(source))
        assert d["layers"]["tailwind"]["layer"] == "tailwind"
        assert d["layers"]["structural"]["layer"] == "structural"
        assert d["layers"]["render"]["layer"] == "render"
