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

# Función para reconstruir el camino desde el punto de encuentro
def reconstruir_camino(padres_inicio, padres_objetivo, interseccion, estado_inicial, estado_objetivo):
    # Reconstruir el camino desde el inicio hasta la intersección
    camino_desde_inicio = []
    estado_actual = interseccion
    while estado_actual is not None:
        camino_desde_inicio.append(estado_actual)
        estado_actual = padres_inicio[estado_actual]
    camino_desde_inicio.reverse()  # Invertimos el camino para que vaya desde el inicio a la intersección

    # Reconstruir el camino desde la intersección hasta el objetivo
    camino_desde_objetivo = []
    estado_actual = padres_objetivo[interseccion]
    while estado_actual is not None:
        camino_desde_objetivo.append(estado_actual)
        estado_actual = padres_objetivo[estado_actual]
    
    return camino_desde_inicio + camino_desde_objetivo

def bidirectional_search(estado_inicial, estado_objetivo):
    # Cola para la búsqueda desde el inicio y desde el objetivo
    cola_inicio = deque([estado_inicial])
    cola_objetivo = deque([estado_objetivo])

    # Diccionarios para rastrear los padres en ambas direcciones
    padres_inicio = {estado_inicial: None}
    padres_objetivo = {estado_objetivo: None}

    # Conjuntos visitados
    visitado_inicio = {estado_inicial}
    visitado_objetivo = {estado_objetivo}

    while cola_inicio and cola_objetivo:
        # Expandir desde el inicio
        estado_actual_inicio = cola_inicio.popleft()
        sucesores_inicio = Sucesora(estado_actual_inicio)
        
        for sucesor in sucesores_inicio.Sucesores:
            if sucesor not in visitado_inicio:
                visitado_inicio.add(sucesor)
                padres_inicio[sucesor] = estado_actual_inicio
                cola_inicio.append(sucesor)
            
            # Si el sucesor está en el conjunto objetivo, encontramos el punto de intersección
            if sucesor in visitado_objetivo:
                return reconstruir_camino(padres_inicio, padres_objetivo, sucesor, estado_inicial, estado_objetivo)

        # Expandir desde el objetivo
        estado_actual_objetivo = cola_objetivo.popleft()
        sucesores_objetivo = Sucesora(estado_actual_objetivo)
        
        for sucesor in sucesores_objetivo.Sucesores:
            if sucesor not in visitado_objetivo:
                visitado_objetivo.add(sucesor)
                padres_objetivo[sucesor] = estado_actual_objetivo
                cola_objetivo.append(sucesor)
            
            # Si el sucesor está en el conjunto inicio, encontramos el punto de intersección
            if sucesor in visitado_inicio:
                return reconstruir_camino(padres_inicio, padres_objetivo, sucesor, estado_inicial, estado_objetivo)
    
    return None  # No se encontró solución

def dfs_limitado(estado_actual, estado_objetivo, limite, padres, profundidad):
    if estado_actual == estado_objetivo:
        camino = []
        while estado_actual is not None:
            camino.append(estado_actual)
            estado_actual = padres[estado_actual]
        camino.reverse()
        return camino
    
    if profundidad >= limite:
        return None

    estado_actual_objeto = Sucesora(estado_actual)
    for sucesor in estado_actual_objeto.Sucesores:
        if sucesor not in padres:  # Evitar ciclos
            padres[sucesor] = estado_actual
            resultado = dfs_limitado(sucesor, estado_objetivo, limite, padres, profundidad + 1)
            if resultado is not None:
                return resultado
    
    return None

def iddfs(estado_inicial, estado_objetivo, limite_maximo):
    for limite in range(limite_maximo + 1):
        padres = {estado_inicial: None}
        resultado = dfs_limitado(estado_inicial, estado_objetivo, limite, padres, 0)
        if resultado is not None:
            return resultado
    return None

# Definir el estado inicial
estado_inicial_ladoA = (3, 3, True, 0, 0, False)

# Definir un límite máximo para la profundidad
limite_maximo = 20

camino = iddfs(estado_inicial_ladoA, estado_objetivo, limite_maximo)

def main():
    # Menú para elegir el tipo de búsqueda
    print("Seleccione el tipo de búsqueda:")
    print("1. Búsqueda en profundidad (DFS)")
    print("2. Búsqueda en anchura (BFS)")
    print("3. Búsqueda bidireccional")
    print("4. Búsqueda profundidad iterativa (IDDFS)")
    
    opcion = input("Ingrese su opción (1, 2, 3 0 4): ")
    
    # Validar la opción
    while opcion not in ['1', '2', '3','4']:
        print("Opción no válida. Intente nuevamente.")
        opcion = input("Ingrese su opción (1, 2, 3 0 4): ")

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
    elif opcion == '2':
        print("Ejecutando búsqueda en anchura (BFS)...")
        soluciones = [bfs(estado_inicial_ladoA, estado_objetivo)]  # BFS retorna una única solución
    elif opcion == '3':
        print("Ejecutando búsqueda bidireccional...")
        soluciones = [bidirectional_search(estado_inicial_ladoA, estado_objetivo)]
    else:
        print("Ejecutando búsqueda iterativo por profundidad...")
        soluciones = [iddfs(estado_inicial_ladoA, estado_objetivo, limite_maximo)]

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