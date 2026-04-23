# Comparador de codigo Python

Esta carpeta contiene una implementacion inspirada en el articulo
`A Program for Identifying Duplicated Code` de Brenda S. Baker.

Incluye dos variantes de comparacion con `difflib.SequenceMatcher`:

- `plain_text`: compara programas por lineas tal como aparecen.
- `preprocessed`: elimina comentarios/espacios irrelevantes y reemplaza
  identificadores y literales por marcadores para detectar similitud
  estructural.

Tambien se incluyen dos programas de ejemplo de autoria propia y un script
que genera un reporte con los fragmentos comunes y un porcentaje de
similitud.

## Archivos

- `comparator.py`: logica del comparador.
- `generate_report.py`: genera el documento `reporte_similitud.md`.
- `samples/programa_a.py`: primer programa de ejemplo.
- `samples/programa_b.py`: segundo programa de ejemplo.

## Ejecucion

```powershell
C:\Users\EMIS4\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe generate_report.py
```

Tambien puedes comparar tus propios archivos:

```powershell
C:\Users\EMIS4\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe generate_report.py ruta\programa1.py ruta\programa2.py --output ruta\reporte.md
```
