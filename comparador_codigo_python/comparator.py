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
SENTINEL_A = 0
SENTINEL_B = 1


@dataclass
class MatchSection:
    start_a: int
    end_a: int
    start_b: int
    end_b: int
    length: int
    lines_a: list[str]
    lines_b: list[str]
    diff_lines: list[str]


@dataclass
class PreparedSequence:
    normalized_units: list[str]
    display_units: list[list[str]]


@dataclass
class ComparisonResult:
    mode: str
    algorithm: str
    file_a: Path
    file_b: Path
    total_units_a: int
    total_units_b: int
    similarity_percent: float
    matched_units: int
    matches: list[MatchSection]
    suffix_array_size: int
    bwt_preview: list[int]


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


def preprocess_python(path: Path) -> PreparedSequence:
    source = path.read_text(encoding="utf-8")
    source_lines = source.splitlines()
    reader = io.StringIO(source).readline
    logical_lines: list[str] = []
    display_units: list[list[str]] = []
    current_tokens: list[str] = []
    current_start_line: int | None = None
    current_end_line: int | None = None

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
                start_line = current_start_line or tok.start[0]
                end_line = current_end_line or tok.end[0]
                display_units.append(source_lines[start_line - 1 : end_line])
                current_tokens = []
                current_start_line = None
                current_end_line = None
            continue

        if current_start_line is None:
            current_start_line = tok.start[0]
        current_end_line = tok.end[0]

        if tok_type == token.OP and tok_string in {"(", ")", "[", "]", "{", "}", ",", ":"}:
            current_tokens.append(tok_string)
            continue

        current_tokens.append(_token_placeholder(tok_type, tok_string))

    if current_tokens:
        logical_lines.append(" ".join(current_tokens))
        start_line = current_start_line or 1
        end_line = current_end_line or start_line
        display_units.append(source_lines[start_line - 1 : end_line])

    while logical_lines and not logical_lines[0].strip():
        logical_lines.pop(0)
        display_units.pop(0)
    while logical_lines and not logical_lines[-1].strip():
        logical_lines.pop()
        display_units.pop()

    return PreparedSequence(normalized_units=logical_lines, display_units=display_units)


def plain_text_lines(path: Path) -> PreparedSequence:
    filtered: list[str] = []
    display_units: list[list[str]] = []
    for line in _read_lines(path):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        clean_line = line.rstrip()
        filtered.append(clean_line)
        display_units.append([clean_line])
    return PreparedSequence(normalized_units=filtered, display_units=display_units)


def _encode_sequences(seq_a: list[str], seq_b: list[str]) -> tuple[list[int], list[int], dict[int, str]]:
    symbol_to_id: dict[str, int] = {}
    id_to_symbol: dict[int, str] = {}
    next_id = 2

    def encode_line(line: str) -> int:
        nonlocal next_id
        if line not in symbol_to_id:
            symbol_to_id[line] = next_id
            id_to_symbol[next_id] = line
            next_id += 1
        return symbol_to_id[line]

    encoded_a = [encode_line(line) for line in seq_a]
    encoded_b = [encode_line(line) for line in seq_b]
    return encoded_a, encoded_b, id_to_symbol


def build_suffix_array(sequence: list[int]) -> list[int]:
    return sorted(range(len(sequence)), key=lambda index: sequence[index:])


def build_lcp(sequence: list[int], suffix_array: list[int]) -> list[int]:
    rank = [0] * len(sequence)
    for index, suffix_start in enumerate(suffix_array):
        rank[suffix_start] = index

    lcp = [0] * len(sequence)
    common = 0
    for i in range(len(sequence)):
        position = rank[i]
        if position == 0:
            common = 0
            continue

        previous_suffix = suffix_array[position - 1]
        while (
            i + common < len(sequence)
            and previous_suffix + common < len(sequence)
            and sequence[i + common] == sequence[previous_suffix + common]
        ):
            common += 1
        lcp[position] = common
        if common:
            common -= 1
    return lcp


def build_bwt(sequence: list[int], suffix_array: list[int]) -> list[int]:
    return [sequence[index - 1] if index > 0 else sequence[-1] for index in suffix_array]


def _origin_for_index(index: int, len_a: int, len_b: int) -> tuple[str, int] | None:
    if index < len_a:
        return ("A", index)
    if index == len_a:
        return None
    offset_b = index - len_a - 1
    if 0 <= offset_b < len_b:
        return ("B", offset_b)
    return None


def _common_prefix_length(sequence: list[int], left: int, right: int, stop_a: int, stop_b: int) -> int:
    length = 0
    while left + length < len(sequence) and right + length < len(sequence):
        left_value = sequence[left + length]
        right_value = sequence[right + length]
        if left_value in {stop_a, stop_b} or right_value in {stop_a, stop_b}:
            break
        if left_value != right_value:
            break
        length += 1
    return length


def _build_diff(lines_a: list[str], lines_b: list[str], file_a: Path, file_b: Path) -> list[str]:
    return list(
        difflib.unified_diff(
            lines_a,
            lines_b,
            fromfile=file_a.name,
            tofile=file_b.name,
            lineterm="",
        )
    )


def _filter_maximal_matches(matches: list[MatchSection]) -> list[MatchSection]:
    matches.sort(key=lambda item: (item.start_a, item.start_b, -item.length))
    filtered: list[MatchSection] = []
    seen: set[tuple[int, int, int, int]] = set()

    for candidate in matches:
        key = (candidate.start_a, candidate.end_a, candidate.start_b, candidate.end_b)
        if key in seen:
            continue

        contained = False
        for existing in filtered:
            if (
                candidate.start_a >= existing.start_a
                and candidate.end_a <= existing.end_a
                and candidate.start_b >= existing.start_b
                and candidate.end_b <= existing.end_b
            ):
                contained = True
                break

        if not contained:
            filtered.append(candidate)
            seen.add(key)

    filtered.sort(key=lambda item: (-item.length, item.start_a, item.start_b))
    return filtered


def _extract_matches_from_suffix_array(
    encoded_a: list[int],
    encoded_b: list[int],
    original_a: list[str],
    original_b: list[str],
    display_a: list[list[str]],
    display_b: list[list[str]],
    file_a: Path,
    file_b: Path,
    min_match_lines: int,
) -> tuple[list[MatchSection], list[int], list[int]]:
    combined = encoded_a + [SENTINEL_A] + encoded_b + [SENTINEL_B]
    suffix_array = build_suffix_array(combined)
    lcp = build_lcp(combined, suffix_array)
    bwt = build_bwt(combined, suffix_array)
    raw_matches: list[MatchSection] = []

    for i in range(1, len(suffix_array)):
        left_start = suffix_array[i - 1]
        right_start = suffix_array[i]
        left_origin = _origin_for_index(left_start, len(encoded_a), len(encoded_b))
        right_origin = _origin_for_index(right_start, len(encoded_a), len(encoded_b))

        if left_origin is None or right_origin is None:
            continue
        if left_origin[0] == right_origin[0]:
            continue

        length = min(
            lcp[i],
            _common_prefix_length(combined, left_start, right_start, SENTINEL_A, SENTINEL_B),
        )
        if length < min_match_lines:
            continue

        if left_origin[0] == "A":
            start_a = left_origin[1]
            start_b = right_origin[1]
        else:
            start_a = right_origin[1]
            start_b = left_origin[1]

        lines_a = [line for block in display_a[start_a : start_a + length] for line in block]
        lines_b = [line for block in display_b[start_b : start_b + length] for line in block]
        raw_matches.append(
            MatchSection(
                start_a=start_a + 1,
                end_a=start_a + length,
                start_b=start_b + 1,
                end_b=start_b + length,
                length=length,
                lines_a=lines_a,
                lines_b=lines_b,
                diff_lines=_build_diff(lines_a, lines_b, file_a, file_b),
            )
        )

    return _filter_maximal_matches(raw_matches), suffix_array, bwt


def _similarity_percentage(matches: list[MatchSection], total_a: int, total_b: int) -> tuple[float, int]:
    covered_a: set[int] = set()
    covered_b: set[int] = set()

    for match in matches:
        covered_a.update(range(match.start_a - 1, match.end_a))
        covered_b.update(range(match.start_b - 1, match.end_b))

    matched_units = min(len(covered_a), len(covered_b))
    base = min(total_a, total_b) or 1
    return (matched_units / base) * 100.0, matched_units


def compare_programs(file_a: Path, file_b: Path, mode: str, min_match_lines: int = MIN_MATCH_LINES) -> ComparisonResult:
    if mode == "plain_text":
        prepared_a = plain_text_lines(file_a)
        prepared_b = plain_text_lines(file_b)
    elif mode == "preprocessed":
        prepared_a = preprocess_python(file_a)
        prepared_b = preprocess_python(file_b)
    else:
        raise ValueError(f"Modo no soportado: {mode}")

    seq_a = prepared_a.normalized_units
    seq_b = prepared_b.normalized_units
    encoded_a, encoded_b, _ = _encode_sequences(seq_a, seq_b)
    matches, suffix_array, bwt = _extract_matches_from_suffix_array(
        encoded_a=encoded_a,
        encoded_b=encoded_b,
        original_a=seq_a,
        original_b=seq_b,
        display_a=prepared_a.display_units,
        display_b=prepared_b.display_units,
        file_a=file_a,
        file_b=file_b,
        min_match_lines=min_match_lines,
    )
    similarity_percent, matched_units = _similarity_percentage(matches, len(seq_a), len(seq_b))

    return ComparisonResult(
        mode=mode,
        algorithm="suffix_array + lcp + bwt + difflib.unified_diff",
        file_a=file_a,
        file_b=file_b,
        total_units_a=len(seq_a),
        total_units_b=len(seq_b),
        similarity_percent=similarity_percent,
        matched_units=matched_units,
        matches=matches,
        suffix_array_size=len(suffix_array),
        bwt_preview=bwt[:20],
    )
