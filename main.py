# Menú y flujo principal
# # Proyecto Final - Camino a mi casa
# Bienvenida al programa
# test
print("=====================================")
print("   CAMINO A MI CASA")
print("=====================================")
print("Este programa te ayudará a encontrar la distancia al destino deseado desde donde te encuentres.")
while True:
    # Comenzamos pidiendo las opciones al usuario
    print("1. Calcular distancia entre dos ciudades \n2. Salir")
    opcion = input("Ingrese la opción deseada: ").strip() # le quitamos espacios demas
    if opcion == "1":
        # Pedimos ambos ubicacaiones al usuario, las llevamos a minusculas y quitamos espacios de mas
        start = input("Ingrese el lugar donde te encuentras (ciudad, pais): ").strip().lower()
        end = input("Ingrese el lugar donde deseas llegar (ciudad, pais): ").strip().lower()
        # Validamos que el usauro no entregue vacio
        if start == "" or end == "":
            print("Por favor, ingrese lugares válidos.")
            continue
        # Validamos que las ubicaciones no son las mismas
        if start == end:
            print("El lugar de inicio y destino son iguales. Por favor, ingrese lugares diferentes.")
            continue
        # validamos que por lo menos tengan 2 caracteres
        if len(start) < 2 or len(end) < 2:
            print("Por favor, ingrese lugares con al menos 2 caracteres.")
            continue

        if not any(c.isalpha() for c in start) or not any(c.isalpha() for c in end):
            print("Por favor, ingrese nombres de lugares válidos (deben contener letras).")
            continue
        # que diga lo que vamos a calcular
        print("Calculando la distancia entre", start, "y", end, "...")
        break
    # Si quiere salir del programa
    elif opcion == "2":
        print("Gracias por usar el programa. ¡Hasta luego!")
        break
    # Ponemos esto en caso que no responde no 1 ni 2. 
    else:
        print("Opción no válida. Por favor, ingrese una opción válida.")

