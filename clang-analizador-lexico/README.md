# Clang Analizador Lexico

Este proyecto implementa un analizador lexico para un subconjunto de C usando
`ply.lex`.

## Requisitos

Crea un environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala la dependencia del proyecto:

```bash
python3 -m pip install -r ../requirements.txt
```

## Ejecutar el lexer

Con el ejemplo integrado:

```bash
python3 clang-lexer.py
```

Con un archivo de entrada:

```bash
python3 clang-lexer.py tests/inputs/valid-basic.c
```

## Ejecutar los tests

```bash
python3 tests/run_lexer_tests.py
```

## Archivos importantes

- `clang-lexer.py`: implementacion principal del lexer
- `tests/run_lexer_tests.py`: script de pruebas
- `tests/inputs/`: archivos de entrada para pruebas
- `justificacion-fragmento-c.md`: justificacion formal del fragmento de C seleccionado

## Nota

La justificacion formal del fragmento seleccionado se encuentra en:

`justificacion-fragmento-c.md`

