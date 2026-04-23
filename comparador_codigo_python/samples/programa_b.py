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
