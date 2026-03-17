import pandas as pd
import os

productos=[]
cantidad=[]
precio_c=[]
precio_v=[]
fecha=[]
lote=[]
producto=[]
cantidad_t=[]

def cargar_datos():
    global productos,cantidad,precio_c,precio_v,fecha,lote,producto,cantidad_t
    if os.path.exists('Inventario.xlsx'):
        inventario=pd.read_excel('Inventario.xlsx',sheet_name='Sheet1')
        productos=inventario["PRODUCTOS"].values.tolist()
        cantidad=inventario["CANTIDAD"].values.tolist()
        precio_c=inventario["COSTO"].values.tolist()
        precio_v=inventario["PRECIO"].values.tolist()
        fecha=inventario["FECHA DE INGRESO"].values.tolist()
        lote=inventario["LOTE"].values.tolist()

        p_disponible=pd.read_excel('Inventario.xlsx',sheet_name='Sheet2')
        producto=p_disponible["Nombre de los productos"].values.tolist()
        cantidad_t=p_disponible["Cantidad total de los productos"].values.tolist()

def guardar_excel():
    inventario=pd.DataFrame({"PRODUCTOS":productos,"CANTIDAD":cantidad,"COSTO":precio_c,"PRECIO":precio_v,
                             "FECHA DE INGRESO":fecha,"LOTE":lote})
    p_disponible=pd.DataFrame({"Nombre de los productos":producto,"Cantidad total de los productos":cantidad_t})
    with pd.ExcelWriter('Inventario.xlsx',engine='xlsxwriter') as writer:
        inventario.to_excel(writer,sheet_name='Sheet1',index=False)
        p_disponible.to_excel(writer,sheet_name='Sheet2',index=False)

cargar_datos()

while True:
    print("\n\t.:MENÚ PRINCIPAL:.")
    print("1.Revisar Inventario\n2.Compra de Unidades (Lotes)\n3.Venta de Unidades\n4.Añadir Productos\n5.Salir del Programa")
    opcion=int(input("Ingrese el número de la acción a realizar: "))

    if opcion==1:
        print("\n\t----Revisar Inventario----")
        if not productos:
            print("El inventario está vacío")
        else:
            print(pd.DataFrame({"PRODUCTOS":productos,"CANTIDAD":cantidad,"COSTO":precio_c,"PRECIO":precio_v,
                                "FECHA DE INGRESO":fecha,"LOTE":lote}))
        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion==2:
        print("\n\t----COMPRA DE UNIDADES----")
        if not productos:
            print("Debe añadir productos primero")
        else:
            print("1.Ingresar un lote\n2.Volver al Menú Principal")
            opcion2=int(input("Ingrese el número de la opción: "))
            if opcion2==1:
                for i in range(len(producto)):
                    print(f"\n{i}.{producto[i]}")
                ind=int(input("\nIngrese el número del producto al que pertenece este lote: "))
                if 0<=ind<len(producto):
                    nombre_p=producto[ind]
                    nlotes=len(lote)+1
                    fechai=str(input("Fecha de ingreso del lote: "))
                    ingreso=int(input(f"Cantidad ingresada de {nombre_p}: "))

                    cantidad.append(ingreso)
                    cantidad_t[ind]+=ingreso
                    productos.append(nombre_p)
                    precio_c.append(float(input("Ingrese el costo: ")))
                    precio_v.append(float(input("Ingrese el precio de venta: ")))
                    fecha.append(fechai)
                    lote.append(f"N.{nlotes}")

                    guardar_excel()
                    print(f"\nLote N.{nlotes} {nombre_p} registrado con éxito.")
                else:
                    print("Número de producto inválido.")
            elif opcion2==2:
                print()
            else:
                print("Opción inválida")
        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion==3:
        print("\n\t----Venta de Unidades----")
        if not productos:
            print("El inventario está vacío")
        else:
            print("1.Registrar una venta\n2.Volver al menú principal")
            opcion3=int(input("Ingrese el número de la opción: "))
            if opcion3==1:
                print("\n\t--PRODUCTOS DISPONIBLES--")
                print(pd.DataFrame({"Nombre de los productos":producto,"Cantidad total de los productos":cantidad_t}))
                n_venta=int(input("Ingrese el número del producto: "))
                venta_unidad=int(input("Ingrese el número de unidades a vender: "))
                if venta_unidad>cantidad_t[n_venta]:
                    print("La cantidad que intentas vender es más grande que tu inventario")
                else:
                    vendido=producto[n_venta]
                    venta_og=venta_unidad
                    for i in range(len(productos)):
                        if productos[i]==vendido:
                            if cantidad[i]>0:
                                if cantidad[i]<venta_unidad:
                                    venta_unidad-=cantidad[i]
                                    cantidad[i]=0
                                else:
                                    cantidad[i]-=venta_unidad
                                    venta_unidad=0
                    cantidad_t[n_venta]-=venta_og
                guardar_excel()
                print("¡Venta realizada con éxito!")

            elif opcion3==2:
                print()
            else:
                print("Opción inválida")
        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion==4:
        print("\n\t----Añadir Productos----")
        print("1.Añadir un producto\n2.Volver al menú principal")
        opcion4=int(input("Ingrese el número de la opción: "))
        if opcion4==1:
            nombre=input("Ingrese el nombre del producto: ")
            productos.append(nombre)
            producto.append(nombre)
            cuanto=int(input("Ingrese la cantidad inicial: "))
            cantidad.append(cuanto)
            cantidad_t.append(cuanto)
            precio_c.append(input("Ingrese el costo unitario: "))
            precio_v.append(input("Ingrese el precio de venta unitario: "))
            fecha.append(input("Fecha de ingreso: "))
            nlotes=len(lote)+1
            lote.append(f"N.{nlotes}")

            guardar_excel()
            print("\n¡Producto añadido correctamente!")

        elif opcion4==2:
            print()
        else:
            print("Opción inválida")
        print("\nPresione Enter para volver al Menú Principal")
        input()

    elif opcion==5:
        print("¡Gracias por usar el sistema!")
        break
    else:
        print("Opción inválida")
        break
        #holA
