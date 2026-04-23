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
