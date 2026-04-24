from __future__ import annotations

import argparse
from pathlib import Path

from comparator import compare_programs, ComparisonResult


BASE_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = BASE_DIR / "samples"
REPORT_PATH = BASE_DIR / "reporte_similitud.md"


def format_block(lines: list[str]) -> str:
    return "\n".join(lines) if lines else "(sin contenido)"


def build_section(lines: list[str], result: ComparisonResult, title: str) -> None:
    lines.append(f"## {title}")
    lines.append(f"- Estrategia: `{result.strategy}`")
    lines.append(f"- Modo: `{result.mode}`")
    lines.append(f"- Algoritmo: `{result.algorithm}`")
    lines.append(f"- Similitud: {result.similarity_percent:.2f}%")
    lines.append(f"- Unidades comunes: {result.matched_units}")
    lines.append(f"- Secciones detectadas: {len(result.matches)}")
    if result.suffix_array_size:
        lines.append(f"- Tamano suffix array: {result.suffix_array_size}")
        lines.append(f"- Vista BWT: `{result.bwt_preview}`")
    lines.append("")

    if not result.matches:
        lines.append("No se encontraron subcadenas comunes con el umbral configurado.")
        lines.append("")
        return

    for index, match in enumerate(result.matches, start=1):
        lines.append(
            f"### Seccion {index}: A[{match.start_a}-{match.end_a}] y "
            f"B[{match.start_b}-{match.end_b}] ({match.length} lineas/unidades)"
        )
        lines.append("")
        lines.append(f"**Fragmento en {result.file_a.name}**")
        lines.append("")
        lines.append("```python")
        lines.append(format_block(match.lines_a))
        lines.append("```")
        lines.append("")
        lines.append(f"**Fragmento en {result.file_b.name}**")
        lines.append("")
        lines.append("```python")
        lines.append(format_block(match.lines_b))
        lines.append("```")
        lines.append("")
        if match.diff_lines:
            lines.append("**Diff del bloque**")
            lines.append("")
            lines.append("```diff")
            lines.append(format_block(match.diff_lines))
            lines.append("```")
            lines.append("")


def build_report(file_a: Path, file_b: Path) -> str:
    results = {
        ("diff", "plain_text"): compare_programs(file_a, file_b, mode="plain_text", strategy="diff"),
        ("diff", "preprocessed"): compare_programs(file_a, file_b, mode="preprocessed", strategy="diff"),
        ("suffix_array", "plain_text"): compare_programs(file_a, file_b, mode="plain_text", strategy="suffix_array"),
        ("suffix_array", "preprocessed"): compare_programs(file_a, file_b, mode="preprocessed", strategy="suffix_array"),
    }

    lines: list[str] = []
    lines.append("# Reporte de similitud entre programas Python")
    lines.append("")
    lines.append("## Base conceptual")
    lines.append(
        "La solucion se presenta como dos comparadores separados, para cubrir de forma explicita la consigna: "
        "un comparador basado en diff y un comparador basado en suffix array/BWT. "
        "Cada uno se ejecuta en texto llano y en texto preprocesado."
    )
    lines.append("")
    lines.append("## Archivos comparados")
    lines.append(f"- Programa A: `{file_a.name}`")
    lines.append(f"- Programa B: `{file_b.name}`")
    lines.append("")
    lines.append("## Medida de similitud propuesta")
    lines.append(
        "Se usa la cobertura total de las subcadenas comunes detectadas, dividida entre la longitud del programa mas corto."
    )
    lines.append("")
    lines.append("```text")
    lines.append("similitud = (matched_units / longitud_programa_mas_corto) * 100")
    lines.append("```")
    lines.append("")
    lines.append("## Resumen comparativo")
    for key in [
        ("diff", "plain_text"),
        ("diff", "preprocessed"),
        ("suffix_array", "plain_text"),
        ("suffix_array", "preprocessed"),
    ]:
        result = results[key]
        lines.append(
            f"- {result.strategy} / {result.mode}: {result.similarity_percent:.2f}% "
            f"de similitud, {result.matched_units} unidades comunes, {len(result.matches)} secciones."
        )
    lines.append("")

    build_section(lines, results[("diff", "plain_text")], "Comparador 1: Diff en texto llano")
    build_section(lines, results[("diff", "preprocessed")], "Comparador 1: Diff en texto preprocesado")
    build_section(lines, results[("suffix_array", "plain_text")], "Comparador 2: Suffix Array/BWT en texto llano")
    build_section(lines, results[("suffix_array", "preprocessed")], "Comparador 2: Suffix Array/BWT en texto preprocesado")

    lines.append("## Conclusiones")
    lines.append(
        "El comparador basado en diff ofrece una solucion directa apoyada en utilidades de comparacion de secuencias, "
        "mientras que el comparador basado en suffix array/BWT resuelve la busqueda desde una estructura clasica sobre sufijos. "
        "La variante preprocesada es la que mejor evidencia similitud estructural con renombrado."
    )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera un reporte de similitud entre dos programas Python.")
    parser.add_argument("file_a", nargs="?", default=str(SAMPLES_DIR / "programa_a.py"))
    parser.add_argument("file_b", nargs="?", default=str(SAMPLES_DIR / "programa_b.py"))
    parser.add_argument("--output", default=str(REPORT_PATH))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_a = Path(args.file_a).resolve()
    file_b = Path(args.file_b).resolve()
    output = Path(args.output).resolve()

    report = build_report(file_a, file_b)
    output.write_text(report, encoding="utf-8")
    print(f"Reporte generado en: {output}")


if __name__ == "__main__":
    main()
