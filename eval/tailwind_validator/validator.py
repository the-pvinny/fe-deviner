"""Validate Tailwind classes against CONFIG.md token rules."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum

from .allowlist import (
    BORDER_RADIUS,
    BORDER_WIDTH_VALUES,
    COLOR_PREFIXES,
    DURATIONS,
    EASING,
    FONT_SIZES,
    FONT_WEIGHTS,
    FORBIDDEN_COLOR_NAMES,
    LEADING,
    MAX_WIDTH_VALUES,
    OPACITY_SCALE,
    PRIMITIVE_PALETTES,
    PRIMITIVE_SCALE_STEPS,
    SEMANTIC_COLORS,
    SHADOWS,
    SIZE_SPECIAL_VALUES,
    SPACING_PREFIXES,
    SPACING_SCALE,
    STATIC_UTILITIES,
    TRACKING,
    VARIANT_PREFIXES,
    Z_INDEX,
)
from .extractor import ClassOccurrence, extract_classes

FRACTION_PATTERN = re.compile(r"^\d+/\d+$")
ARBITRARY_PATTERN = re.compile(r"\[.+\]")
IMPORTANT_PREFIX = re.compile(r"^!+")

# aria-[...] and data-[...] variant prefixes
DYNAMIC_VARIANT = re.compile(r"^(aria|data)-.+$")


class ViolationCategory(str, Enum):
    ARBITRARY_VALUE = "arbitrary_value"
    IMPORTANT_MODIFIER = "important_modifier"
    PRIMITIVE_COLOR = "primitive_color"
    FORBIDDEN_COLOR = "forbidden_color"
    INVALID_COLOR = "invalid_color"
    INVALID_SPACING = "invalid_spacing"
    INVALID_TYPOGRAPHY = "invalid_typography"
    INVALID_RADIUS = "invalid_radius"
    INVALID_SHADOW = "invalid_shadow"
    INVALID_TRANSITION = "invalid_transition"
    INVALID_Z_INDEX = "invalid_z_index"
    INVALID_OPACITY = "invalid_opacity"
    UNKNOWN_UTILITY = "unknown_utility"


@dataclass
class Violation:
    cls: str
    category: ViolationCategory
    message: str
    line: int | None = None
    column: int | None = None
    source: str | None = None


@dataclass
class ValidationResult:
    total_classes: int = 0
    valid_classes: int = 0
    violations: list[Violation] = field(default_factory=list)

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    @property
    def violation_rate(self) -> float:
        if self.total_classes == 0:
            return 0.0
        return self.violation_count / self.total_classes

    @property
    def pass_rate(self) -> float:
        return 1.0 - self.violation_rate

    def violations_by_category(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for v in self.violations:
            key = v.category.value
            counts[key] = counts.get(key, 0) + 1
        return counts


def _strip_variants(cls: str) -> str:
    """Remove responsive/state variant prefixes from a class token."""
    parts = cls.split(":")
    while len(parts) > 1:
        prefix = parts[0]
        if prefix in VARIANT_PREFIXES or DYNAMIC_VARIANT.match(prefix):
            parts = parts[1:]
            continue
        break
    return parts[-1] if parts else cls


def _strip_important(cls: str) -> tuple[str, bool]:
    if IMPORTANT_PREFIX.match(cls):
        return IMPORTANT_PREFIX.sub("", cls), True
    return cls, False


def _parse_color_value(value: str) -> tuple[str, str | None]:
    """Split color token and optional opacity modifier (primary/80)."""
    if "/" in value:
        color, opacity = value.split("/", 1)
        return color, opacity
    return value, None


def _is_primitive_color(color: str) -> bool:
    if "-" not in color:
        return False
    palette, step = color.rsplit("-", 1)
    return palette in PRIMITIVE_PALETTES and step in PRIMITIVE_SCALE_STEPS


def _is_forbidden_color(color: str) -> bool:
    if color in FORBIDDEN_COLOR_NAMES:
        return True
    if "-" in color:
        palette = color.split("-", 1)[0]
        return palette in FORBIDDEN_COLOR_NAMES
    return False


def _validate_color_value(value: str) -> ViolationCategory | None:
    color, opacity = _parse_color_value(value)

    if _is_primitive_color(color):
        return ViolationCategory.PRIMITIVE_COLOR
    if _is_forbidden_color(color):
        return ViolationCategory.FORBIDDEN_COLOR
    if color not in SEMANTIC_COLORS:
        return ViolationCategory.INVALID_COLOR
    if opacity is not None and opacity not in OPACITY_SCALE:
        return ViolationCategory.INVALID_COLOR
    return None


def _validate_spacing_value(prefix: str, value: str) -> bool:
    if value in SPACING_SCALE:
        return True
    # auto is valid for margin and positioning utilities
    if value == "auto" and prefix in (
        "m", "mx", "my", "mt", "mr", "mb", "ml", "ms", "me",
        "inset", "inset-x", "inset-y", "top", "right", "bottom", "left", "start", "end",
    ):
        return True
    if prefix in ("w", "h", "min-w", "min-h", "max-h", "size", "basis"):
        if value in SIZE_SPECIAL_VALUES:
            return True
        if FRACTION_PATTERN.match(value):
            return True
    if prefix == "max-w" and value in MAX_WIDTH_VALUES:
        return True
    if prefix in ("max-w", "w", "basis") and FRACTION_PATTERN.match(value):
        return True
    if value.startswith("-") and value[1:] in SPACING_SCALE:
        return True
    return False


def _match_prefix(base: str, prefixes: set[str]) -> tuple[str, str] | None:
    """Return (prefix, value) if base matches a known prefix."""
    for prefix in sorted(prefixes, key=len, reverse=True):
        if base == prefix:
            return prefix, ""
        if base.startswith(prefix + "-"):
            return prefix, base[len(prefix) + 1 :]
    return None


def _validate_base_class(base: str) -> list[tuple[ViolationCategory, str]]:
    """Validate a single class after variants and important are stripped."""
    errors: list[tuple[ViolationCategory, str]] = []

    if ARBITRARY_PATTERN.search(base):
        errors.append(
            (ViolationCategory.ARBITRARY_VALUE, "Arbitrary values are forbidden")
        )
        return errors

    if base in STATIC_UTILITIES:
        return errors

    # Negative translate/scale/inset utilities
    if base.startswith("-") and base[1:] in STATIC_UTILITIES:
        return errors

    # Standalone typography utilities
    if base.startswith("text-") and base[5:] in FONT_SIZES:
        return errors
    if base.startswith("font-") and base[5:] in FONT_WEIGHTS:
        return errors
    if base.startswith("tracking-") and base[9:] in TRACKING:
        return errors
    if base.startswith("leading-") and base[8:] in LEADING:
        return errors

    # Border radius
    if base.startswith("rounded"):
        suffix = base[7:].lstrip("-") or "DEFAULT"
        if suffix in BORDER_RADIUS or base == "rounded":
            return errors
        errors.append((ViolationCategory.INVALID_RADIUS, f"Unknown radius token: {suffix}"))
        return errors

    # Shadow
    if base.startswith("shadow-"):
        suffix = base[7:]
        if suffix in SHADOWS:
            return errors
        errors.append((ViolationCategory.INVALID_SHADOW, f"Unknown shadow token: {suffix}"))
        return errors

    # Duration / easing
    if base.startswith("duration-"):
        suffix = base[9:]
        if suffix in DURATIONS:
            return errors
        errors.append((ViolationCategory.INVALID_TRANSITION, f"Unknown duration: {suffix}"))
        return errors
    if base.startswith("ease-"):
        suffix = base[5:]
        if suffix in EASING:
            return errors
        errors.append((ViolationCategory.INVALID_TRANSITION, f"Unknown easing: {suffix}"))
        return errors

    # Z-index (includes negative stacking, e.g. -z-10 for background layers)
    if base.startswith("-z-"):
        suffix = base[3:]
        if suffix in Z_INDEX:
            return errors
        errors.append((ViolationCategory.INVALID_Z_INDEX, f"Unknown z-index: -{suffix}"))
        return errors
    if base.startswith("z-"):
        suffix = base[2:]
        if suffix in Z_INDEX:
            return errors
        errors.append((ViolationCategory.INVALID_Z_INDEX, f"Unknown z-index: {suffix}"))
        return errors

    # Opacity standalone
    if base.startswith("opacity-"):
        suffix = base[8:]
        if suffix in OPACITY_SCALE:
            return errors
        errors.append((ViolationCategory.INVALID_OPACITY, f"Unknown opacity: {suffix}"))
        return errors

    # Grid/flex enumerated
    for prefix in ("grid-cols", "grid-rows", "col-span", "row-span", "order"):
        if base.startswith(prefix + "-"):
            suffix = base[len(prefix) + 1 :]
            if suffix.isdigit() or suffix in ("none", "full", "subgrid"):
                return errors

    # Translate utilities with spacing scale (including negative: -translate-y-0.5)
    for axis in ("x", "y"):
        for sign in ("", "-"):
            prefix = f"{sign}translate-{axis}"
            if base.startswith(prefix + "-"):
                value = base[len(prefix) + 1 :]
                if value in SPACING_SCALE:
                    return errors
                if value in ("full", "1/2", "1/3", "2/3", "1/4", "2/4", "3/4"):
                    return errors

    # Color utilities
    color_match = _match_prefix(base, COLOR_PREFIXES)
    if color_match:
        prefix, value = color_match
        if prefix == "shadow" and value in SHADOWS:
            return errors
        if not value:
            if prefix in ("border", "ring", "outline", "divide", "divide-x", "divide-y"):
                return errors
            errors.append((ViolationCategory.INVALID_COLOR, "Missing color value"))
            return errors
        category = _validate_color_value(value)
        if category:
            if category == ViolationCategory.PRIMITIVE_COLOR:
                errors.append((category, f"Primitive color '{value}' - use semantic tokens"))
            elif category == ViolationCategory.FORBIDDEN_COLOR:
                errors.append((category, f"Forbidden color '{value}' - use semantic tokens"))
            else:
                errors.append((category, f"Unapproved color '{value}'"))
        return errors

    # Spacing utilities
    spacing_match = _match_prefix(base, set(SPACING_PREFIXES.keys()))
    if spacing_match:
        prefix, value = spacing_match
        if _validate_spacing_value(prefix, value):
            return errors
        errors.append((ViolationCategory.INVALID_SPACING, f"Invalid spacing value '{value}' for {prefix}"))
        return errors

    # Border width with semantic color handled above; bare border-N
    if base.startswith("border-") and base[7:] in BORDER_WIDTH_VALUES:
        return errors

    # line-clamp-N
    if base.startswith("line-clamp-"):
        suffix = base[11:]
        if suffix.isdigit() or suffix == "none":
            return errors

    errors.append((ViolationCategory.UNKNOWN_UTILITY, f"Unrecognized utility class"))
    return errors


def validate_class(cls: str) -> list[Violation]:
    """Validate a single Tailwind class token."""
    stripped, has_important = _strip_important(cls)
    base = _strip_variants(stripped)

    violations: list[Violation] = []
    if has_important:
        violations.append(
            Violation(
                cls=cls,
                category=ViolationCategory.IMPORTANT_MODIFIER,
                message="!important modifier is forbidden",
            )
        )

    for category, message in _validate_base_class(base):
        violations.append(Violation(cls=cls, category=category, message=message))

    return violations


def validate_source(source: str) -> ValidationResult:
    """Validate all Tailwind classes found in source code."""
    result = ValidationResult()

    for cls, occurrence in extract_classes(source):
        result.total_classes += 1
        class_violations = validate_class(cls)

        if class_violations:
            for v in class_violations:
                v.line = occurrence.line
                v.column = occurrence.column
                v.source = occurrence.source
                result.violations.append(v)
        else:
            result.valid_classes += 1

    return result


def validate_classes(classes: list[str]) -> ValidationResult:
    """Validate a list of class tokens (no source locations)."""
    result = ValidationResult()
    for cls in classes:
        result.total_classes += 1
        class_violations = validate_class(cls)
        if class_violations:
            result.violations.extend(class_violations)
        else:
            result.valid_classes += 1
    return result
