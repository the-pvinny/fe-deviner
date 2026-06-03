"""Layer 3 — render validity check for generated JSX/HTML."""

from __future__ import annotations

import re
from enum import Enum

from eval.shared.parser import (
    BaseResult,
    BaseViolation,
    extract_elements,
    line_col,
    snippet_at,
    strip_strings_and_comments,
)

FRAGMENT_OPEN = re.compile(r"<>")
FRAGMENT_CLOSE = re.compile(r"</>")


class RenderCategory(str, Enum):
    UNCLOSED_TAG = "unclosed_tag"
    MISMATCHED_TAG = "mismatched_tag"
    UNBALANCED_BRACES = "unbalanced_braces"
    UNCLOSED_STRING = "unclosed_string"
    INVALID_IMPORT = "invalid_import"
    UNCLOSED_FRAGMENT = "unclosed_fragment"
    SYNTAX_ERROR = "syntax_error"


def _violation(
    category: RenderCategory,
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


_IMPORT_PATTERN = re.compile(
    r"^\s*import\s+(?:type\s+)?(?:[\w*{}\s,]+)\s+from\s+['\"][^'\"]+['\"]\s*;?\s*$",
    re.MULTILINE,
)
_BARE_IMPORT = re.compile(
    r"^\s*import\s+['\"][^'\"]+['\"]\s*;?\s*$",
    re.MULTILINE,
)


def _check_brace_balance(source: str) -> list[BaseViolation]:
    violations: list[BaseViolation] = []
    stripped = strip_strings_and_comments(source)
    pairs = {"(": ")", "{": "}", "[": "]"}
    closers = {v: k for k, v in pairs.items()}
    stack: list[tuple[str, int]] = []

    for i, ch in enumerate(stripped):
        if ch in pairs:
            stack.append((ch, i))
        elif ch in closers:
            if not stack or stack[-1][0] != closers[ch]:
                line, col = line_col(source, i)
                violations.append(
                    _violation(
                        RenderCategory.UNBALANCED_BRACES,
                        f"Unexpected '{ch}' without matching opener",
                        line=line,
                        column=col,
                        snippet=snippet_at(source, i),
                    )
                )
                return violations
            stack.pop()

    if stack:
        opener, pos = stack[-1]
        line, col = line_col(source, pos)
        violations.append(
            _violation(
                RenderCategory.UNBALANCED_BRACES,
                f"Unclosed '{opener}'",
                line=line,
                column=col,
                snippet=snippet_at(source, pos),
            )
        )
    return violations


def _check_string_literals(source: str) -> list[BaseViolation]:
    violations: list[BaseViolation] = []
    i = 0
    n = len(source)
    while i < n:
        ch = source[i]
        if ch in "\"'`":
            quote = ch
            i += 1
            escaped = False
            while i < n:
                if escaped:
                    escaped = False
                elif source[i] == "\\":
                    escaped = True
                elif source[i] == quote:
                    break
                i += 1
            else:
                line, col = line_col(source, i - 1)
                violations.append(
                    _violation(
                        RenderCategory.UNCLOSED_STRING,
                        f"Unclosed {quote} string literal",
                        line=line,
                        column=col,
                        snippet=snippet_at(source, i - 1),
                    )
                )
                return violations
        elif ch == "/" and i + 1 < n and source[i + 1] == "/":
            i = source.find("\n", i)
            if i == -1:
                break
        elif ch == "/" and i + 1 < n and source[i + 1] == "*":
            end = source.find("*/", i + 2)
            if end == -1:
                line, col = line_col(source, i)
                violations.append(
                    _violation(
                        RenderCategory.SYNTAX_ERROR,
                        "Unclosed block comment",
                        line=line,
                        column=col,
                    )
                )
                return violations
            i = end + 2
            continue
        i += 1
    return violations


def _check_tag_balance(source: str) -> list[BaseViolation]:
    violations: list[BaseViolation] = []
    elements = extract_elements(source)
    stack: list[tuple[str, int, int]] = []

    for el in elements:
        if el.is_closing:
            if not stack:
                violations.append(
                    _violation(
                        RenderCategory.MISMATCHED_TAG,
                        f"Closing </{el.tag}> without matching opener",
                        line=el.line,
                        column=el.column,
                    )
                )
                continue
            opener_tag, opener_line, opener_col = stack.pop()
            if opener_tag != el.tag:
                violations.append(
                    _violation(
                        RenderCategory.MISMATCHED_TAG,
                        f"</{el.tag}> does not match <{opener_tag}>",
                        line=el.line,
                        column=el.column,
                        snippet=f"<{opener_tag}> at line {opener_line}",
                    )
                )
        elif not el.self_closing:
            stack.append((el.tag, el.line, el.column))

    for tag, line, col in reversed(stack):
        violations.append(
            _violation(
                RenderCategory.UNCLOSED_TAG,
                f"Unclosed <{tag}>",
                line=line,
                column=col,
            )
        )

    return violations


def _check_fragments(source: str) -> list[BaseViolation]:
    stripped = strip_strings_and_comments(source)
    opens = len(FRAGMENT_OPEN.findall(stripped))
    closes = len(FRAGMENT_CLOSE.findall(stripped))
    if opens != closes:
        return [
            _violation(
                RenderCategory.UNCLOSED_FRAGMENT,
                f"Fragment count mismatch: {opens} <> vs {closes} </>",
            )
        ]
    return []


def _check_imports(source: str) -> list[BaseViolation]:
    violations: list[BaseViolation] = []
    for match in re.finditer(r"^\s*import\b.*$", source, re.MULTILINE):
        line_text = match.group(0).strip()
        if _IMPORT_PATTERN.match(line_text) or _BARE_IMPORT.match(line_text):
            continue
        # import { x } from "y" without from
        if "from" not in line_text and not _BARE_IMPORT.match(line_text):
            # side-effect import like import "./styles.css" is valid
            if re.match(r"""import\s+['"][^'"]+['"]""", line_text):
                continue
            line, col = line_col(source, match.start())
            violations.append(
                _violation(
                    RenderCategory.INVALID_IMPORT,
                    f"Malformed import statement",
                    line=line,
                    column=col,
                    snippet=line_text[:80],
                )
            )
    return violations


def validate_source(source: str) -> BaseResult:
    """Check whether generated code is syntactically usable."""
    result = BaseResult(layer="render")
    violations: list[BaseViolation] = []

    checks = [
        _check_string_literals(source),
        _check_brace_balance(source),
        _check_tag_balance(source),
        _check_fragments(source),
        _check_imports(source),
    ]

    for check_violations in checks:
        violations.extend(check_violations)

    # Total checks = number of parse passes (5) + tag/element count
    elements = extract_elements(source)
    result.total_checks = 5 + max(len(elements), 1)
    result.violations = violations
    result.passed = len(violations) == 0
    result.metadata = {
        "elements_found": len(elements),
        "syntax_valid": len(violations) == 0,
    }
    return result
