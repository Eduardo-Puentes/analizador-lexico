# Analizador Lexico: trabajos del repositorio

Este repositorio contiene varios trabajos relacionados con analisis de codigo.

## Dependencias

La unica dependencia externa declarada a nivel repositorio es:

```text
ply
```

Se instala desde la raiz con:

```bash
python3 -m pip install -r requirements.txt
```

El proyecto `comparador_codigo_python` no requiere paquetes adicionales fuera
de la biblioteca estandar de Python.

## Proyectos incluidos

### 1. Analizador lexico para C

Carpeta:

```text
clang-analizador-lexico/
```

Contenido:

- analizador lexico para un subconjunto de C usando `ply.lex`
- script principal del lexer
- casos de prueba
- justificacion del fragmento de lenguaje seleccionado

Lee el README de este proyecto para instrucciones de uso:

[README de clang-analizador-lexico](./clang-analizador-lexico/README.md)

### 2. Comparador de programas Python

Carpeta:

```text
comparador_codigo_python/
```

Contenido:

- comparador de similitud entre programas Python
- variante en texto llano
- variante preprocesada
- deteccion de subcadenas comunes con `suffix array`, `LCP` y `BWT`
- comparacion por pares y comparacion por dataset
- generacion de reportes en Markdown

Lee el README de este proyecto para instrucciones de uso y explicacion interna:

[README de comparador_codigo_python](./comparador_codigo_python/README.md)

## Nota

Cada proyecto tiene su propia documentacion dentro de su carpeta. Para ejecutar,
probar o entender el funcionamiento interno de un trabajo, consulta primero el
README correspondiente dentro de ese proyecto.
