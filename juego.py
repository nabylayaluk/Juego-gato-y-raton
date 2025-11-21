import random
import time

filas = 8
columnas = 8
vacio = '_'

# Movimientos posibles para la IA (4 direcciones)
movs = [
    (-1, 0), (1, 0), (0, -1), (0, 1)
]

# Controles humanos WASD + diagonales (8 direcciones)
controles = {
    'w': (-1, 0),   # arriba
    's': (1, 0),    # abajo
    'a': (0, -1),   # izquierda
    'd': (0, 1),    # derecha
    'q': (-1, -1),  # arriba izquierda
    'e': (-1, 1),   # arriba derecha
    'z': (1, -1),   # abajo izquierda
    'c': (1, 1),    # abajo derecha
}

# MANEJO DEL TABLERO

def crear_tablero():
    tablero = []
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(vacio)
        tablero.append(fila)
    return tablero

def limpiar_tablero(tablero):
    for f in range(filas):
        for c in range(columnas):
            tablero[f][c] = vacio

def poner(tablero, pos, simbolo):
    f, c = pos
    tablero[f][c] = simbolo

def mostrar(tablero):
    print("\n" + "-" * (columnas + 2))
    for fila_ in tablero:
        print("|" + "".join(fila_) + "|")
    print("-" * (columnas + 2) + "\n")

# LÓGICA DEL JUEGO

def posiciones_iniciales():
    posiciones = []
    for f in range(filas):
        for c in range(columnas):
            posiciones.append((f, c))
    raton, gato, puerta = random.sample(posiciones, 3)
    return raton, gato, puerta

def mov_validos(pos, movimientos=movs):
    f, c = pos
    res = []
    for cambio_fila, cambio_columna in movimientos:
        nf, nc = f + cambio_fila, c + cambio_columna
        if 0 <= nf < filas and 0 <= nc < columnas:
            res.append((nf, nc))
    return res

# HEURÍSTICAS Y MINIMAX

# Gato es MAX, raton es MIN

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def terminal(raton, gato, puerta):
    if raton == gato:
        return True, "gato"
    if raton == puerta:
        return True, "raton"
    return False, None

def eval_posi(raton, gato, puerta):
    if raton == gato:
        return 10000
    if raton == puerta:
        return -10000
    dist_puerta = manhattan(raton, puerta)
    dist_gato = manhattan(raton, gato)
    return 50 * dist_puerta - dist_gato

def minimax(raton, gato, puerta, depth, max_player):
    term, win = terminal(raton, gato, puerta)
    if term:
        return 10000 if win == "gato" else -10000
    if depth == 0:
        return eval_posi(raton, gato, puerta)

    if max_player:  # GATO (MAX)
        value = -float('inf')
        for nuevo_gato in mov_validos(gato):
            val = minimax(raton, nuevo_gato, puerta, depth - 1, False)
            value = max(value, val)
        return value

    else:  # RATÓN (MIN)
        value = float('inf')
        for nuevo_raton in mov_validos(raton):
            val = minimax(nuevo_raton, gato, puerta, depth - 1, True)
            value = min(value, val)
        return value

# ELECCIÓN DE MOVIMIENTOS

def mejor_mov_gato(raton, gato, puerta, depth):
    mejor = -float('inf')
    opciones = []
    for pos in mov_validos(gato):
        val = minimax(raton, pos, puerta, depth - 1, False)
        if val > mejor:
            mejor = val
            opciones = [pos]
        elif val == mejor:
            opciones.append(pos)
    return random.choice(opciones)

def mejor_mov_raton(raton, gato, puerta, depth):
    mejor = float('inf')
    opciones = []
    for pos in mov_validos(raton):
        val = minimax(pos, gato, puerta, depth - 1, True)
        if val < mejor:
            mejor = val
            opciones = [pos]
        elif val == mejor:
            opciones.append(pos)
    return random.choice(opciones)

# INPUT HUMANO (8 MOVIMIENTOS)

def pedir_movimiento_wasd(pos_actual):
    print("Movimiento con W A S D (4 dir) + Q E Z C (diagonales)")
    print("w/a/s/d = arriba/izq/abajo/der")
    print("q/e/z/c = diagonales")
    while True:
        tecla = input("Tu movimiento: ").lower().strip()
        if tecla not in controles:
            print("Tecla inválida. Usá WASD o QEZX para diagonales.")
            continue
        cambio_fila, cambio_columna = controles[tecla]
        f, c = pos_actual
        nf, nc = f + cambio_fila, c + cambio_columna
        if 0 <= nf < filas and 0 <= nc < columnas:
            return (nf, nc)
        print("Movimiento fuera del tablero. Probá otra tecla.")

# LOOP PRINCIPAL

def jugar(depth=5, turnos_max=100, modo="pc-pc"):
    raton, gato, puerta = posiciones_iniciales()
    tablero = crear_tablero()
    turno_gato = False
    turno = 0

    while turno < turnos_max:
        limpiar_tablero(tablero)
        poner(tablero, puerta, 'P')
        poner(tablero, raton, 'R')
        poner(tablero, gato, 'G')
        mostrar(tablero)

        term, win = terminal(raton, gato, puerta)
        if term:
            print("Ganó el", win)
            return win

        if turno_gato:  # Gato
            if modo == "humano-gato":
                print("Tu turno (GATO)")
                gato = pedir_movimiento_wasd(gato)
            else:
                gato = mejor_mov_gato(raton, gato, puerta, depth)
        else:  # Ratón
            if modo == "humano-raton":
                print("Tu turno (RATÓN)")
                raton = pedir_movimiento_wasd(raton)
            else:
                raton = mejor_mov_raton(raton, gato, puerta, depth)

        turno_gato = not turno_gato
        turno += 1
        time.sleep(0.5)

    print("Empate por turnos.")
    return "empate"

# MENÚ

print("Elige modo de juego:")
print("1) PC vs PC")
print("2) Humano vs PC (ser GATO)")
print("3) Humano vs PC (ser RATÓN)")
op = input("Opción: ")

if op == "2":
    jugar(modo="humano-gato")
elif op == "3":
    jugar(modo="humano-raton")
else:
    jugar(modo="pc-pc")
