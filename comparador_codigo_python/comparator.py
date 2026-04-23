from __future__ import annotations

from dataclasses import dataclass
import difflib
import io
import keyword
from pathlib import Path
import token
import tokenize
from typing import Iterable


MIN_MATCH_LINES = 3


@dataclass
class MatchSection:
    start_a: int
    end_a: int
    start_b: int
    end_b: int
    length: int
    lines_a: list[str]
    lines_b: list[str]


@dataclass
class ComparisonResult:
    mode: str
    file_a: Path
    file_b: Path
    total_units_a: int
    total_units_b: int
    similarity_percent: float
    matched_units: int
    matches: list[MatchSection]


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _strip_empty_edges(lines: Iterable[str]) -> list[str]:
    cleaned = [line.rstrip() for line in lines]
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    return cleaned


def _token_placeholder(tok_type: int, tok_string: str) -> str:
    if tok_type == token.NAME:
        return tok_string if keyword.iskeyword(tok_string) else "ID"
    if tok_type == token.NUMBER:
        return "NUM"
    if tok_type == token.STRING:
        return "STR"
    return tok_string


def preprocess_python(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    reader = io.StringIO(source).readline
    logical_lines: list[str] = []
    current_tokens: list[str] = []

    for tok in tokenize.generate_tokens(reader):
        tok_type = tok.type
        tok_string = tok.string

        if tok_type in {
            token.ENCODING,
            token.ENDMARKER,
            token.INDENT,
            token.DEDENT,
            token.NL,
            token.NEWLINE,
            token.COMMENT,
        }:
            if tok_type == token.NEWLINE and current_tokens:
                logical_lines.append(" ".join(current_tokens))
                current_tokens = []
            continue

        if tok_type == token.OP and tok_string in {"(", ")", "[", "]", "{", "}", ",", ":"}:
            current_tokens.append(tok_string)
            continue

        current_tokens.append(_token_placeholder(tok_type, tok_string))

    if current_tokens:
        logical_lines.append(" ".join(current_tokens))

    return _strip_empty_edges(logical_lines)


def plain_text_lines(path: Path) -> list[str]:
    filtered: list[str] = []
    for line in _read_lines(path):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        filtered.append(line.rstrip())
    return filtered


def _extract_matches(
    seq_a: list[str],
    seq_b: list[str],
    original_a: list[str],
    original_b: list[str],
    min_match_lines: int,
) -> list[MatchSection]:
    matcher = difflib.SequenceMatcher(a=seq_a, b=seq_b, autojunk=False)
    blocks = matcher.get_matching_blocks()
    matches: list[MatchSection] = []

    for block in blocks:
        if block.size < min_match_lines:
            continue
        matches.append(
            MatchSection(
                start_a=block.a + 1,
                end_a=block.a + block.size,
                start_b=block.b + 1,
                end_b=block.b + block.size,
                length=block.size,
                lines_a=original_a[block.a : block.a + block.size],
                lines_b=original_b[block.b : block.b + block.size],
            )
        )
    return matches


def _similarity_percentage(matches: list[MatchSection], total_a: int, total_b: int) -> tuple[float, int]:
    matched_units = sum(match.length for match in matches)
    base = min(total_a, total_b) or 1
    return (matched_units / base) * 100.0, matched_units


def compare_programs(file_a: Path, file_b: Path, mode: str, min_match_lines: int = MIN_MATCH_LINES) -> ComparisonResult:
    if mode == "plain_text":
        seq_a = plain_text_lines(file_a)
        seq_b = plain_text_lines(file_b)
    elif mode == "preprocessed":
        seq_a = preprocess_python(file_a)
        seq_b = preprocess_python(file_b)
    else:
        raise ValueError(f"Modo no soportado: {mode}")

    original_a = seq_a
    original_b = seq_b
    matches = _extract_matches(seq_a, seq_b, original_a, original_b, min_match_lines)
    similarity_percent, matched_units = _similarity_percentage(matches, len(seq_a), len(seq_b))

    return ComparisonResult(
        mode=mode,
        file_a=file_a,
        file_b=file_b,
        total_units_a=len(seq_a),
        total_units_b=len(seq_b),
        similarity_percent=similarity_percent,
        matched_units=matched_units,
        matches=matches,
    )
