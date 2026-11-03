# Proyecto Final - Camino a mi casa
# Bienvenida al programa
print("=====================================")
print("   CAMINO A MI CASA")
print("=====================================")
print("Este programa te ayudará a encontrar la distancia al destino deseado desde donde te encuentres.")
while True:
    print("1. Calcular distancia entre dos ciudades \n2. Salir")
    opcion = input("Ingrese la opción deseada: ")
    if opcion == "1":
        start = input("Ingrese el lugar donde te encuentras (ciudad, pais): ")
        end = input("Ingrese el lugar donde deseas llegar (ciudad, pais): ")
    elif opcion == "2":
        print("Gracias por usar el programa. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, ingrese una opción válida.")
