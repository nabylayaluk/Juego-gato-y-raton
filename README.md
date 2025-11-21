# Gato y Ratón - Juego en Python 🐭🐱
## Qué creé

Un juego de tablero 8x8 donde un ratón intenta llegar a una puerta mientras un gato lo persigue.
Se puede jugar PC vs PC o Humano vs PC, con movimientos en 8 direcciones para el jugador.

## Qué funcionó

La lógica del tablero y los movimientos básicos funcionaron perfectamente.

Minimax permite que el gato y el ratón tomen decisiones “inteligentes” en la versión PC vs PC.

Los controles WASD + diagonales para el jugador son intuitivos y evitan errores de entrada.

## Qué fue un desastre

Sin poda alfa-beta, el minimax se vuelve muy lento si aumentás demasiado la profundidad.

A veces el gato no atrapaba al ratón como esperaba, sobre todo con profundidades bajas, lo que generaba movimientos raros.

## Mi mejor “¡ajá!”

Descubrí que usar distancia Manhattan como heurística simplifica mucho la evaluación de posiciones y funciona perfecto para un tablero cuadrado, me da el aproximado ideal sin complicaciones.

También el truco de turno_gato = not turno_gato fue un “¡ajá!” genial para alternar turnos sin ifs complicados.
