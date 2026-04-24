from __future__ import annotations

import argparse
from pathlib import Path

from comparator import compare_programs


BASE_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = BASE_DIR / "samples"
REPORT_PATH = BASE_DIR / "reporte_similitud.md"


def format_block(lines: list[str]) -> str:
    return "\n".join(lines) if lines else "(sin contenido)"


def build_report(file_a: Path, file_b: Path) -> str:
    plain = compare_programs(file_a, file_b, mode="plain_text")
    preprocessed = compare_programs(file_a, file_b, mode="preprocessed")

    lines: list[str] = []
    lines.append("# Reporte de similitud entre programas Python")
    lines.append("")
    lines.append("## Base conceptual")
    lines.append(
        "La solucion retoma dos ideas centrales del articulo `A Program for Identifying Duplicated Code`: "
        "comparar por secuencias lineales y, en una segunda variante, aplicar un preprocesamiento que "
        "permita detectar coincidencias estructurales aunque cambien nombres de variables o literales. "
        "La deteccion de subcadenas comunes se implementa con suffix array, LCP y BWT."
    )
    lines.append("")
    lines.append("## Archivos comparados")
    lines.append(f"- Programa A: `{file_a.name}`")
    lines.append(f"- Programa B: `{file_b.name}`")
    lines.append("")
    lines.append("## Algoritmo")
    lines.append(f"- Variante texto llano: `{plain.algorithm}`")
    lines.append(f"- Variante preprocesada: `{preprocessed.algorithm}`")
    lines.append(f"- Tamano suffix array texto llano: {plain.suffix_array_size}")
    lines.append(f"- Tamano suffix array preprocesado: {preprocessed.suffix_array_size}")
    lines.append(f"- Vista BWT texto llano: `{plain.bwt_preview}`")
    lines.append(f"- Vista BWT preprocesado: `{preprocessed.bwt_preview}`")
    lines.append("")
    lines.append("## Medida de similitud propuesta")
    lines.append(
        "Se usa la cobertura total de las subcadenas comunes reportadas por el analisis con suffix array/LCP, "
        "dividida entre la longitud del programa mas corto. La formula es:"
    )
    lines.append("")
    lines.append("```text")
    lines.append("similitud = (suma_longitudes_subcadenas_comunes / longitud_programa_mas_corto) * 100")
    lines.append("```")
    lines.append("")
    lines.append("## Resumen cuantitativo")
    lines.append(
        f"- Texto llano: {plain.similarity_percent:.2f}% de similitud, "
        f"{plain.matched_units} lineas/unidades comunes, "
        f"{len(plain.matches)} secciones detectadas."
    )
    lines.append(
        f"- Texto preprocesado: {preprocessed.similarity_percent:.2f}% de similitud, "
        f"{preprocessed.matched_units} lineas/unidades comunes, "
        f"{len(preprocessed.matches)} secciones detectadas."
    )
    lines.append("")

    for result, title in [
        (plain, "Texto llano"),
        (preprocessed, "Texto preprocesado"),
    ]:
        lines.append(f"## Coincidencias encontradas: {title}")
        if not result.matches:
            lines.append("No se encontraron subcadenas comunes con el umbral configurado.")
            lines.append("")
            continue

        for index, match in enumerate(result.matches, start=1):
            lines.append(
                f"### Seccion {index}: A[{match.start_a}-{match.end_a}] y B[{match.start_b}-{match.end_b}] "
                f"({match.length} lineas/unidades)"
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

    lines.append("## Conclusiones")
    lines.append(
        "La comparacion en texto llano solo detecta coincidencias literales, mientras que la comparacion "
        "preprocesada encuentra bloques con la misma estructura aun cuando cambian identificadores, "
        "constantes o cadenas. El uso de suffix array y BWT permite justificar que la busqueda de subcadenas "
        "comunes ya no depende de `SequenceMatcher`, sino de una estructura clasica de busqueda sobre sufijos."
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
