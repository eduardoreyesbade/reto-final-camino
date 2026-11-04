# Menú y flujo principal
# # Proyecto Final - Camino a mi casa
# Bienvenida al programa
# test
print("=====================================")
print("   CAMINO A MI CASA")
print("=====================================")
print("Este programa te ayudará a encontrar la distancia al destino deseado desde donde te encuentres.")
while True:
    print("1. Calcular distancia entre dos ciudades \n2. Salir")
    opcion = input("Ingrese la opción deseada: ").strip()
    if opcion == "1":
        start = input("Ingrese el lugar donde te encuentras (ciudad, pais): ").strip().lower()
        end = input("Ingrese el lugar donde deseas llegar (ciudad, pais): ").strip().lower()
        if start == "" or end == "":
            print("Por favor, ingrese lugares válidos.")
            continue
        if start == end:
            print("El lugar de inicio y destino son iguales. Por favor, ingrese lugares diferentes.")
            continue
        if len(start) < 2 or len(end) < 2:
            print("Por favor, ingrese lugares con al menos 2 caracteres.")
            continue
        if not any(c.isalpha() for c in start) or not any(c.isalpha() for c in end):
            print("Por favor, ingrese nombres de lugares válidos (deben contener letras).")
            continue
        print("Calculando la distancia entre", start, "y", end, "...")
        break
    elif opcion == "2":
        print("Gracias por usar el programa. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, ingrese una opción válida.")

