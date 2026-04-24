# Justificacion de decisiones del proyecto

Este documento resume y justifica las decisiones tecnicas principales tomadas
en el proyecto `comparador_codigo_python`, en su enfoque actual de la rama
`main`.

## 1. Eleccion del enfoque principal

La decision central del proyecto fue usar un comparador cuya deteccion de
similitud se basa en:

- `suffix array`
- `LCP` (`Longest Common Prefix`)
- `BWT` (`Burrows-Wheeler Transform`)

La justificacion de esta decision es doble:

1. responde directamente a la idea academica de buscar subcadenas comunes por
   medio de estructuras de sufijos
2. se alinea con la inspiracion del articulo de Brenda S. Baker, donde la
   deteccion de duplicacion se modela como un problema de comparacion de
   secuencias

En esta rama no se uso `difflib` como algoritmo principal de deteccion,
porque se privilegio un enfoque estructurado sobre sufijos para que la parte
algoritmica del proyecto quedara claramente diferenciada de un comparador
basado en diff.

## 2. Uso de `difflib` solo como apoyo visual

Aunque el algoritmo principal no depende de `difflib` para encontrar
similitud, si se decidio usar `difflib.unified_diff` para mostrar las
diferencias entre bloques ya detectados.

Esto se hizo por tres razones:

1. mejora la interpretabilidad del reporte
2. permite ver cambios concretos entre dos fragmentos similares
3. evita mezclar la deteccion principal con la visualizacion del resultado

La idea fue separar claramente:

- deteccion: `suffix array + LCP + BWT`
- presentacion: `difflib.unified_diff`

## 3. Dos modos de comparacion: `plain_text` y `preprocessed`

Se decidio ofrecer dos modos de comparacion:

- `plain_text`
- `preprocessed`

Esto responde a una necesidad academica y practica.

### `plain_text`

El modo `plain_text` conserva el codigo casi tal como aparece en el archivo.
Se eliminan lineas vacias y comentarios triviales, pero la comparacion sigue
siendo esencialmente literal.

Se eligio este modo porque:

- permite detectar copia casi exacta
- sirve como linea base
- hace visible cuanto depende la similitud del texto literal

### `preprocessed`

El modo `preprocessed` normaliza el codigo reemplazando:

- identificadores por `ID`
- numeros por `NUM`
- cadenas por `STR`

Se eligio este modo porque replica la intuicion del enfoque de Baker:
programas parecidos pueden seguir siendo estructuralmente equivalentes aunque
cambien nombres, constantes o literales.

Esta decision permite que el proyecto detecte:

- similitud textual
- similitud estructural

y no solamente copia exacta.

## 4. Comparacion por unidades lineales en lugar de caracteres

El comparador trabaja sobre secuencias de unidades lineales, no sobre el flujo
crudo de caracteres.

En `plain_text`, una unidad es una linea real.
En `preprocessed`, una unidad es una linea logica normalizada.

Esta decision se tomo porque:

1. simplifica el modelo de comparacion
2. hace mas legibles las coincidencias reportadas
3. conecta mejor con la idea de duplicacion de bloques de codigo
4. reduce el ruido que produciria una comparacion a nivel de caracteres

El costo de esta decision es que no se detectan microvariaciones internas a
nivel de caracteres como unidad principal de coincidencia, pero para la tarea
esa perdida es razonable.

## 5. Tokenizacion con `tokenize` de Python

Para el modo `preprocessed` se eligio usar el modulo estandar `tokenize`.

La justificacion es:

- ya entiende la estructura lexical basica de Python
- evita construir un preprocesador manual propenso a errores
- permite distinguir nombres, numeros, strings y operadores con precision

Tambien reduce la complejidad de mantenimiento, porque el proyecto reutiliza
una herramienta oficial del propio lenguaje.

## 6. Separacion entre representacion para comparar y representacion para mostrar

Se introdujo la estructura `PreparedSequence` con:

- `normalized_units`
- `display_units`

Esta decision fue importante porque el algoritmo necesita una forma
normalizada para comparar, pero el usuario necesita ver el codigo original con
indentacion real en el reporte.

Sin esta separacion, habia dos problemas posibles:

1. o se comparaba codigo muy ruidoso
2. o el reporte mostraba una version artificial poco legible

La decision entonces fue:

- comparar sobre una abstraccion
- reportar sobre el codigo real

Esto mejora la utilidad del resultado sin sacrificar claridad algoritmica.

## 7. Codificacion a enteros

Antes de construir el `suffix array`, cada unidad se transforma a un entero.

Esto se hizo porque:

- facilita trabajar con una secuencia discreta
- simplifica la construccion del `suffix array`, del `LCP` y de la `BWT`
- evita comparar cadenas largas repetidamente

La codificacion preserva igualdad estructural entre unidades y hace mas claro
el paso de texto a estructura comparable.

## 8. Uso de centinelas para separar ambos programas

Se definieron dos centinelas:

- `SENTINEL_A = 0`
- `SENTINEL_B = 1`

La secuencia combinada se construye como:

```text
programa_A + [SENTINEL_A] + programa_B + [SENTINEL_B]
```

La justificacion de esta decision es evitar coincidencias artificiales que
crucen de un programa al otro. Sin separadores especiales, una coincidencia
podria extenderse mas alla del limite real de uno de los programas.

## 9. Filtrado de coincidencias maximas

El algoritmo encuentra candidatos a coincidencia a partir de sufijos
adyacentes, pero despues aplica un filtrado para eliminar matches contenidos
dentro de otros mayores.

Se tomo esta decision porque, sin ese filtrado:

- el reporte se llenaria de fragmentos redundantes
- aumentaria el ruido de interpretacion
- la metrica podria verse afectada por sobreconteo conceptual

La meta fue priorizar bloques mas representativos y utiles.

## 10. Medida de similitud por cobertura

La similitud se calcula con base en cobertura de unidades comunes, no con la
suma bruta de todas las longitudes encontradas.

La formula implementada es:

```text
similitud = (matched_units / min(total_units_a, total_units_b)) * 100
```

donde `matched_units` se obtiene como la cobertura comun efectiva de las
unidades encontradas.

Esta decision se tomo para evitar:

- sobrecontar bloques solapados
- inflar artificialmente la similitud
- depender de la cantidad de matches redundantes

En otras palabras, la metrica intenta medir cuanto del programa mas corto esta
cubierto por secciones comunes reales.

## 11. Reportes en Markdown

Se eligio generar salidas en Markdown porque:

- son faciles de leer
- se pueden abrir en cualquier editor
- permiten mezclar explicacion, codigo y diff en un solo documento
- son apropiadas para entrega academica

El reporte muestra:

- porcentaje de similitud
- bloques similares
- fragmentos originales
- diff del bloque
- datos del algoritmo como suffix array y BWT

Esto convierte la salida en un artefacto justificable, no solo en una cifra.

## 12. Comparacion por pares y por dataset

El proyecto incluye dos niveles de uso:

- comparacion de dos programas concretos
- comparacion masiva de un dataset

Se decidio incluir ambos porque responden a necesidades distintas:

- el analisis por pares sirve para explicar y defender el comportamiento
- el analisis por dataset sirve para evaluar el enfoque en varios casos

La combinacion de ambas vistas ayuda a validar mejor el proyecto.

## 13. Mantener el proyecto sin dependencias externas adicionales

Se decidio que este subproyecto usara solo biblioteca estandar de Python.

La justificacion fue:

- facilitar ejecucion en cualquier entorno
- reducir friccion de instalacion
- hacer la entrega mas portable

La unica dependencia externa del repositorio completo sigue siendo `ply`, pero
eso corresponde al proyecto del analizador lexico de C, no al comparador de
Python.

## 14. Alcance y limitaciones aceptadas

Se aceptaron conscientemente estas limitaciones:

- el comparador es line-based, no semantic-based
- no hay analisis de AST ni equivalencia semantica
- `build_suffix_array()` usa ordenamiento directo, correcto pero no optimo
- la `BWT` se construye y se reporta, pero no se usa como indice FM completo

Estas limitaciones se aceptaron porque el objetivo del proyecto no era crear
un detector industrial de plagio o equivalencia semantica, sino implementar y
justificar un comparador coherente con la consigna, entendible y demostrable.

## 15. Decision de documentar la rama alternativa

Finalmente, se decidio documentar en el README que existe una rama alternativa
llamada `separated-comparision`, donde el enfoque se presenta como dos
comparadores separados:

- uno basado en diff
- otro basado en suffix array/BWT

La justificacion de esa decision fue dejar constancia de una interpretacion
alternativa de la consigna, sin mezclarla con el enfoque principal de `main`.

## Conclusion

Las decisiones del proyecto buscaron equilibrio entre:

- claridad academica
- trazabilidad de resultados
- simplicidad de ejecucion
- alineacion con la consigna

El resultado es un comparador que privilegia una deteccion estructurada sobre
secuencias de codigo, con soporte para comparacion literal y preprocesada, y
con reportes que permiten justificar visualmente el porcentaje de similitud
obtenido.
