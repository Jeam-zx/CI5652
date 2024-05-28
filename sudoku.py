sudoku_incorrecto = [
    [6, 3, 7, 1, 7, 9, 2, 4, 8],
    [2, 8, 1, 3, 4, 7, 9, 5, 6],
    [5, 9, 3, 2, 6, 8, 1, 7, 3],
    [8, 1, 6, 5, 9, 2, 7, 3, 4],
    [4, 2, 9, 5, 8, 4, 6, 1, 5],
    [3, 7, 5, 6, 1, 4, 8, 2, 9],
    [7, 4, 2, 9, 3, 6, 5, 8, 1],
    [9, 5, 3, 8, 2, 1, 4, 6, 7],
    [1, 6, 8, 4, 7, 5, 3, 9, 2]
]  

def vecindad(sudoku):
    """
    Funcion que recibe un sudoku y retorna la vecindad de este.
    """
    vecindad = []
    for i in range(9):
        for j in range(9):
            for k in range(1, 10):
                if sudoku[i][j] != k:
                    vecino = [fila.copy() for fila in sudoku]
                    vecino[i][j] = k
                    vecindad.append((vecino, (i, j)))
    return vecindad

def verificar_sudoku(matriz):
    def verificar_filas(matriz):
        errores = []
        for i, fila in enumerate(matriz):
            contador = {}
            for j, numero in enumerate(fila):
                if numero in contador:
                    contador[numero].append((i, j))
                else:
                    contador[numero] = [(i, j)]
            for posiciones in contador.values():
                if len(posiciones) > 1:
                    errores.extend(posiciones)
        return errores

    def verificar_columnas(matriz):
        errores = []
        for col in range(9):
            contador = {}
            for fila in range(9):
                numero = matriz[fila][col]
                if numero in contador:
                    contador[numero].append((fila, col))
                else:
                    contador[numero] = [(fila, col)]
            for posiciones in contador.values():
                if len(posiciones) > 1:
                    errores.extend(posiciones)
        return errores

    def verificar_submatrices(matriz):
        errores = []
        for box_row in range(3):
            for box_col in range(3):
                contador = {}
                for i in range(3):
                    for j in range(3):
                        fila = box_row * 3 + i
                        col = box_col * 3 + j
                        numero = matriz[fila][col]
                        if numero in contador:
                            contador[numero].append((fila, col))
                        else:
                            contador[numero] = [(fila, col)]
                for posiciones in contador.values():
                    if len(posiciones) > 1:
                        errores.extend(posiciones)
        return errores

    errores_filas = verificar_filas(matriz)
    errores_columnas = verificar_columnas(matriz)
    errores_submatrices = verificar_submatrices(matriz)

    # Unificar los errores eliminando duplicados
    errores_totales = set(errores_filas + errores_columnas + errores_submatrices)
    
    return errores_totales

def local_search(sudoku):
    """
    Funcion que recibe un sudoku y retorna el sudoku solucionado.
    """
    mejor_sudoku = sudoku
    mejor_costo = len(verificar_sudoku(sudoku))
    print("Costo inicial:", mejor_costo)
    imprimir_sudoku(mejor_sudoku)
    cnt = 0
    while True:
        vecinos = vecindad(mejor_sudoku)
        for vecino, p, q in vecinos:
            costo_vecino = len(verificar_sudoku(vecino))
            if costo_vecino < mejor_costo:
                cnt += 1
                mejor_sudoku = vecino
                mejor_costo = costo_vecino
                print("Costo actual:", mejor_costo)
                imprimir_sudoku(mejor_sudoku)
                print("Intercambio:", p, q)
                print("Iteraciones:", cnt)
                break
        else:
            break

    return mejor_sudoku

def imprimir_sudoku(sudoku):
    for fila in sudoku:
        print(fila)

solucion = local_search(sudoku_incorrecto)

def causa_conflicto_pos(sudoku, pos):
    """
    Funcion que recibe un sudoku y una posicion y retorna si esta posicion causa conflicto.
    """
    i, j = pos
    for k in range(9):
        if k != i and sudoku[k][j] == sudoku[i][j]:
            return True
    for l in range(9):
        if l != j and sudoku[i][l] == sudoku[i][j]:
            return True
    box_row = i // 3
    box_col = j // 3
    for m in range(3):
        for n in range(3):
            if (box_row * 3 + m != i or box_col * 3 + n != j) and sudoku[box_row * 3 + m][box_col * 3 + n] == sudoku[i][j]:
                return True
    return False

tabu_list = []

def vecindad_tabu(sudoku):
    """
    Funcion que recibe un sudoku y retorna la vecindad de este.
    """
    vecindad = []
    for i in range(9):
        for j in range(9):
            for k in range(1, 10):
                if sudoku[i][j] != k and True:
                    vecino = [fila.copy() for fila in sudoku]
                    vecino[i][j] = k
                    if not causa_conflicto_pos(vecino, (i, j)):
                        vecindad.append((vecino,(i, j)))
                        if len(tabu_list) > 2:
                            tabu_list.pop(0)

    if len(vecindad) == 0:
        for i in range(9):
            for j in range(9):
                for k in range(1, 10):
                    if sudoku[i][j] != k:
                        vecino = [fila.copy() for fila in sudoku]
                        vecino[i][j] = k
                        vecindad.append((vecino, (i, j)))
                

    return vecindad



def local_search_tabu(sudoku):
    """
    Funcion que recibe un sudoku y retorna el sudoku solucionado.
    """
    mejor_sudoku = sudoku
    mejor_costo = len(verificar_sudoku(sudoku))
    print("Costo inicial:", mejor_costo)
    imprimir_sudoku(mejor_sudoku)
    cnt = 0
    while True:
        vecinos = vecindad_tabu(mejor_sudoku)
        print("Vecinos tabu:", len(vecinos))
        for vecino, p, q in vecinos:
            costo_vecino = len(verificar_sudoku(vecino))
            if costo_vecino < mejor_costo:
                cnt += 1
                mejor_sudoku = vecino
                mejor_costo = costo_vecino
                print("Costo actual tabu:", mejor_costo)
                imprimir_sudoku(mejor_sudoku)
                tabu_list.append((p, q))
                print("Intercambio tabu:", p, q)
                print("Iteraciones tabu:", cnt)
                break
        else:
            break
    print("Costo final tabu:", mejor_costo)
    return mejor_sudoku

print("Comienza la busqueda tabu")
solucion = local_search_tabu(sudoku_incorrecto)



