"""Shared eval types and utilities."""

from .parser import (
    BaseResult,
    BaseViolation,
    Element,
    attr_value,
    class_names,
    extract_elements,
    extract_inner_text,
    find_matching_close,
    has_attr,
    has_focus_visible,
    is_pascal_case,
    line_col,
    snippet_at,
    strip_strings_and_comments,
)

__all__ = [
    "BaseResult",
    "BaseViolation",
    "Element",
    "attr_value",
    "class_names",
    "extract_elements",
    "extract_inner_text",
    "find_matching_close",
    "has_attr",
    "has_focus_visible",
    "is_pascal_case",
    "line_col",
    "snippet_at",
    "strip_strings_and_comments",
]
