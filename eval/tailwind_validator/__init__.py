"""Tailwind class validator — Layer 1 eval for fe-deviner."""

from .extractor import ClassOccurrence, extract_class_strings, extract_classes
from .report import format_json_report, format_text_report, result_to_dict
from .validator import ValidationResult, Violation, ViolationCategory, validate_class, validate_classes, validate_source

__all__ = [
    "ClassOccurrence",
    "ValidationResult",
    "Violation",
    "ViolationCategory",
    "extract_class_strings",
    "extract_classes",
    "format_json_report",
    "format_text_report",
    "result_to_dict",
    "validate_class",
    "validate_classes",
    "validate_source",
]
