# Reporte de similitud entre programas Python

## Base conceptual
La solucion se presenta como dos comparadores separados, para cubrir de forma explicita la consigna: un comparador basado en diff y un comparador basado en suffix array/BWT. Cada uno se ejecuta en texto llano y en texto preprocesado.

## Archivos comparados
- Programa A: `programa_a.py`
- Programa B: `programa_b.py`

## Medida de similitud propuesta
Se usa la cobertura total de las subcadenas comunes detectadas, dividida entre la longitud del programa mas corto.

```text
similitud = (matched_units / longitud_programa_mas_corto) * 100
```

## Resumen comparativo
- diff / plain_text: 6.52% de similitud, 3 unidades comunes, 1 secciones.
- diff / preprocessed: 100.00% de similitud, 37 unidades comunes, 1 secciones.
- suffix_array / plain_text: 6.52% de similitud, 3 unidades comunes, 1 secciones.
- suffix_array / preprocessed: 100.00% de similitud, 37 unidades comunes, 1 secciones.

## Comparador 1: Diff en texto llano
- Estrategia: `diff`
- Modo: `plain_text`
- Algoritmo: `difflib.SequenceMatcher + difflib.unified_diff`
- Similitud: 6.52%
- Unidades comunes: 3
- Secciones detectadas: 1

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

## Comparador 1: Diff en texto preprocesado
- Estrategia: `diff`
- Modo: `preprocessed`
- Algoritmo: `difflib.SequenceMatcher + difflib.unified_diff`
- Similitud: 100.00%
- Unidades comunes: 37
- Secciones detectadas: 1

### Seccion 1: A[1-37] y B[1-37] (37 lineas/unidades)

**Fragmento en programa_a.py**

```python
def calcular_descuento(total, nivel_cliente):
    if nivel_cliente == "oro":
        descuento = total * 0.15
    elif nivel_cliente == "plata":
        descuento = total * 0.10
    else:
        descuento = total * 0.03
    return round(descuento, 2)
def calcular_impuesto_base(monto):
    impuesto = monto * 0.16
    return round(impuesto, 2)
def construir_resumen_ventas(registros):
    ventas_validas = []
    for fila in registros:
        if fila["estado"] != "cancelada":
            ventas_validas.append(fila)
    subtotal = 0
    impuestos = 0
    for venta in ventas_validas:
        subtotal += venta["monto"]
        impuestos += calcular_impuesto_base(venta["monto"])
    total_descuentos = 0
    for venta in ventas_validas:
        total_descuentos += calcular_descuento(venta["monto"], venta["cliente"])
    return {
        "subtotal": round(subtotal, 2),
        "impuestos": round(impuestos, 2),
        "descuentos": round(total_descuentos, 2),
        "total": round(subtotal + impuestos - total_descuentos, 2),
    }
def formatear_reporte(registros):
    resumen = construir_resumen_ventas(registros)
    lineas = []
    lineas.append("REPORTE DE VENTAS")
    lineas.append(f"Subtotal: {resumen['subtotal']}")
    lineas.append(f"Impuestos: {resumen['impuestos']}")
    lineas.append(f"Descuentos: {resumen['descuentos']}")
    lineas.append(f"Total final: {resumen['total']}")
    return "\n".join(lineas)
if __name__ == "__main__":
    datos = [
        {"monto": 120.0, "cliente": "oro", "estado": "pagada"},
        {"monto": 80.0, "cliente": "plata", "estado": "pagada"},
        {"monto": 30.0, "cliente": "bronce", "estado": "cancelada"},
    ]
    print(formatear_reporte(datos))
```

**Fragmento en programa_b.py**

```python
def obtener_bonificacion(cantidad, categoria_usuario):
    if categoria_usuario == "premium":
        rebaja = cantidad * 0.15
    elif categoria_usuario == "frecuente":
        rebaja = cantidad * 0.10
    else:
        rebaja = cantidad * 0.03
    return round(rebaja, 2)
def calcular_impuesto_base(monto):
    impuesto = monto * 0.16
    return round(impuesto, 2)
def construir_resumen_pedidos(entradas):
    pedidos_confirmados = []
    for elemento in entradas:
        if elemento["estado"] != "rechazada":
            pedidos_confirmados.append(elemento)
    acumulado = 0
    iva = 0
    for pedido in pedidos_confirmados:
        acumulado += pedido["monto"]
        iva += calcular_impuesto_base(pedido["monto"])
    bonificaciones = 0
    for pedido in pedidos_confirmados:
        bonificaciones += obtener_bonificacion(pedido["monto"], pedido["cliente"])
    return {
        "subtotal": round(acumulado, 2),
        "impuestos": round(iva, 2),
        "descuentos": round(bonificaciones, 2),
        "total": round(acumulado + iva - bonificaciones, 2),
    }
def crear_salida(entradas):
    reporte = construir_resumen_pedidos(entradas)
    texto = []
    texto.append("RESUMEN DE PEDIDOS")
    texto.append(f"Subtotal: {reporte['subtotal']}")
    texto.append(f"Impuestos: {reporte['impuestos']}")
    texto.append(f"Descuentos: {reporte['descuentos']}")
    texto.append(f"Total final: {reporte['total']}")
    return "\n".join(texto)
if __name__ == "__main__":
    muestras = [
        {"monto": 120.0, "cliente": "premium", "estado": "aceptada"},
        {"monto": 80.0, "cliente": "frecuente", "estado": "aceptada"},
        {"monto": 30.0, "cliente": "ocasional", "estado": "rechazada"},
    ]
    print(crear_salida(muestras))
```

**Diff del bloque**

```diff
--- programa_a.py
+++ programa_b.py
@@ -1,46 +1,46 @@
-def calcular_descuento(total, nivel_cliente):
-    if nivel_cliente == "oro":
-        descuento = total * 0.15
-    elif nivel_cliente == "plata":
-        descuento = total * 0.10
+def obtener_bonificacion(cantidad, categoria_usuario):
+    if categoria_usuario == "premium":
+        rebaja = cantidad * 0.15
+    elif categoria_usuario == "frecuente":
+        rebaja = cantidad * 0.10
     else:
-        descuento = total * 0.03
-    return round(descuento, 2)
+        rebaja = cantidad * 0.03
+    return round(rebaja, 2)
 def calcular_impuesto_base(monto):
     impuesto = monto * 0.16
     return round(impuesto, 2)
-def construir_resumen_ventas(registros):
-    ventas_validas = []
-    for fila in registros:
-        if fila["estado"] != "cancelada":
-            ventas_validas.append(fila)
-    subtotal = 0
-    impuestos = 0
-    for venta in ventas_validas:
-        subtotal += venta["monto"]
-        impuestos += calcular_impuesto_base(venta["monto"])
-    total_descuentos = 0
-    for venta in ventas_validas:
-        total_descuentos += calcular_descuento(venta["monto"], venta["cliente"])
+def construir_resumen_pedidos(entradas):
+    pedidos_confirmados = []
+    for elemento in entradas:
+        if elemento["estado"] != "rechazada":
+            pedidos_confirmados.append(elemento)
+    acumulado = 0
+    iva = 0
+    for pedido in pedidos_confirmados:
+        acumulado += pedido["monto"]
+        iva += calcular_impuesto_base(pedido["monto"])
+    bonificaciones = 0
+    for pedido in pedidos_confirmados:
+        bonificaciones += obtener_bonificacion(pedido["monto"], pedido["cliente"])
     return {
-        "subtotal": round(subtotal, 2),
-        "impuestos": round(impuestos, 2),
-        "descuentos": round(total_descuentos, 2),
-        "total": round(subtotal + impuestos - total_descuentos, 2),
+        "subtotal": round(acumulado, 2),
+        "impuestos": round(iva, 2),
+        "descuentos": round(bonificaciones, 2),
+        "total": round(acumulado + iva - bonificaciones, 2),
     }
-def formatear_reporte(registros):
-    resumen = construir_resumen_ventas(registros)
-    lineas = []
-    lineas.append("REPORTE DE VENTAS")
-    lineas.append(f"Subtotal: {resumen['subtotal']}")
-    lineas.append(f"Impuestos: {resumen['impuestos']}")
-    lineas.append(f"Descuentos: {resumen['descuentos']}")
-    lineas.append(f"Total final: {resumen['total']}")
-    return "\n".join(lineas)
+def crear_salida(entradas):
+    reporte = construir_resumen_pedidos(entradas)
+    texto = []
+    texto.append("RESUMEN DE PEDIDOS")
+    texto.append(f"Subtotal: {reporte['subtotal']}")
+    texto.append(f"Impuestos: {reporte['impuestos']}")
+    texto.append(f"Descuentos: {reporte['descuentos']}")
+    texto.append(f"Total final: {reporte['total']}")
+    return "\n".join(texto)
 if __name__ == "__main__":
-    datos = [
-        {"monto": 120.0, "cliente": "oro", "estado": "pagada"},
-        {"monto": 80.0, "cliente": "plata", "estado": "pagada"},
-        {"monto": 30.0, "cliente": "bronce", "estado": "cancelada"},
+    muestras = [
+        {"monto": 120.0, "cliente": "premium", "estado": "aceptada"},
+        {"monto": 80.0, "cliente": "frecuente", "estado": "aceptada"},
+        {"monto": 30.0, "cliente": "ocasional", "estado": "rechazada"},
     ]
-    print(formatear_reporte(datos))
+    print(crear_salida(muestras))
```

## Comparador 2: Suffix Array/BWT en texto llano
- Estrategia: `suffix_array`
- Modo: `plain_text`
- Algoritmo: `suffix_array + lcp + bwt + difflib.unified_diff`
- Similitud: 6.52%
- Unidades comunes: 3
- Secciones detectadas: 1
- Tamano suffix array: 94
- Vista BWT: `[46, 83, 1, 2, 3, 4, 5, 6, 51, 7, 8, 9, 53, 10, 10, 11, 11, 12, 13, 14]`

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

## Comparador 2: Suffix Array/BWT en texto preprocesado
- Estrategia: `suffix_array`
- Modo: `preprocessed`
- Algoritmo: `suffix_array + lcp + bwt + difflib.unified_diff`
- Similitud: 100.00%
- Unidades comunes: 37
- Secciones detectadas: 1
- Tamano suffix array: 76
- Vista BWT: `[26, 26, 1, 0, 2, 2, 24, 24, 3, 3, 5, 5, 6, 6, 8, 8, 4, 4, 4, 4]`

### Seccion 1: A[1-37] y B[1-37] (37 lineas/unidades)

**Fragmento en programa_a.py**

```python
def calcular_descuento(total, nivel_cliente):
    if nivel_cliente == "oro":
        descuento = total * 0.15
    elif nivel_cliente == "plata":
        descuento = total * 0.10
    else:
        descuento = total * 0.03
    return round(descuento, 2)
def calcular_impuesto_base(monto):
    impuesto = monto * 0.16
    return round(impuesto, 2)
def construir_resumen_ventas(registros):
    ventas_validas = []
    for fila in registros:
        if fila["estado"] != "cancelada":
            ventas_validas.append(fila)
    subtotal = 0
    impuestos = 0
    for venta in ventas_validas:
        subtotal += venta["monto"]
        impuestos += calcular_impuesto_base(venta["monto"])
    total_descuentos = 0
    for venta in ventas_validas:
        total_descuentos += calcular_descuento(venta["monto"], venta["cliente"])
    return {
        "subtotal": round(subtotal, 2),
        "impuestos": round(impuestos, 2),
        "descuentos": round(total_descuentos, 2),
        "total": round(subtotal + impuestos - total_descuentos, 2),
    }
def formatear_reporte(registros):
    resumen = construir_resumen_ventas(registros)
    lineas = []
    lineas.append("REPORTE DE VENTAS")
    lineas.append(f"Subtotal: {resumen['subtotal']}")
    lineas.append(f"Impuestos: {resumen['impuestos']}")
    lineas.append(f"Descuentos: {resumen['descuentos']}")
    lineas.append(f"Total final: {resumen['total']}")
    return "\n".join(lineas)
if __name__ == "__main__":
    datos = [
        {"monto": 120.0, "cliente": "oro", "estado": "pagada"},
        {"monto": 80.0, "cliente": "plata", "estado": "pagada"},
        {"monto": 30.0, "cliente": "bronce", "estado": "cancelada"},
    ]
    print(formatear_reporte(datos))
```

**Fragmento en programa_b.py**

```python
def obtener_bonificacion(cantidad, categoria_usuario):
    if categoria_usuario == "premium":
        rebaja = cantidad * 0.15
    elif categoria_usuario == "frecuente":
        rebaja = cantidad * 0.10
    else:
        rebaja = cantidad * 0.03
    return round(rebaja, 2)
def calcular_impuesto_base(monto):
    impuesto = monto * 0.16
    return round(impuesto, 2)
def construir_resumen_pedidos(entradas):
    pedidos_confirmados = []
    for elemento in entradas:
        if elemento["estado"] != "rechazada":
            pedidos_confirmados.append(elemento)
    acumulado = 0
    iva = 0
    for pedido in pedidos_confirmados:
        acumulado += pedido["monto"]
        iva += calcular_impuesto_base(pedido["monto"])
    bonificaciones = 0
    for pedido in pedidos_confirmados:
        bonificaciones += obtener_bonificacion(pedido["monto"], pedido["cliente"])
    return {
        "subtotal": round(acumulado, 2),
        "impuestos": round(iva, 2),
        "descuentos": round(bonificaciones, 2),
        "total": round(acumulado + iva - bonificaciones, 2),
    }
def crear_salida(entradas):
    reporte = construir_resumen_pedidos(entradas)
    texto = []
    texto.append("RESUMEN DE PEDIDOS")
    texto.append(f"Subtotal: {reporte['subtotal']}")
    texto.append(f"Impuestos: {reporte['impuestos']}")
    texto.append(f"Descuentos: {reporte['descuentos']}")
    texto.append(f"Total final: {reporte['total']}")
    return "\n".join(texto)
if __name__ == "__main__":
    muestras = [
        {"monto": 120.0, "cliente": "premium", "estado": "aceptada"},
        {"monto": 80.0, "cliente": "frecuente", "estado": "aceptada"},
        {"monto": 30.0, "cliente": "ocasional", "estado": "rechazada"},
    ]
    print(crear_salida(muestras))
```

**Diff del bloque**

```diff
--- programa_a.py
+++ programa_b.py
@@ -1,46 +1,46 @@
-def calcular_descuento(total, nivel_cliente):
-    if nivel_cliente == "oro":
-        descuento = total * 0.15
-    elif nivel_cliente == "plata":
-        descuento = total * 0.10
+def obtener_bonificacion(cantidad, categoria_usuario):
+    if categoria_usuario == "premium":
+        rebaja = cantidad * 0.15
+    elif categoria_usuario == "frecuente":
+        rebaja = cantidad * 0.10
     else:
-        descuento = total * 0.03
-    return round(descuento, 2)
+        rebaja = cantidad * 0.03
+    return round(rebaja, 2)
 def calcular_impuesto_base(monto):
     impuesto = monto * 0.16
     return round(impuesto, 2)
-def construir_resumen_ventas(registros):
-    ventas_validas = []
-    for fila in registros:
-        if fila["estado"] != "cancelada":
-            ventas_validas.append(fila)
-    subtotal = 0
-    impuestos = 0
-    for venta in ventas_validas:
-        subtotal += venta["monto"]
-        impuestos += calcular_impuesto_base(venta["monto"])
-    total_descuentos = 0
-    for venta in ventas_validas:
-        total_descuentos += calcular_descuento(venta["monto"], venta["cliente"])
+def construir_resumen_pedidos(entradas):
+    pedidos_confirmados = []
+    for elemento in entradas:
+        if elemento["estado"] != "rechazada":
+            pedidos_confirmados.append(elemento)
+    acumulado = 0
+    iva = 0
+    for pedido in pedidos_confirmados:
+        acumulado += pedido["monto"]
+        iva += calcular_impuesto_base(pedido["monto"])
+    bonificaciones = 0
+    for pedido in pedidos_confirmados:
+        bonificaciones += obtener_bonificacion(pedido["monto"], pedido["cliente"])
     return {
-        "subtotal": round(subtotal, 2),
-        "impuestos": round(impuestos, 2),
-        "descuentos": round(total_descuentos, 2),
-        "total": round(subtotal + impuestos - total_descuentos, 2),
+        "subtotal": round(acumulado, 2),
+        "impuestos": round(iva, 2),
+        "descuentos": round(bonificaciones, 2),
+        "total": round(acumulado + iva - bonificaciones, 2),
     }
-def formatear_reporte(registros):
-    resumen = construir_resumen_ventas(registros)
-    lineas = []
-    lineas.append("REPORTE DE VENTAS")
-    lineas.append(f"Subtotal: {resumen['subtotal']}")
-    lineas.append(f"Impuestos: {resumen['impuestos']}")
-    lineas.append(f"Descuentos: {resumen['descuentos']}")
-    lineas.append(f"Total final: {resumen['total']}")
-    return "\n".join(lineas)
+def crear_salida(entradas):
+    reporte = construir_resumen_pedidos(entradas)
+    texto = []
+    texto.append("RESUMEN DE PEDIDOS")
+    texto.append(f"Subtotal: {reporte['subtotal']}")
+    texto.append(f"Impuestos: {reporte['impuestos']}")
+    texto.append(f"Descuentos: {reporte['descuentos']}")
+    texto.append(f"Total final: {reporte['total']}")
+    return "\n".join(texto)
 if __name__ == "__main__":
-    datos = [
-        {"monto": 120.0, "cliente": "oro", "estado": "pagada"},
-        {"monto": 80.0, "cliente": "plata", "estado": "pagada"},
-        {"monto": 30.0, "cliente": "bronce", "estado": "cancelada"},
+    muestras = [
+        {"monto": 120.0, "cliente": "premium", "estado": "aceptada"},
+        {"monto": 80.0, "cliente": "frecuente", "estado": "aceptada"},
+        {"monto": 30.0, "cliente": "ocasional", "estado": "rechazada"},
     ]
-    print(formatear_reporte(datos))
+    print(crear_salida(muestras))
```

## Conclusiones
El comparador basado en diff ofrece una solucion directa apoyada en utilidades de comparacion de secuencias, mientras que el comparador basado en suffix array/BWT resuelve la busqueda desde una estructura clasica sobre sufijos. La variante preprocesada es la que mejor evidencia similitud estructural con renombrado.
