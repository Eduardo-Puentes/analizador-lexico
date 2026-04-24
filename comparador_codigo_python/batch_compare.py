from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

from comparator import compare_programs


DEFAULT_DATASET_DIR = Path("samples/dataset")
DEFAULT_OUTPUT = Path("reporte_dataset.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compara todos los pares de archivos Python dentro de un dataset."
    )
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET_DIR), help="Carpeta que contiene archivos .py")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Ruta del archivo Markdown de salida")
    parser.add_argument(
        "--strategy",
        choices=["diff", "suffix_array"],
        default="suffix_array",
        help="Comparador a usar sobre el dataset",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_dir = Path(args.dataset).resolve()
    output = Path(args.output).resolve()
    strategy = args.strategy

    archivos = sorted(dataset_dir.glob("*.py"))
    print(f"Dataset: {dataset_dir}")
    print(f"Archivos encontrados: {len(archivos)}")

    if not archivos:
        raise SystemExit(f"ERROR: no se encontraron archivos .py en {dataset_dir}")

    resultados = []
    pares = list(combinations(archivos, 2))
    print(f"Comparando {len(pares)} pares...\n")

    for index, (a, b) in enumerate(pares, start=1):
        print(f"[{index}/{len(pares)}] {a.name} vs {b.name}", end="... ")
        plain = compare_programs(a, b, mode="plain_text", strategy=strategy)
        preprocessed = compare_programs(a, b, mode="preprocessed", strategy=strategy)
        resultados.append((a.name, b.name, plain.similarity_percent, preprocessed.similarity_percent))
        print(
            f"llano={plain.similarity_percent:.1f}% | "
            f"preprocesado={preprocessed.similarity_percent:.1f}%"
        )

    lines = ["# Resultados de comparacion del dataset", ""]
    lines.append(f"- Dataset analizado: `{dataset_dir}`")
    lines.append(f"- Estrategia: `{strategy}`")
    lines.append(f"- Archivos: {len(archivos)}")
    lines.append(f"- Pares comparados: {len(pares)}")
    lines.append("")
    lines.append("| Archivo A | Archivo B | Texto llano | Preprocesado |")
    lines.append("|-----------|-----------|-------------|--------------|")
    for a, b, plain, preprocessed in sorted(resultados, key=lambda item: item[3], reverse=True):
        lines.append(f"| {a} | {b} | {plain:.1f}% | {preprocessed:.1f}% |")

    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReporte guardado en: {output}")


if __name__ == "__main__":
    main()
