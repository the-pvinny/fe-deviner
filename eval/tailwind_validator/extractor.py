"""Extract Tailwind class strings from React/JSX/HTML source."""

from __future__ import annotations

import re
from dataclasses import dataclass

# className="..." or className='...'
CLASSNAME_STRING = re.compile(
    r"""className\s*=\s*(["'`])(?P<content>(?:\\.|(?!\1).)*)\1""",
    re.DOTALL,
)

# class="..." for HTML
HTML_CLASS = re.compile(
    r"""class\s*=\s*(["'`])(?P<content>(?:\\.|(?!\1).)*)\1""",
    re.DOTALL,
)

# cn("...", "...", `...`) — capture string literal arguments only
CN_CALL = re.compile(
    r"""cn\s*\((?P<args>[^)]*)\)""",
    re.DOTALL,
)

CN_STRING_ARG = re.compile(
    r"""["'`](?P<content>(?:\\.|[^"'`])*)["'`]""",
    re.DOTALL,
)


@dataclass(frozen=True)
class ClassOccurrence:
    """A class string found in source with location metadata."""

    classes: str
    line: int
    column: int
    source: str  # "className", "class", or "cn"


def _line_col(source: str, pos: int) -> tuple[int, int]:
    line = source.count("\n", 0, pos) + 1
    last_nl = source.rfind("\n", 0, pos)
    column = pos - last_nl if last_nl >= 0 else pos + 1
    return line, column


def _split_class_tokens(raw: str) -> list[str]:
    """Split a class string into individual utility tokens."""
    cleaned = raw.replace("\\n", " ").replace("\\t", " ")
    return [token for token in cleaned.split() if token]


def extract_class_strings(source: str) -> list[ClassOccurrence]:
    """Return all class string occurrences from JSX/HTML source."""
    occurrences: list[ClassOccurrence] = []

    for pattern, label in ((CLASSNAME_STRING, "className"), (HTML_CLASS, "class")):
        for match in pattern.finditer(source):
            line, col = _line_col(source, match.start())
            occurrences.append(
                ClassOccurrence(
                    classes=match.group("content"),
                    line=line,
                    column=col,
                    source=label,
                )
            )

    for cn_match in CN_CALL.finditer(source):
        args = cn_match.group("args")
        line, col = _line_col(source, cn_match.start())
        for arg_match in CN_STRING_ARG.finditer(args):
            occurrences.append(
                ClassOccurrence(
                    classes=arg_match.group("content"),
                    line=line,
                    column=col,
                    source="cn",
                )
            )

    return occurrences


def extract_classes(source: str) -> list[tuple[str, ClassOccurrence]]:
    """Return individual class tokens paired with their source occurrence."""
    result: list[tuple[str, ClassOccurrence]] = []
    for occurrence in extract_class_strings(source):
        for token in _split_class_tokens(occurrence.classes):
            result.append((token, occurrence))
    return result
