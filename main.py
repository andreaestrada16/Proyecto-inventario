import pandas as pd
import os

productos = []
cantidad = []
precio_c = []
precio_v = []
fecha = []
lote = []
producto = []
cantidad_t = []

def cargar_datos():
    global productos, cantidad, precio_c, precio_v, fecha, lote, producto, cantidad_t
    if os.path.exists('Inventario.xlsx'):
        inventario = pd.read_excel('Inventario.xlsx', sheet_name='Sheet1')
        productos = inventario["PRODUCTOS"].values.tolist()
        cantidad = inventario["CANTIDAD"].values.tolist()
        precio_c = inventario["COSTO"].values.tolist()
        precio_v = inventario["PRECIO"].values.tolist()
        fecha = inventario["FECHA DE INGRESO"].values.tolist()
        lote = inventario["LOTE"].values.tolist()

        p_disponible = pd.read_excel('Inventario.xlsx', sheet_name='Sheet2')
        producto = p_disponible["Nombre de los productos"].values.tolist()
        cantidad_t = p_disponible["Cantidad total de los productos"].values.tolist()

def guardar_excel():
    inventario = pd.DataFrame({
        "PRODUCTOS": productos,
        "CANTIDAD": cantidad,
        "COSTO": precio_c,
        "PRECIO": precio_v,
        "FECHA DE INGRESO": fecha,
        "LOTE": lote
    })

    p_disponible = pd.DataFrame({
        "Nombre de los productos": producto,
        "Cantidad total de los productos": cantidad_t
    })

    with pd.ExcelWriter('Inventario.xlsx', engine='xlsxwriter') as writer:
        inventario.to_excel(writer, sheet_name='Sheet1', index=False)
        p_disponible.to_excel(writer, sheet_name='Sheet2', index=False)

def mostrar_inventario():
    if not productos:
        print("El inventario está vacío")
    else:
        df = pd.DataFrame({
            "ÍNDICE": list(range(len(productos))),
            "PRODUCTOS": productos,
            "CANTIDAD": cantidad,
            "COSTO": precio_c,
            "PRECIO": precio_v,
            "FECHA DE INGRESO": fecha,
            "LOTE": lote
        })
        print(df)

def recalcular_totales():
    global producto, cantidad_t
    resumen = {}

    for i in range(len(productos)):
        nombre = productos[i]
        cant = cantidad[i]

        if nombre in resumen:
            resumen[nombre] += cant
        else:
            resumen[nombre] = cant

    producto = list(resumen.keys())
    cantidad_t = list(resumen.values())

cargar_datos()

while True:
    print("\n\t.:MENÚ PRINCIPAL:.")
    print("1. Revisar Inventario")
    print("2. Compra de Unidades (Lotes)")
    print("3. Venta de Unidades")
    print("4. Añadir Productos")
    print("5. Editar datos")
    print("6. Eliminar registros")
    print("7. Salir del Programa")

    try:
        opcion = int(input("Ingrese el número de la acción a realizar: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        continue

    if opcion == 1:
        print("\n\t----REVISAR INVENTARIO----")
        mostrar_inventario()
        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion == 2:
        print("\n\t----COMPRA DE UNIDADES----")
        if not producto:
            print("Debe añadir productos primero")
        else:
            print("1. Ingresar un lote")
            print("2. Volver al Menú Principal")

            try:
                opcion2 = int(input("Ingrese el número de la opción: "))
            except ValueError:
                print("Opción inválida")
                continue

            if opcion2 == 1:
                for i in range(len(producto)):
                    print(f"{i}. {producto[i]}")

                try:
                    ind = int(input("\nIngrese el número del producto al que pertenece este lote: "))
                except ValueError:
                    print("Número inválido.")
                    continue

                if 0 <= ind < len(producto):
                    nombre_p = producto[ind]
                    nlotes = len(lote) + 1
                    fechai = input("Fecha (DD/MM/AAAA) de ingreso del lote: ")

                    try:
                        ingreso = int(input(f"Cantidad ingresada de {nombre_p}: "))
                        costo = float(input("Ingrese el costo: "))
                        precio = float(input("Ingrese el precio de venta: "))
                    except ValueError:
                        print("Debe ingresar datos numéricos válidos.")
                        continue

                    cantidad.append(ingreso)
                    productos.append(nombre_p)
                    precio_c.append(costo)
                    precio_v.append(precio)
                    fecha.append(fechai)
                    lote.append(f"N.{nlotes}")

                    recalcular_totales()
                    guardar_excel()
                    print(f"\nLote N.{nlotes} de {nombre_p} registrado con éxito.")
                else:
                    print("Número de producto inválido.")

            elif opcion2 == 2:
                print()

            else:
                print("Opción inválida")

        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion == 3:
        print("\n\t----VENTA DE UNIDADES----")
        if not producto:
            print("El inventario está vacío")
        else:
            print("1. Registrar una venta")
            print("2. Volver al menú principal")

            try:
                opcion3 = int(input("Ingrese el número de la opción: "))
            except ValueError:
                print("Opción inválida")
                continue

            if opcion3 == 1:
                print("\n\t--PRODUCTOS DISPONIBLES--")
                df_productos = pd.DataFrame({
                    "ÍNDICE": list(range(len(producto))),
                    "Nombre de los productos": producto,
                    "Cantidad total de los productos": cantidad_t
                })
                print(df_productos)

                try:
                    n_venta = int(input("Ingrese el número del producto: "))
                    venta_unidad = int(input("Ingrese el número de unidades a vender: "))
                except ValueError:
                    print("Debe ingresar números válidos.")
                    continue

                if not (0 <= n_venta < len(producto)):
                    print("Número de producto inválido.")
                elif venta_unidad <= 0:
                    print("La cantidad a vender debe ser mayor que cero.")
                elif venta_unidad > cantidad_t[n_venta]:
                    print("La cantidad que intentas vender es mayor que tu inventario.")
                else:
                    vendido = producto[n_venta]
                    restante = venta_unidad

                    for i in range(len(productos)):
                        if productos[i] == vendido and restante > 0:
                            if cantidad[i] > 0:
                                if cantidad[i] < restante:
                                    restante -= cantidad[i]
                                    cantidad[i] = 0
                                else:
                                    cantidad[i] -= restante
                                    restante = 0

                    recalcular_totales()
                    guardar_excel()
                    print("¡Venta realizada con éxito!")

            elif opcion3 == 2:
                print()

            else:
                print("Opción inválida")

        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion == 4:
        print("\n\t----AÑADIR PRODUCTOS----")
        print("1. Añadir un producto")
        print("2. Volver al menú principal")

        try:
            opcion4 = int(input("Ingrese el número de la opción: "))
        except ValueError:
            print("Opción inválida")
            continue

        if opcion4 == 1:
            nombre = input("Ingrese el nombre del producto: ").strip()

            if nombre == "":
                print("El nombre no puede estar vacío.")
            elif nombre in producto:
                print("Ese producto ya existe. Use la opción de compra de lotes para agregar más unidades.")
            else:
                try:
                    cuanto = int(input("Ingrese la cantidad inicial: "))
                    costo = float(input("Ingrese el costo unitario: "))
                    precio = float(input("Ingrese el precio de venta unitario: "))
                except ValueError:
                    print("Debe ingresar valores numéricos válidos.")
                    continue

                fechai = input("Fecha de ingreso: ")
                nlotes = len(lote) + 1

                productos.append(nombre)
                cantidad.append(cuanto)
                precio_c.append(costo)
                precio_v.append(precio)
                fecha.append(fechai)
                lote.append(f"N.{nlotes}")

                recalcular_totales()
                guardar_excel()
                print("\n¡Producto añadido correctamente!")

        elif opcion4 == 2:
            print()

        else:
            print("Opción inválida")

        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion == 5:
        print("\n\t----EDITAR DATOS----")
        if not productos:
            print("No hay registros para editar.")
        else:
            mostrar_inventario()

            try:
                editar = int(input("\nIngrese el índice del registro que desea editar: "))
            except ValueError:
                print("Debe ingresar un número válido.")
                continue

            if 0 <= editar < len(productos):
                print("\nDeje vacío si no desea cambiar ese dato.")

                nuevo_producto = input(f"Producto actual ({productos[editar]}): ").strip()
                nueva_cantidad = input(f"Cantidad actual ({cantidad[editar]}): ").strip()
                nuevo_costo = input(f"Costo actual ({precio_c[editar]}): ").strip()
                nuevo_precio = input(f"Precio actual ({precio_v[editar]}): ").strip()
                nueva_fecha = input(f"Fecha actual ({fecha[editar]}): ").strip()
                nuevo_lote = input(f"Lote actual ({lote[editar]}): ").strip()

                if nuevo_producto != "":
                    nombre_viejo = productos[editar]
                    productos[editar] = nuevo_producto

                if nueva_cantidad != "":
                    try:
                        cantidad[editar] = int(nueva_cantidad)
                    except ValueError:
                        print("Cantidad inválida. No se hizo ningún cambio en ese campo.")

                if nuevo_costo != "":
                    try:
                        precio_c[editar] = float(nuevo_costo)
                    except ValueError:
                        print("Costo inválido. No se hizo ningún cambio en ese campo.")

                if nuevo_precio != "":
                    try:
                        precio_v[editar] = float(nuevo_precio)
                    except ValueError:
                        print("Precio inválido. No se hizo ningún cambio en ese campo.")

                if nueva_fecha != "":
                    fecha[editar] = nueva_fecha

                if nuevo_lote != "":
                    lote[editar] = nuevo_lote

                recalcular_totales()
                guardar_excel()
                print("\n¡Registro editado correctamente!")

            else:
                print("Índice inválido.")

        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion == 6:
        print("\n\t----ELIMINAR REGISTROS----")
        if not productos:
            print("No hay registros para eliminar.")
        else:
            mostrar_inventario()

            try:
                eliminar = int(input("\nIngrese el índice del registro que desea eliminar: "))
            except ValueError:
                print("Debe ingresar un número válido.")
                continue

            if 0 <= eliminar < len(productos):
                print("\nRegistro seleccionado:")
                print(f"Producto: {productos[eliminar]}")
                print(f"Cantidad: {cantidad[eliminar]}")
                print(f"Costo: {precio_c[eliminar]}")
                print(f"Precio: {precio_v[eliminar]}")
                print(f"Fecha: {fecha[eliminar]}")
                print(f"Lote: {lote[eliminar]}")

                confirmar = input("\n¿Está seguro de eliminar este registro? (s/n): ").lower()

                if confirmar == "s":
                    productos.pop(eliminar)
                    cantidad.pop(eliminar)
                    precio_c.pop(eliminar)
                    precio_v.pop(eliminar)
                    fecha.pop(eliminar)
                    lote.pop(eliminar)

                    recalcular_totales()
                    guardar_excel()
                    print("\n¡Registro eliminado correctamente!")
                else:
                    print("Eliminación cancelada.")
            else:
                print("Índice inválido.")

        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion == 7:
        print("¡Gracias por usar el sistema!")
        break

    else:
        print("Opción inválida")
