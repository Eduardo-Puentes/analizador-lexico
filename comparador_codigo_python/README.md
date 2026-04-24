# Comparador de codigo Python

Este proyecto implementa un comparador de similitud entre programas Python
inspirado en las ideas del articulo `A Program for Identifying Duplicated Code`
de Brenda S. Baker.

La solucion ahora se presenta como dos comparadores separados:

- `Comparador 1: diff`
- `Comparador 2: suffix array/BWT`

Cada comparador tiene dos modos:

- `plain_text`: compara lineas reales del programa.
- `preprocessed`: compara una version normalizada del programa para detectar
  similitud estructural aunque cambien nombres o literales.

Internamente, los enfoques quedan asi:

- `diff`: `difflib.SequenceMatcher` + `difflib.unified_diff`
- `suffix_array`: `suffix array` + `LCP` + `BWT` + `difflib.unified_diff`

## Requisitos

Este proyecto no agrega dependencias externas nuevas.
Usa solamente la biblioteca estandar de Python.

Si deseas instalar todas las dependencias del repositorio desde la raiz:

```bash
python3 -m pip install -r requirements.txt
```

Actualmente `requirements.txt` solo contiene `ply`, que es usado por el
proyecto `clang-analizador-lexico`.

## Como comparar dos programas

El script `generate_report.py` ejecuta ambas estrategias en una sola corrida:

- `Comparador 1: diff`
- `Comparador 2: suffix array/BWT`

Por eso, al comparar dos archivos con este script, el reporte incluye:

- `diff` en `plain_text`
- `diff` en `preprocessed`
- `suffix_array` en `plain_text`
- `suffix_array` en `preprocessed`

Comando general:

```powershell
python generate_report.py ruta\programa1.py ruta\programa2.py --output reporte_similitud.md
```

Ejemplo con los archivos incluidos:

```powershell
python generate_report.py samples\programa_a.py samples\programa_b.py --output reporte_similitud.md
```

El archivo `reporte_similitud.md` incluye:

- resultados del comparador basado en diff
- resultados del comparador basado en suffix array/BWT
- bloques similares encontrados
- fragmentos de codigo con indentacion real
- diff del bloque encontrado
- tamano del suffix array
- vista resumida de la BWT

En comparacion individual no necesitas elegir estrategia por parametro:
`generate_report.py` ejecuta ambas automaticamente.

## Como probar con un dataset

En comparacion por dataset si debes elegir explicitamente la estrategia.

### Dataset con `diff`

Para comparar todos los pares de archivos `.py` usando el comparador basado en
`diff`:

```powershell
python batch_compare.py --strategy diff --output reporte_dataset_diff.md
```

### Dataset con `suffix_array`

Para comparar todos los pares de archivos `.py` usando el comparador basado en
`suffix_array`:

```powershell
python batch_compare.py --strategy suffix_array --output reporte_dataset_suffix.md
```

Ambos comandos usan por defecto:

```text
samples/dataset/
```

El reporte del dataset contiene una tabla con:

- archivo A
- archivo B
- similitud en texto llano
- similitud en texto preprocesado

### Usar otro dataset con `diff`

```powershell
python batch_compare.py --dataset ruta\mi_dataset --output mi_reporte_diff.md --strategy diff
```

### Usar otro dataset con `suffix_array`

```powershell
python batch_compare.py --dataset ruta\mi_dataset --output mi_reporte_suffix.md --strategy suffix_array
```

La carpeta indicada debe contener archivos `.py`.

## Estructura del proyecto

- `comparator.py`: implementa el algoritmo principal.
- `generate_report.py`: ejecuta la comparacion de dos archivos y escribe un
  reporte detallado.
- `batch_compare.py`: ejecuta la comparacion sobre todos los pares de un dataset.
- `samples/programa_a.py` y `samples/programa_b.py`: ejemplos pequenos.
- `samples/dataset/`: conjunto de archivos para pruebas por lote.

## Explicacion interna

La idea central es tratar cada programa como una secuencia de unidades
comparables y buscar subcadenas comunes entre dos programas.

## Vista general del flujo

Internamente, el comparador `suffix_array` sigue este pipeline:

1. Lee dos archivos Python.
2. Convierte cada archivo en una secuencia de unidades.
3. Codifica cada unidad como un entero.
4. Concatena ambas secuencias con separadores centinela.
5. Construye el `suffix array` de la secuencia combinada.
6. Calcula el arreglo `LCP`.
7. Deriva la `BWT`.
8. Recorre sufijos adyacentes para encontrar prefijos comunes entre un sufijo
   que viene del programa A y otro que viene del programa B.
9. Filtra coincidencias contenidas dentro de bloques mayores.
10. Calcula una medida de similitud y genera el reporte.

## Modelado interno de datos

En `comparator.py` hay tres estructuras clave:

- `PreparedSequence`: representa un programa ya preparado para comparacion.
  Contiene:
  - `normalized_units`: secuencia que realmente usa el algoritmo.
  - `display_units`: bloques originales que luego se imprimen en el reporte.
- `MatchSection`: representa una coincidencia detectada entre ambos programas.
  Guarda posiciones, longitud, fragmentos y diff.
- `ComparisonResult`: resume toda una corrida de comparacion, incluyendo la
  estrategia usada, porcentaje de similitud, lista de matches, tamano del
  suffix array y una vista corta de la BWT.

## Preparacion de secuencias

La preparacion depende del modo de comparacion.

### Modo `plain_text`

La funcion `plain_text_lines()`:

- lee el archivo linea por linea
- elimina lineas vacias
- elimina lineas que empiezan con `#`
- conserva el texto de cada linea
- guarda esa misma linea como unidad visible para el reporte

Resultado:

- una unidad normalizada equivale a una linea del archivo
- una unidad visible tambien equivale a una linea del archivo

Este modo detecta solo coincidencias literales entre lineas reales.

### Modo `preprocessed`

La funcion `preprocess_python()` tokeniza el archivo usando `tokenize`.

La normalizacion sigue esta idea:

- `NAME`:
  - si es palabra reservada, se conserva
  - si es identificador, se reemplaza por `ID`
- `NUMBER`: se reemplaza por `NUM`
- `STRING`: se reemplaza por `STR`
- operadores y puntuacion relevantes se conservan
- comentarios no participan
- indentacion y dedent no participan como tokens de comparacion

Ejemplo conceptual:

```python
if cliente == "oro":
    descuento = total * 0.15
```

puede transformarse a algo parecido a:

```text
if ID == STR :
ID = ID * NUM
```

Esto permite que dos fragmentos con distinta nomenclatura sigan coincidiendo
si su forma estructural es la misma.

### Por que existen `display_units`

Aunque en `preprocessed` el algoritmo compara versiones normalizadas, el
reporte debe mostrar el codigo original con su indentacion real.

Por eso `preprocess_python()` no solo construye `normalized_units`, sino
tambien `display_units`. Cada unidad visible guarda las lineas reales del
archivo fuente que dieron origen a esa unidad normalizada.

Asi, el algoritmo compara una forma abstracta, pero el reporte ensena el
fragmento original legible.

## Codificacion a enteros

La funcion `_encode_sequences()` transforma ambas secuencias normalizadas en
una secuencia de enteros.

Ejemplo conceptual:

```text
"if ID == STR :" -> 2
"ID = ID * NUM" -> 3
"return ID" -> 4
```

Esto es util porque el `suffix array`, el `LCP` y la `BWT` trabajan de forma
natural sobre simbolos discretos.

Los enteros `0` y `1` se reservan como centinelas:

- `SENTINEL_A = 0`
- `SENTINEL_B = 1`

Entonces la secuencia combinada tiene esta forma:

```text
programa_A_codificado + [0] + programa_B_codificado + [1]
```

Los centinelas evitan que una coincidencia cruce artificialmente de un
programa al otro.

## Suffix array

La funcion `build_suffix_array()` construye el arreglo de sufijos de la
secuencia combinada.

Cada posicion `i` representa el sufijo:

```text
sequence[i:]
```

El `suffix array` es simplemente la lista de indices iniciales de todos los
sufijos, ordenados lexicograficamente por su contenido.

Ejemplo conceptual:

```text
Secuencia: [5, 2, 5, 1]
Sufijos:
0 -> [5, 2, 5, 1]
1 -> [2, 5, 1]
2 -> [5, 1]
3 -> [1]
```

Al ordenar esos sufijos, los que empiezan parecido quedan cerca. Esa es la
propiedad que aprovecha el comparador para encontrar subcadenas comunes.

## LCP

La funcion `build_lcp()` calcula el arreglo `LCP`.

`LCP[i]` representa la longitud del prefijo comun entre:

- el sufijo en `suffix_array[i]`
- el sufijo en `suffix_array[i - 1]`

Si dos sufijos adyacentes tienen un `LCP` alto, entonces comparten una
subcadena larga al inicio.

Eso es precisamente lo que el comparador interpreta como candidato a bloque
similar.

## BWT

La funcion `build_bwt()` deriva la `Burrows-Wheeler Transform` a partir del
`suffix array`.

Para cada sufijo ordenado, la BWT toma el simbolo anterior a ese sufijo en la
secuencia original.

En esta implementacion la `BWT` se usa principalmente para:

- respaldar el cumplimiento de la especificacion pedida
- exponer en el reporte una vista resumida de la transformacion obtenida

No se usa como indice FM completo ni para compresion; aqui funciona como una
transformacion asociada al arreglo de sufijos.

## Deteccion de coincidencias

### Comparador 1: diff

La estrategia `diff` usa `difflib.SequenceMatcher`.

El procedimiento es:

1. Preparar las secuencias en `plain_text` o `preprocessed`.
2. Ejecutar `SequenceMatcher` sobre las unidades normalizadas.
3. Tomar los bloques devueltos por `get_matching_blocks()`.
4. Filtrar los que no alcancen `MIN_MATCH_LINES`.
5. Reconstruir el fragmento visible con `display_units`.
6. Generar el diff del bloque con `difflib.unified_diff`.

Esta variante deja muy clara la solucion basada en herramientas tipo diff.

### Comparador 2: suffix array/BWT

La parte central esta en `_extract_matches_from_suffix_array()`.

El procedimiento es:

1. Construir secuencia combinada.
2. Construir `suffix array`, `LCP` y `BWT`.
3. Recorrer pares adyacentes de sufijos en el `suffix array`.
4. Identificar de que programa viene cada sufijo con `_origin_for_index()`.
5. Ignorar pares donde ambos sufijos pertenecen al mismo programa.
6. Tomar la longitud comun usando:
   - el valor `LCP`
   - `_common_prefix_length()` para cortar al llegar a un centinela
7. Si la longitud comun es al menos `MIN_MATCH_LINES`, registrar un `MatchSection`.

### Por que solo sufijos adyacentes

Cuando dos sufijos comparten un prefijo largo, al ordenar todos los sufijos
lexicograficamente esos sufijos quedan cerca entre si. Por eso revisar
adyacencias en el `suffix array` es suficiente para encontrar candidatos
fuertes.

### Posiciones reportadas

Cada match guarda:

- `start_a`, `end_a`
- `start_b`, `end_b`
- `length`

Estas posiciones no son offsets de caracteres; son indices de unidades
comparadas:

- en `plain_text`, una unidad es una linea real
- en `preprocessed`, una unidad es una linea logica normalizada

## Reconstruccion del fragmento visible

Una vez encontrada una coincidencia, el reporte no imprime la secuencia
normalizada, sino el codigo original.

Para eso, `_extract_matches_from_suffix_array()` arma:

- `lines_a`
- `lines_b`

uniendo los bloques de `display_units` asociados a cada unidad coincidente.

Eso permite que en el reporte aparezca:

- la indentacion real
- los nombres reales de variables
- los literales reales
- el codigo fuente legible

incluso cuando la deteccion se hizo sobre la version preprocesada.

## Filtrado de coincidencias contenidas

La funcion `_filter_maximal_matches()` elimina coincidencias redundantes.

La idea es conservar coincidencias maximas y descartar bloques totalmente
contenidos dentro de otro bloque mayor con el mismo alineamiento relativo.

Sin este filtrado, el reporte tenderia a llenarse de subbloques triviales.

## Diff del bloque

La funcion `_build_diff()` usa:

```python
difflib.unified_diff(...)
```

para construir un diff de texto entre los dos fragmentos originales del match.

Este diff no se usa para detectar similitud; se usa solo para explicar
visualmente que cambio dentro de un bloque ya detectado como similar.

## Medida de similitud

La funcion `_similarity_percentage()` calcula el porcentaje final.

El criterio usado es cobertura de unidades coincidentes:

1. Reune todas las posiciones cubiertas por los matches en A.
2. Reune todas las posiciones cubiertas por los matches en B.
3. Toma el minimo de ambas coberturas como `matched_units`.
4. Divide entre la longitud del programa mas corto.

Formula:

```text
similitud = (matched_units / min(total_units_a, total_units_b)) * 100
```

Esto evita sobrecontar tramos repetidos cuando existen varios matches que se
solapan.

## Reporte individual

`generate_report.py` hace lo siguiente:

1. Ejecuta el comparador `diff` en modo `plain_text`.
2. Ejecuta el comparador `diff` en modo `preprocessed`.
3. Ejecuta el comparador `suffix_array` en modo `plain_text`.
4. Ejecuta el comparador `suffix_array` en modo `preprocessed`.
5. Genera un Markdown con:
   - descripcion conceptual
   - resultados de ambos comparadores
   - detalles del algoritmo de cada uno
   - tamano del suffix array cuando aplica
   - vista corta de BWT cuando aplica
   - porcentaje de similitud
   - secciones encontradas
   - diff de cada bloque

## Comparacion por lote

`batch_compare.py` toma todos los `.py` de un directorio y compara todos los
pares posibles.

Flujo:

1. Lee la carpeta del dataset.
2. Genera combinaciones de archivos de dos en dos.
3. Ejecuta `compare_programs()` en ambos modos para cada par usando la
   estrategia elegida.
4. Ordena resultados por similitud preprocesada.
5. Escribe `reporte_dataset.md`.

## Decisiones de diseno

Estas son las decisiones importantes de esta implementacion:

- comparar por unidades lineales en lugar de caracteres
- ofrecer una variante literal y una estructural
- separar representacion para comparar y representacion para mostrar
- usar centinelas para no mezclar ambos programas en una coincidencia
- filtrar matches internos para que el reporte sea manejable

## Limitaciones actuales

- `build_suffix_array()` usa ordenamiento directo de sufijos, lo cual es
  correcto pero no es la variante mas eficiente para entradas muy grandes
- la comparacion sigue siendo line-based, no semantic-based
- no hay parser de AST ni analisis de control de flujo
- en modo preprocesado los comentarios y lineas vacias no participan en la
  deteccion
- la BWT se construye y se reporta, pero no se explota como indice avanzado

## Resumen

Internamente, este comparador funciona transformando dos programas Python en
secuencias comparables, construyendo un `suffix array` sobre ambas a la vez y
usando `LCP` para detectar prefijos comunes largos entre sufijos de distintos
programas. Luego reconstruye el codigo original para mostrar los fragmentos
con indentacion real y calcula un porcentaje de similitud basado en cobertura
de bloques comunes.
