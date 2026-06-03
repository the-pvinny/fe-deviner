"""Layer 2 — structural validator against METHOD.md rules."""

from __future__ import annotations

import re
from enum import Enum

from eval.shared.parser import (
    BaseResult,
    BaseViolation,
    class_names,
    extract_elements,
    find_matching_close,
    has_attr,
    has_focus_visible,
    line_col,
    snippet_at,
)

INTERACTIVE_TAGS = frozenset({"button", "a", "input", "select", "textarea"})


class StructuralCategory(str, Enum):
    INLINE_STYLE = "inline_style"
    DEFAULT_EXPORT = "default_export"
    NON_SEMANTIC_INTERACTIVE = "non_semantic_interactive"
    MISSING_ALT = "missing_alt"
    MISSING_LABEL = "missing_label"
    MISSING_ARIA_LABEL = "missing_aria_label"
    MISSING_FOCUS_STATE = "missing_focus_state"
    MISSING_ACCESSIBLE_TEXT = "missing_accessible_text"
    MULTIPLE_H1 = "multiple_h1"
    INVALID_NAMING = "invalid_naming"
    MISSING_DATA_SLOT = "missing_data_slot"


def _violation(
    category: StructuralCategory,
    message: str,
    *,
    line: int | None = None,
    column: int | None = None,
    snippet: str | None = None,
) -> BaseViolation:
    return BaseViolation(
        category=category.value,
        message=message,
        line=line,
        column=column,
        snippet=snippet,
    )


_INLINE_STYLE = re.compile(r"""style\s*=\s*(?:\{\{|["'])""")
_DEFAULT_EXPORT = re.compile(r"\bexport\s+default\b")
_COMPONENT_FN = re.compile(
    r"(?:export\s+)?function\s+(?P<name>[A-Za-z_]\w*)\s*\(",
)
_DIV_SPAN_ONCLICK = re.compile(
    r"<(?:div|span)\b[^>]*\bonClick\b",
    re.IGNORECASE,
)


def _is_icon_only_content(text: str) -> bool:
    # JSX expression children (e.g. {primaryLabel}) imply dynamic visible text.
    if re.search(r"\{[^}]*\}", text):
        return False
    cleaned = re.sub(r"<[^>]+/?>", "", text)
    cleaned = re.sub(r"\s+", "", cleaned)
    return cleaned == ""


def _collect_label_targets(source: str) -> set[str]:
    targets: set[str] = set()
    for match in re.finditer(r"""htmlFor\s*=\s*["'{]([^"'}]+)["'}]""", source):
        targets.add(match.group(1))
    for match in re.finditer(r"""<label[^>]*htmlFor\s*=\s*["'{]([^"'}]+)["'}]""", source):
        targets.add(match.group(1))
    # Wrapping labels: <label ...> ... <input id="x" ...> ... </label>
    for match in re.finditer(
        r"<label\b[^>]*>(?:(?!</label>).)*<input\b[^>]*\bid\s*=\s*[\"'{]([^\"'}]+)[\"'}]",
        source,
        re.DOTALL | re.IGNORECASE,
    ):
        targets.add(match.group(1))
    return targets


def _collect_input_ids(source: str) -> list[tuple[str, int, str]]:
    """Return (id, line, snippet) for inputs that require labels."""
    inputs: list[tuple[str, int, str]] = []
    for match in re.finditer(r"<input\b[^>]*>", source, re.IGNORECASE):
        tag = match.group(0)
        type_match = re.search(r"""type\s*=\s*["'{]([^"'}]+)["'}]""", tag, re.IGNORECASE)
        input_type = (type_match.group(1) if type_match else "text").lower()
        if input_type in {"hidden", "submit", "button", "reset"}:
            continue
        if re.search(r"\baria-label\s*=", tag, re.IGNORECASE):
            continue
        if re.search(r"\baria-labelledby\s*=", tag, re.IGNORECASE):
            continue
        id_match = re.search(r"""\bid\s*=\s*["'{]([^"'}]+)["'}]""", tag, re.IGNORECASE)
        if not id_match:
            line, _ = line_col(source, match.start())
            inputs.append(("", line, snippet_at(source, match.start())))
            continue
        line, _ = line_col(source, match.start())
        inputs.append((id_match.group(1), line, snippet_at(source, match.start())))
    return inputs


def validate_source(source: str) -> BaseResult:
    """Validate structural and accessibility rules from METHOD.md."""
    result = BaseResult(layer="structural")
    violations: list[BaseViolation] = []

    # --- File-level checks ---
    for match in _INLINE_STYLE.finditer(source):
        result.total_checks += 1
        line, col = line_col(source, match.start())
        violations.append(
            _violation(
                StructuralCategory.INLINE_STYLE,
                "Inline styles are forbidden (style={{ }} or style=\"\")",
                line=line,
                column=col,
                snippet=snippet_at(source, match.start()),
            )
        )

    match = _DEFAULT_EXPORT.search(source)
    if match is not None:
        result.total_checks += 1
        line, col = line_col(source, match.start())
        violations.append(
            _violation(
                StructuralCategory.DEFAULT_EXPORT,
                "Use named exports, not export default",
                line=line,
                column=col,
                snippet=snippet_at(source, match.start()),
            )
        )

    for match in _COMPONENT_FN.finditer(source):
        name = match.group("name")
        if name[0].islower() and name not in {"cn"}:
            result.total_checks += 1
            line, col = line_col(source, match.start())
            violations.append(
                _violation(
                    StructuralCategory.INVALID_NAMING,
                    f"Component/function '{name}' should be PascalCase",
                    line=line,
                    column=col,
                    snippet=snippet_at(source, match.start()),
                )
            )

    h1_count = len(re.findall(r"<h1\b", source, re.IGNORECASE))
    if h1_count > 1:
        result.total_checks += h1_count
        violations.append(
            _violation(
                StructuralCategory.MULTIPLE_H1,
                f"Found {h1_count} <h1> elements; only one per page",
            )
        )

    for match in _DIV_SPAN_ONCLICK.finditer(source):
        tag = match.group(0)
        if re.search(r'\brole\s*=\s*["\']button["\']', tag, re.IGNORECASE):
            continue
        result.total_checks += 1
        line, col = line_col(source, match.start())
        violations.append(
            _violation(
                StructuralCategory.NON_SEMANTIC_INTERACTIVE,
                "Use <button> instead of div/span with onClick",
                line=line,
                column=col,
                snippet=snippet_at(source, match.start()),
            )
        )

    label_targets = _collect_label_targets(source)
    for input_id, line, snip in _collect_input_ids(source):
        result.total_checks += 1
        if not input_id or input_id not in label_targets:
            violations.append(
                _violation(
                    StructuralCategory.MISSING_LABEL,
                    "Form input missing associated <label htmlFor>",
                    line=line,
                    snippet=snip,
                )
            )

    # --- Element-level checks ---
    elements = extract_elements(source)
    for i, el in enumerate(elements):
        if el.is_closing:
            continue

        tag_lower = el.tag.lower()

        if tag_lower == "img":
            result.total_checks += 1
            if not has_attr(el.attrs, "alt"):
                violations.append(
                    _violation(
                        StructuralCategory.MISSING_ALT,
                        "<img> must include alt attribute",
                        line=el.line,
                        column=el.column,
                    )
                )

        if tag_lower in INTERACTIVE_TAGS:
            cls = class_names(el.attrs)
            if tag_lower in {"button", "a", "input", "select", "textarea"}:
                result.total_checks += 1
                if not has_focus_visible(cls):
                    violations.append(
                        _violation(
                            StructuralCategory.MISSING_FOCUS_STATE,
                            f"<{tag_lower}> missing focus-visible focus ring in className",
                            line=el.line,
                            column=el.column,
                        )
                    )

        if tag_lower == "button":
            has_aria = has_attr(el.attrs, "aria-label", "aria-labelledby")
            result.total_checks += 1
            if not has_aria and el.inner_start is not None:
                close_idx = find_matching_close(source, i, elements)
                inner = ""
                if close_idx is not None:
                    close_tag = f"</{el.tag}>"
                    close_pos = source.find(close_tag, el.inner_start)
                    if close_pos != -1:
                        inner = source[el.inner_start:close_pos]
                if _is_icon_only_content(inner):
                    violations.append(
                        _violation(
                            StructuralCategory.MISSING_ARIA_LABEL,
                            "Icon-only <button> requires aria-label",
                            line=el.line,
                            column=el.column,
                        )
                    )
                elif not inner.strip() and "{" not in inner:
                    violations.append(
                        _violation(
                            StructuralCategory.MISSING_ACCESSIBLE_TEXT,
                            "<button> must have visible text or aria-label",
                            line=el.line,
                            column=el.column,
                        )
                    )

    if result.total_checks == 0:
        result.total_checks = max(1, len([e for e in elements if not e.is_closing]))

    result.violations = violations
    result.passed = len(violations) == 0
    result.metadata = {
        "elements_found": len(elements),
        "interactive_elements": len(
            [e for e in elements if e.tag.lower() in INTERACTIVE_TAGS and not e.is_closing]
        ),
    }
    return result
