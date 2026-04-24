from pathlib import Path
from itertools import combinations
from comparator import compare_programs

DATASET_DIR = Path("samples/dataset")
archivos = sorted(DATASET_DIR.glob("*.py"))
print(f"Archivos encontrados: {len(archivos)}")

if not archivos:
    print("ERROR: no se encontraron archivos en samples/dataset/")
    exit()

resultados = []
pares = list(combinations(archivos, 2))
print(f"Comparando {len(pares)} pares...\n")

for i, (a, b) in enumerate(pares, 1):
    print(f"[{i}/{len(pares)}] {a.name} vs {b.name}", end="... ")
    plain = compare_programs(a, b, mode="plain_text")
    prep  = compare_programs(a, b, mode="preprocessed")
    resultados.append((a.name, b.name, plain.similarity_percent, prep.similarity_percent))
    print(f"llano={plain.similarity_percent:.1f}% | preprocesado={prep.similarity_percent:.1f}%")

# Guardar reporte
output = Path("reporte_dataset.md")
lines = ["# Resultados de comparación del dataset\n"]
lines.append(f"| Archivo A | Archivo B | Texto llano | Preprocesado |")
lines.append(f"|-----------|-----------|-------------|--------------|")
for a, b, p, pp in sorted(resultados, key=lambda x: x[3], reverse=True):
    lines.append(f"| {a} | {b} | {p:.1f}% | {pp:.1f}% |")

output.write_text("\n".join(lines), encoding="utf-8")
print(f"\nReporte guardado en: {output.resolve()}")