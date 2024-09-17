import time
import psutil
from collections import deque
from estado import Estado

# Estado objetivo
estado_objetivo = (0, 0, False, 3, 3, True)

def es_estado_valido(estado):
    lA, oA, _, lB, oB, _ = estado
    if lA > oA and oA > 0:
        return False
    if lB > oB and oB > 0:
        return False
    if lA < 0 or oA < 0 or lB < 0 or oB < 0:
        return False
    return True

def Sucesora(estado_inicial):
    if estado_inicial is None:
        return Estado(None, [])
    
    sucesores_estado = []
    cambios = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]
    
    lA, oA, boteA, lB, oB, boteB = estado_inicial
    
    if boteA:
        for cambio in cambios:
            nuevo_lA = lA - cambio[0]
            nuevo_oA = oA - cambio[1]
            nuevo_lB = lB + cambio[0]
            nuevo_oB = oB + cambio[1]
            
            nuevo_estado = (nuevo_lA, nuevo_oA, False, nuevo_lB, nuevo_oB, True)
            
            if es_estado_valido(nuevo_estado):
                sucesores_estado.append(nuevo_estado)
    else:
        for cambio in cambios:
            nuevo_lA = lA + cambio[0]
            nuevo_oA = oA + cambio[1]
            nuevo_lB = lB - cambio[0]
            nuevo_oB = oB - cambio[1]
            
            nuevo_estado = (nuevo_lA, nuevo_oA, True, nuevo_lB, nuevo_oB, False)
            
            if es_estado_valido(nuevo_estado):
                sucesores_estado.append(nuevo_estado)
    
    return Estado(estado_inicial, sucesores_estado)

def dfs(estado_inicial, estado_objetivo):
    if estado_inicial is None:
        return []
    
    pila = [estado_inicial]
    padres = {estado_inicial: None}
    soluciones = []
    
    while pila:
        estado_actual = pila.pop()
        
        if estado_actual == estado_objetivo:
            camino = []
            while estado_actual is not None:
                camino.append(estado_actual)
                estado_actual = padres[estado_actual]
            camino.reverse()
            soluciones.append(camino)
        
        sucesores = Sucesora(estado_actual)
        for sucesor in sucesores.Sucesores:
            if sucesor is not None and sucesor not in padres:
                padres[sucesor] = estado_actual
                pila.append(sucesor)
    
    return soluciones

def bfs(estado_inicial, estado_objetivo):
    cola = deque([estado_inicial])
    padres = {estado_inicial: None}
    
    while cola:
        estado_actual = cola.popleft()
        
        if estado_actual == estado_objetivo:
            camino = []
            while estado_actual is not None:
                camino.append(estado_actual)
                estado_actual = padres[estado_actual]
            camino.reverse()
            return camino
        
        sucesores = Sucesora(estado_actual)
        for sucesor in sucesores.Sucesores:
            if sucesor not in padres:
                padres[sucesor] = estado_actual
                cola.append(sucesor)
    
    return None

def main():
    # Menú para elegir el tipo de búsqueda
    print("Seleccione el tipo de búsqueda:")
    print("1. Búsqueda en profundidad (DFS)")
    print("2. Búsqueda en anchura (BFS)")
    
    opcion = input("Ingrese su opción (1 o 2): ")
    
    # Validar la opción
    while opcion not in ['1', '2']:
        print("Opción no válida. Intente nuevamente.")
        opcion = input("Ingrese su opción (1 o 2): ")

    # Medir el tiempo de inicio
    tiempo_inicio = time.time()
    
    # Obtener el uso de memoria inicial
    proceso = psutil.Process()
    memoria_inicio = proceso.memory_info().rss / 1024 / 1024  # Convertir a MB

    # Definir el estado inicial
    estado_inicial_ladoA = (3, 3, True, 0, 0, False)
    
    # Ejecutar la búsqueda seleccionada
    if opcion == '1':
        print("Ejecutando búsqueda en profundidad (DFS)...")
        soluciones = dfs(estado_inicial_ladoA, estado_objetivo)
    else:
        print("Ejecutando búsqueda en anchura (BFS)...")
        soluciones = [bfs(estado_inicial_ladoA, estado_objetivo)]  # BFS retorna una única solución

    # Medir el tiempo final
    tiempo_fin = time.time()
    
    # Obtener el uso de memoria final
    memoria_fin = proceso.memory_info().rss / 1024 / 1024  # Convertir a MB

    # Calcular el tiempo total y el uso de memoria
    tiempo_total = tiempo_fin - tiempo_inicio
    memoria_usada = memoria_fin - memoria_inicio

    # Mostrar todas las soluciones
    if soluciones and soluciones[0] is not None:
        print(f"Se encontraron {len(soluciones)} soluciones:")
        for i, solucion in enumerate(soluciones, 1):
            print(f"Solución {i}:")
            for estado in solucion:
                print(estado)
    else:
        print("No se encontró ninguna solución.")

    # Mostrar las métricas de tiempo y memoria
    print(f"\nTiempo de ejecución: {tiempo_total:.4f} segundos")
    print(f"Memoria utilizada: {memoria_usada:.2f} MB")

if __name__ == "__main__":
    main()
