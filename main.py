import pandas as pd
import numpy as np

f=0
n=0
try:
    inventario = pd.read_excel('Inventario.xlsx',sheet_name='Sheet1')
    productos= (inventario["PRODUCTOS"]).values.tolist()
    cantidad = (inventario["CANTIDAD"]).values.tolist()
    precioC = (inventario["COSTO"]).values.tolist()
    precioV = (inventario["PRECIO"]).values.tolist()
    fecha = (inventario["FECHA DE INGRESO"]).values.tolist()
    pro_lotes = pd.read_excel('Inventario.xlsx',sheet_name='Sheet2')
    prod = pro_lotes["productos"].values.tolist()
    pro = prod[0]
    lotess = pro_lotes["lotes"].values.tolist()
    lotes = lotess[0]
    producto_disponible = pd.read_excel('Inventario.xlsx',sheet_name='Sheet3')
    producto= (producto_disponible["nombres de los productos"].values.tolist())
    cantidadtot = (producto_disponible["cantidades totales de los productos"]).values.tolist()

except FileNotFoundError:
    productos = ["-"]
    cantidad = [0]
    precioC = ["Lote"]
    precioV = ["Inicial"]
    fecha = ["-"]
    inventario = pd.DataFrame(
        {"PRODUCTOS": productos, "CANTIDAD": cantidad, "COSTO": precioC, "PRECIO": precioV, "FECHA DE INGRESO": fecha})
    producto = []
    cantidadtot = []
    lotes = 0
    pro = 0


while f==0:
    print("1) Revisar Inventario")
    print("2) Añadir Productos")
    print("3) Compra de Unidades")
    print("4) Venta de Unidades")
    print("5) Cambios a los Productos")
    print("6) Salir del Programa")
    option = input("Ingrese el Numero de la Opcion: ")

    if option == "1":
        print("===Revisar Inventario===")
        if pro==0:
            print("no hay inventario")
            print("presione enter para continuar")
            input()
        else:
            print(inventario)

    elif option == "2":
        print("===Añadir Productos===")
        print("1) añadir productos")
        print("2) Volver al Menu Principal")
        option2 = input("Ingrese el Numero de la Opcion: ")
        if option2 == "1":
            print("===añadir productos===")
            nombre = input("Ingrese el Nombre del Producto: ")
            productos.append(nombre)
            producto.append(nombre)
            cuanto = int(input("Ingrese la cantidad inicial: "))
            cantidad.append(cuanto)
            cantidadtot.append(cuanto)
            costo = input("Ingrese el costo unitario: ")
            precioC.append(costo)
            PrecioFinal = input("Ingrese el precio Final del Producto: ")
            precioV.append(PrecioFinal)
            fechaI = input("Ingrese la Fecha de Ingreso: ")
            fecha.append(fechaI)
            inventario = pd.DataFrame(
                {"PRODUCTOS": productos , "CANTIDAD": cantidad , "COSTO": precioC, "PRECIO": precioV ,
                 "FECHA DE INGRESO": fecha })
            pro += 1

        if option2=="2" :
            print("Volviendo al Menu Principal...")
        else:
            print("opcion invalida")

    elif option == "3":
        if pro == 0:
            print("no hay inventario")
        else:
            print("===INGRESO DE LOTES===")
            print("Desea Ingresar un Lote?")
            print("1)si")
            print("2)No")
            option3 = input("Ingrese el Numero de la Opcion: ")
            if option3 == "1":
                lotes+=1
                productos.append("-")
                cantidad.append(0)
                precioC.append("Lote ")
                precioV.append(f"N.{lotes}")
                fecha.append("-")
                fechai = input("Ingrese la fecha de ingreso de el lote")
                for i in range(0,pro,1):
                    productos.append(producto[i])
                    ingreso = int(input("ingrese la cantidad: "))
                    cantidad.append(ingreso)
                    cantidadtot[i]=cantidadtot[i]+ingreso
                    precioC.append(input("ingrese el costo : "))
                    precioV.append(input("ingrese el precio : "))
                    fecha.append(fechai)
                    inventario = pd.DataFrame(
                        {"PRODUCTOS": productos , "CANTIDAD": cantidad , "COSTO": precioC ,
                         "PRECIO": precioV ,
                         "FECHA DE INGRESO": fecha})


            elif option3 == "2":
                print("Presione Enter para Volver al Menu")
                input()
            else:
                print("Opcion invalida")

    elif option == "4":
        if pro == 0:
            print("no hay inventario")
        else:
            print("===Venta de Unidades===")
            print("Desea Vender Unidades de un Producto?")
            print("1)si")
            print("2)No")
            option4 = int(input("Ingrese el Numero de la Opcion: "))
            if option4 == 1:
                v=0
                bool = []
                print("=PRODUCTOS DISPONIBLES=")
                producto_dispobibles = pd.DataFrame({"Productos":producto,"Cantidad Total":cantidadtot})
                print(producto_dispobibles)
                Nventa = int(input("Ingrese el numero del producto: "))
                vendido = producto[Nventa]
                venta_unidad = int(input("Ingrese el numero de unidades para la venta: "))
                if venta_unidad > cantidadtot[Nventa]:
                    print("La cantidad que intentas vender es mas grande que tu inventario")
                else:
                    for prod in productos:
                        if prod == vendido:
                            bol = True
                            bool.append(bol)
                        else:
                            bol = False
                            bool.append(bol)
                    for bolean in bool:
                        if bolean == True:
                            if cantidad[v] < venta_unidad:
                                venta_unidad = venta_unidad - cantidad[v]
                                cantidad[v] = 0
                            else:
                                cantidad[v] = cantidad[v] - venta_unidad
                        if bolean == False:
                            print("")
                        v += 1
                    inventario = pd.DataFrame(
                        {"PRODUCTOS": productos, "CANTIDAD": cantidad, "COSTO": precioC, "PRECIO": precioV,
                         "FECHA DE INGRESO": fecha})

            elif option4 == 2:
                print("Presione Cualquier Tecla para Volver al Menu")
                input()
            else:
                print("Opcion invalida")

    elif option == "5":
        if pro == 0:
            print("no hay inventario")
        else:
            print("===Cambios a los Productos===")
            print("1) Modificar los Nombres")
            print("2) Modificar el Costo de los productos")
            print("3) Modificar Precio de Venta")
            print("4) Modificar Fecha de Ingreso")
            print("5) Salir al Menu Principal")
            option5 = input("Ingrese el Numero de la Opcion: ")
            if option5 == "1":
                v = 0
                bool = []
                print(pd.DataFrame({"PRODUCTOS REGISTRADOS":producto}))
                nprod = int(input("Ingrese el numero del producto: "))
                prod_reemplazado = producto[nprod]
                Nnombre = input("Ingrese el nombre nuevo del producto: ")
                for prod in productos:
                    if prod == prod_reemplazado:
                        bol = True
                        bool.append(bol)
                    else:
                        bol = False
                        bool.append(bol)
                for bolean in bool:
                    if bolean == True:
                        productos[v] = Nnombre
                    if bolean == False:
                        print("")
                    v+=1
                inventario = pd.DataFrame(
                            {"PRODUCTOS": productos, "CANTIDAD": cantidad, "COSTO": precioC, "PRECIO": precioV,
                             "FECHA DE INGRESO": fecha})
            elif option5 == "2":
                bool = []
                print(inventario)
                ncosto = int(input("Ingrese el numero del producto: "))
                precioC[ncosto] = input("Ingrese el costo nuevo del producto: ")
                inventario = pd.DataFrame(
                    {"PRODUCTOS": productos, "CANTIDAD": cantidad, "COSTO": precioC, "PRECIO": precioV,
                     "FECHA DE INGRESO": fecha})
            elif option5 == "3":
                bool = []
                print(inventario)
                nprecio = int(input("Ingrese el numero del producto: "))
                precioV[nprecio] = input("Ingrese el precio nuevo del producto: ")
                inventario = pd.DataFrame(
                    {"PRODUCTOS": productos, "CANTIDAD": cantidad, "COSTO": precioC, "PRECIO": precioV,
                     "FECHA DE INGRESO": fecha})
            elif option5 == "4":
                bool = []
                print(inventario)
                nfecha = int(input("Ingrese el numero del producto: "))
                fecha[nfecha] = input("Ingrese la nueva fecha del producto: ")
                inventario = pd.DataFrame(
                    {"PRODUCTOS": productos, "CANTIDAD": cantidad, "COSTO": precioC, "PRECIO": precioV,
                     "FECHA DE INGRESO": fecha})
            elif option5 == "5":
                print("Presione Cualquier Tecla para Volver al Menu")
                input()
            else:
                print("Opcion invalida")

    elif option == "6":
        break
    else:
        print("Opcion invalida")

datos_importantes = pd.DataFrame({"productos":pro,"lotes":lotes},index=[0])
datos_importantes3 = pd.DataFrame({"nombres de los productos":producto,"cantidades totales de los productos":cantidadtot})
nombre_archivo = 'Inventario.xlsx'

try:
    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:

        inventario.to_excel(writer, sheet_name='Sheet1', index=False)
        datos_importantes.to_excel(writer, sheet_name='Sheet2', index=False,header=True)
        datos_importantes3.to_excel(writer, sheet_name='Sheet3', index=False, header=True)
except Exception as e:
    print("Ocurrió un error al guardar el archivo, intente de nuevo su operacion")