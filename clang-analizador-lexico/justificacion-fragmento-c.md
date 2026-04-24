# Justificación formal del fragmento seleccionado

## 1. Objetivo del trabajo

El objetivo de este proyecto es diseñar e implementar un analizador léxico para un fragmento del lenguaje C, tomando como referencia:

- las secciones 3.3 - 3.8 del texto de Aho, Sethi y Ullman;
- el estándar ISO/IEC 9899:1999 (C99).

La intención no es cubrir la totalidad de C99, sino construir un analizador léxico correcto, defendible y viable dentro del alcance de una práctica de clase.

## 2. Criterio de selección del fragmento

Se seleccionó un subconjunto de C99 orientado a programas imperativos pequeños, con declaraciones, expresiones, estructuras de control y manejo básico de literales.

## 3. Elementos incluidos

El fragmento implementado incluye las siguientes categorías léxicas:

### 3.1 Palabras reservadas

Se incluyen las reservadas:

- `if`
- `else`
- `while`
- `for`
- `return`
- `int`
- `float`
- `char`
- `void`
- `break`
- `continue`

Estas palabras permiten construir ejemplos con declaraciones, condicionales, ciclos y control básico de flujo.

### 3.2 Identificadores

Se aceptan identificadores con la forma:

- letra o guion bajo al inicio;
- letras, dígitos o guion bajo en las posiciones subsecuentes.

Esta decisión coincide con la estructura general de identificadores en C y permite distinguir claramente entre identificadores y palabras reservadas.

### 3.3 Literales

Se incluyeron:

- enteros decimales;
- flotantes decimales sencillos;
- literales de carácter;
- literales de cadena con escapes básicos.

Estas clases léxicas son suficientes para expresar constantes comunes en ejercicios de clase y permiten ilustrar patrones regulares con diferentes niveles de complejidad.

### 3.4 Operadores

Se incluyeron operadores:

- aritméticos: `+`, `-`, `*`, `/`, `%`;
- relacionales: `<`, `<=`, `>`, `>=`, `==`, `!=`;
- lógicos: `&&`, `||`, `!`;
- asignación: `=`;
- incremento y decremento: `++`, `--`.

Su inclusión es importante porque permite mostrar uno de los problemas clásicos del análisis léxico: la prioridad entre tokens de un carácter y tokens compuestos.

### 3.5 Delimitadores y puntuación

Se reconocen:

- `(`, `)`;
- `{`, `}`;
- `[`, `]`;
- `,`, `;`.

Esto cubre la estructura superficial de expresiones, bloques, listas de argumentos y declaraciones simples.

### 3.6 Espacios y comentarios

Se decidió ignorar:

- espacios en blanco;
- tabulaciones;
- saltos de línea;
- comentarios de línea `// ...`;
- comentarios de bloque `/* ... */`.

Aunque estos elementos no producen tokens útiles para el parser, sí deben ser tratados correctamente por el lexer para preservar la posición y evitar falsos errores léxicos.

## 4. Elementos excluidos

Se decidió dejar fuera las siguientes partes del lenguaje:

### 4.1 Preprocesador

No se incluyó el tratamiento completo de:

- `#include`
- `#define`
- macros
- expansión de macros
- directivas condicionales del preprocesador

La razón principal es que el preprocesador introduce una fase previa al análisis léxico tradicional y su manejo completo requiere una arquitectura más amplia que la de este ejercicio.

### 4.2 Variantes avanzadas de constantes

No se incorporó soporte amplio para:

- enteros octales y hexadecimales;
- sufijos `U`, `L`, `LL`;
- variantes extensas de notación exponencial;
- literales anchos y prefijados.

Estas construcciones existen en C99, pero su valor pedagógico en una primera entrega es menor que el costo adicional de implementación, validación y documentación.

### 4.3 Soporte completo de escapes y caracteres especiales

No se cubrieron en forma exhaustiva:

- nombres universales;
- combinaciones amplias de caracteres no ASCII;
- todas las variantes de secuencias de escape del estándar.

### 4.4 Digrafos, trigrafos y tokens alternativos

Tampoco se incluyeron:

- digrafos;
- trigrafos;
- operadores alternativos poco frecuentes.

## 5. Justificación técnica

La selección realizada es adecuada desde el punto de vista del análisis léxico por las siguientes razones:

1. Las clases léxicas incluidas pueden especificarse de forma clara mediante expresiones regulares.
2. Permiten discutir el paso conceptual de expresiones regulares a autómatas finitos, como se estudia en AHO.
3. Presentan conflictos clásicos de prioridad y coincidencia máxima, por ejemplo entre `=` y `==`, o entre `+` y `++`.
4. Obligan a contemplar manejo de errores léxicos, como literales mal formados o comentarios sin cerrar.
5. Permiten generar casos de prueba claros, tanto válidos como inválidos.

En consecuencia, el subconjunto elegido conserva los elementos más formativos del problema léxico sin introducir una complejidad desproporcionada.

## 6. Relación con AHO

La propuesta se apoya directamente en los temas tratados en las secciones 3.3 - 3.8:

- especificación de tokens por medio de expresiones regulares;
- prioridad entre reglas;
- distinción entre lexema y token;
- tratamiento de palabras reservadas e identificadores;
- detección y reporte de errores.

Por tanto, el trabajo implementado no sólo usa una herramienta práctica (`PLY`), sino que conserva el fundamento teórico.

## 7. Conclusión

El fragmento seleccionado es suficientemente amplio para analizar programas pequeños de C con declaraciones, expresiones y estructuras de control, y suficientemente acotado para implementarse con claridad dentro del tiempo y complejidad de una práctica de clase.

La exclusión de elementos más complejos del estándar no es una omisión arbitraria, sino una decisión metodológica orientada a privilegiar:

- corrección;
- claridad;
- justificabilidad teórica;
- facilidad de prueba.

Por ello, el resultado puede defenderse como un analizador léxico válido para un subconjunto representativo de C99.
