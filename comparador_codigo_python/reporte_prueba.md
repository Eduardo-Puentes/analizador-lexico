# Reporte de similitud entre programas Python

## Base conceptual
La solucion retoma dos ideas centrales del articulo `A Program for Identifying Duplicated Code`: comparar por secuencias lineales y, en una segunda variante, aplicar un preprocesamiento que permita detectar coincidencias estructurales aunque cambien nombres de variables o literales.

## Archivos comparados
- Programa A: `programa_a.py`
- Programa B: `programa_b.py`

## Medida de similitud propuesta
Se usa la suma de las longitudes de las subcadenas comunes reportadas por `difflib.SequenceMatcher`, dividida entre la longitud del programa mas corto. La formula es:

```text
similitud = (suma_longitudes_subcadenas_comunes / longitud_programa_mas_corto) * 100
```

## Resumen cuantitativo
- Texto llano: 6.52% de similitud, 3 lineas/unidades comunes, 1 secciones detectadas.
- Texto preprocesado: 100.00% de similitud, 37 lineas/unidades comunes, 1 secciones detectadas.

## Coincidencias encontradas: Texto llano
### Seccion 1: A[9-11] y B[9-11] (3 lineas/unidades)

**Fragmento en programa_a.py**

```python
def calcular_impuesto_base(monto):
    impuesto = monto * 0.16
    return round(impuesto, 2)
```

**Fragmento en programa_b.py**

```python
def calcular_impuesto_base(monto):
    impuesto = monto * 0.16
    return round(impuesto, 2)
```

## Coincidencias encontradas: Texto preprocesado
### Seccion 1: A[1-37] y B[1-37] (37 lineas/unidades)

**Fragmento en programa_a.py**

```python
def ID ( ID , ID ) :
if ID == STR :
ID = ID * NUM
elif ID == STR :
ID = ID * NUM
else :
ID = ID * NUM
return ID ( ID , NUM )
def ID ( ID ) :
ID = ID * NUM
return ID ( ID , NUM )
def ID ( ID ) :
ID = [ ]
for ID in ID :
if ID [ STR ] != STR :
ID . ID ( ID )
ID = NUM
ID = NUM
for ID in ID :
ID += ID [ STR ]
ID += ID ( ID [ STR ] )
ID = NUM
for ID in ID :
ID += ID ( ID [ STR ] , ID [ STR ] )
return { STR : ID ( ID , NUM ) , STR : ID ( ID , NUM ) , STR : ID ( ID , NUM ) , STR : ID ( ID + ID - ID , NUM ) , }
def ID ( ID ) :
ID = ID ( ID )
ID = [ ]
ID . ID ( STR )
ID . ID ( f" Subtotal:  { ID [ STR ] } " )
ID . ID ( f" Impuestos:  { ID [ STR ] } " )
ID . ID ( f" Descuentos:  { ID [ STR ] } " )
ID . ID ( f" Total final:  { ID [ STR ] } " )
return STR . ID ( ID )
if ID == STR :
ID = [ { STR : NUM , STR : STR , STR : STR } , { STR : NUM , STR : STR , STR : STR } , { STR : NUM , STR : STR , STR : STR } , ]
ID ( ID ( ID ) )
```

**Fragmento en programa_b.py**

```python
def ID ( ID , ID ) :
if ID == STR :
ID = ID * NUM
elif ID == STR :
ID = ID * NUM
else :
ID = ID * NUM
return ID ( ID , NUM )
def ID ( ID ) :
ID = ID * NUM
return ID ( ID , NUM )
def ID ( ID ) :
ID = [ ]
for ID in ID :
if ID [ STR ] != STR :
ID . ID ( ID )
ID = NUM
ID = NUM
for ID in ID :
ID += ID [ STR ]
ID += ID ( ID [ STR ] )
ID = NUM
for ID in ID :
ID += ID ( ID [ STR ] , ID [ STR ] )
return { STR : ID ( ID , NUM ) , STR : ID ( ID , NUM ) , STR : ID ( ID , NUM ) , STR : ID ( ID + ID - ID , NUM ) , }
def ID ( ID ) :
ID = ID ( ID )
ID = [ ]
ID . ID ( STR )
ID . ID ( f" Subtotal:  { ID [ STR ] } " )
ID . ID ( f" Impuestos:  { ID [ STR ] } " )
ID . ID ( f" Descuentos:  { ID [ STR ] } " )
ID . ID ( f" Total final:  { ID [ STR ] } " )
return STR . ID ( ID )
if ID == STR :
ID = [ { STR : NUM , STR : STR , STR : STR } , { STR : NUM , STR : STR , STR : STR } , { STR : NUM , STR : STR , STR : STR } , ]
ID ( ID ( ID ) )
```

## Conclusiones
La comparacion en texto llano solo detecta coincidencias literales, mientras que la comparacion preprocesada encuentra bloques con la misma estructura aun cuando cambian identificadores, constantes o cadenas. Esto replica la intuicion del articulo: el preprocesamiento permite revelar duplicacion con renombrado.
