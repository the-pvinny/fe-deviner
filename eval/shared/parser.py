"""Shared utilities for eval layers."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BaseViolation:
    category: str
    message: str
    line: int | None = None
    column: int | None = None
    snippet: str | None = None


@dataclass
class BaseResult:
    layer: str
    total_checks: int = 0
    violations: list[BaseViolation] = field(default_factory=list)
    passed: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    @property
    def violation_rate(self) -> float:
        if self.total_checks == 0:
            return 0.0
        return self.violation_count / self.total_checks

    @property
    def pass_rate(self) -> float:
        return 1.0 - self.violation_rate

    def violations_by_category(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for v in self.violations:
            counts[v.category] = counts.get(v.category, 0) + 1
        return counts


def line_col(source: str, pos: int) -> tuple[int, int]:
    line = source.count("\n", 0, pos) + 1
    last_nl = source.rfind("\n", 0, pos)
    column = pos - last_nl if last_nl >= 0 else pos + 1
    return line, column


def snippet_at(source: str, pos: int, length: int = 60) -> str:
    start = max(0, pos - 10)
    end = min(len(source), pos + length)
    text = source[start:end].replace("\n", " ")
    return text.strip()


# Strip strings and comments so tag/brace parsers ignore code inside literals.
_STRING_PATTERN = re.compile(
    r"""
    (/\*.*?\*/)|           # block comment
    (//[^\n]*)|            # line comment
    (\{/\*.*?\*/\})|       # JSX comment
    ("(?:\\.|[^"\\])*")|  # double-quoted
    ('(?:\\.|[^'\\])*')|  # single-quoted
    (`(?:\\.|[^`\\])*`)    # template literal (no ${} nesting)
    """,
    re.DOTALL | re.VERBOSE,
)


def strip_strings_and_comments(source: str) -> str:
    """Replace strings/comments with spaces, preserving length for position mapping."""

    def replacer(match: re.Match[str]) -> str:
        return " " * len(match.group(0))

    return _STRING_PATTERN.sub(replacer, source)


@dataclass(frozen=True)
class Element:
    tag: str
    attrs: dict[str, str]
    raw_attrs: str
    line: int
    column: int
    self_closing: bool
    is_closing: bool
    inner_start: int | None = None
    inner_end: int | None = None


_ATTR_PATTERN = re.compile(
    r"""
    (?P<spread>\{\.\.\.[\w.]+\})|
    (?P<name>@?\w[\w:-]*)
    (?:=(?P<value>
        "(?:\\.|[^"\\])*"|
        '(?:\\.|[^'\\])*'|
        \{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}
    ))?
    """,
    re.VERBOSE,
)

_TAG_PATTERN = re.compile(
    r"<(?P<closing>/)?(?P<name>[A-Za-z][\w.-]*)(?P<attrs>[^>]*?)/?>",
)

_VOID_ELEMENTS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "source",
        "track",
        "wbr",
    }
)


def _parse_attrs(raw: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for match in _ATTR_PATTERN.finditer(raw):
        if match.group("spread"):
            continue
        name = match.group("name")
        if not name:
            continue
        value = match.group("value") or "true"
        attrs[name.lower()] = value
    return attrs


def extract_elements(source: str) -> list[Element]:
    """Extract JSX/HTML elements from source (strings/comments stripped for matching)."""
    stripped = strip_strings_and_comments(source)
    elements: list[Element] = []

    for match in _TAG_PATTERN.finditer(stripped):
        tag = match.group("name")
        is_closing = bool(match.group("closing"))
        tag_start = match.start()
        tag_end = match.end()
        tag_text = source[tag_start:tag_end]
        attrs_match = re.match(
            rf"<(?:/)?{re.escape(tag)}(?P<attrs>[^>]*)/?>",
            tag_text,
            re.DOTALL,
        )
        raw_attrs = attrs_match.group("attrs") if attrs_match else (match.group("attrs") or "")
        self_closing = tag_text.rstrip().endswith("/>") or tag.lower() in _VOID_ELEMENTS
        line, col = line_col(source, tag_start)
        elements.append(
            Element(
                tag=tag,
                attrs=_parse_attrs(raw_attrs),
                raw_attrs=raw_attrs,
                line=line,
                column=col,
                self_closing=self_closing,
                is_closing=is_closing,
                inner_start=tag_end if not is_closing and not self_closing else None,
            )
        )

    return elements


def extract_inner_text(source: str, open_pos: int, close_pos: int) -> str:
    return source[open_pos:close_pos]


def find_matching_close(source: str, open_index: int, elements: list[Element]) -> int | None:
    """Find index of closing element matching elements[open_index]."""
    opener = elements[open_index]
    if opener.self_closing or opener.is_closing:
        return None

    depth = 1
    for i in range(open_index + 1, len(elements)):
        el = elements[i]
        if el.tag != opener.tag:
            continue
        if el.is_closing:
            depth -= 1
            if depth == 0:
                return i
        elif not el.self_closing:
            depth += 1
    return None


def has_attr(attrs: dict[str, str], *names: str) -> bool:
    lowered = {k.lower(): v for k, v in attrs.items()}
    for name in names:
        if name.lower() in lowered:
            return True
    return False


def attr_value(attrs: dict[str, str], name: str) -> str | None:
    for key, value in attrs.items():
        if key.lower() == name.lower():
            return value.strip("\"'")
    return None


def class_names(attrs: dict[str, str]) -> str:
    """Return flattened className/class string content."""
    for k, v in attrs.items():
        if k.lower() in ("classname", "class"):
            return v.strip("\"'")
    return ""


def has_focus_visible(class_str: str) -> bool:
    return "focus-visible" in class_str


def is_pascal_case(name: str) -> bool:
    return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))
