"""
simularVIDEOS.py

Corre 5 simulaciones de boarding EN PARALELO, cada una en su propia
ventana de pygame, para grabar un video comparativo de los criterios.

Cómo resuelve los dos problemas anteriores:

1) "la ventana se resetea de posición cuando arranca la simulación"
   -> Esto pasaba porque simular() (en simular.py) llama a
      iniciar_ventana() de nuevo internamente, lo que recrea/reubica
      la ventana. Acá definimos SIMULAR_SIN_RESET, una copia de esa
      función que NO vuelve a llamar a iniciar_ventana(): reutiliza la
      misma ventana que ya abrimos y que vos ya acomodaste a mano.

2) "no arrancan todos a la vez"
   -> Cada ventana abre en momentos distintos (según STAGGER) y hace
      su propia pausa (PAUSA_SEGUNDOS) para que la acomodes. Para que
      las 5 simulaciones arranquen sincronizadas en el mismo instante
      (aunque hayan abierto en momentos distintos), usamos una
      multiprocessing.Barrier: cada proceso, al terminar SU pausa,
      espera ahí hasta que los otros 4 también terminen la suya, y
      recién ahí arrancan las 5 juntas.

Flujo por cada criterio:
  1. Se abre la ventana (vacía).
  2. Cuenta regresiva de PAUSA_SEGUNDOS en el título — tu tiempo para
     arrastrarla a donde quieras.
  3. Espera (barrera) a que las otras 4 ventanas también hayan
     terminado su pausa.
  4. Arrancan las 5 simulaciones a la vez.
  5. Al terminar, la ventana queda abierta hasta que la cierres a mano.
"""

import os
import time
import random
import multiprocessing as mp

# ---------------- Parámetros de la simulación (iguales a main.py) ----------------
FILAS = 25
N_PASAJEROS = 100
P_CARRY_ON = 0.75
T_SENTADO = 3
T_CARRYON = 6
ASIENTOS_VALIDOS = [0, 1, 3, 4]
VELOCIDAD = 10
SEED = 100
K_GRUPOS = 2

# Nombres del enum Criterio (se resuelven adentro de cada proceso hijo,
# para no tener que importar simular.py -> visualizar.py a nivel de módulo)
CRITERIOS = ["random", "por_zona", "back_to_front", "wilma_random", "steffen"]

# ---------------- Timing ----------------
PAUSA_SEGUNDOS = 60   # tiempo con la ventana abierta y quieta para que la acomodes a mano
STAGGER = 10          # segundos entre la apertura de cada ventana

# Posición inicial "de arranque" (solo un intento; si tu SO la ignora, no pasa
# nada, para eso está la pausa + el acomodo manual)
WIN_W = 260
MARGEN_X = 10
POS_Y = 40


def simular_sin_reset(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO,
                       T_CARRYON, VISUALIZAR, criterio, pantalla, K_grupos=2, VELOCIDAD=0):
    """
    Copia de simular() (simular.py) que recibe la `pantalla` ya creada
    en vez de llamar a iniciar_ventana() de nuevo, para que la ventana
    no cambie de posición al arrancar. El resto de la lógica es
    idéntica a la original.
    """
    import sys
    import pygame
    import numpy as np
    from Pasajero import Pasajero, Estado
    from visualizar import dibujar
    from posiciones import posiciones_por_zona, posiciones_random, posiciones_por_WILMA_random, posiciones_por_WILMA_por_grupos, posiciones_steffen2, posiciones_por_WILMA_back_to_front
    from simular import Criterio

    K = K_grupos
    posiciones = []
    if criterio == Criterio.random:
        posiciones = posiciones_random(FILAS, ASIENTOS_VALIDOS, N_PASAJEROS)
    elif criterio == Criterio.por_zona:
        posiciones = posiciones_por_zona(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, K)
    elif criterio == Criterio.back_to_front:
        posiciones = posiciones_por_zona(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, K=FILAS)
    elif criterio == Criterio.wilma_por_grupos:
        posiciones = posiciones_por_WILMA_por_grupos(FILAS, N_PASAJEROS, K)
    elif criterio == Criterio.wilma_random:
        posiciones = posiciones_por_WILMA_random(FILAS, N_PASAJEROS)
    elif criterio == Criterio.wilma_back_to_front:
        posiciones = posiciones_por_WILMA_back_to_front(FILAS, N_PASAJEROS)
    elif criterio == Criterio.steffen:
        posiciones = posiciones_steffen2(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS)
    else:
        raise ValueError(f"Criterio no soportado: {criterio}")

    pasajeros = []
    siguiente = 0
    sentados = 0
    tiempo = 0

    avion = np.zeros((FILAS + 2, 5), dtype=int)
    avion[0][0] = -1
    avion[0][1] = -1
    avion[0][3] = -1
    avion[0][4] = -1

    while tiempo <= (60 * 60) and sentados < N_PASAJEROS:
        if VISUALIZAR:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if siguiente < N_PASAJEROS and avion[0][2] == 0:
            objetivo = list(posiciones[siguiente])
            nuevo = Pasajero(objetivo, avion, P_CARRY_ON, T_SENTADO, T_CARRYON)
            pasajeros.append(nuevo)
            siguiente += 1

        for p in pasajeros:
            if p.estado != Estado.SENTADO:
                p.decidirObjetivo(avion)
                sentados += p.estado == Estado.SENTADO

        if VISUALIZAR:
            dibujar(pantalla, avion)
            pygame.time.delay(VELOCIDAD)
        tiempo += 1

    return {"tiempo": tiempo}


def correr_uno(criterio_nombre: str, pos_x: int, pos_y: int, queue: mp.Queue, barrera: mp.Barrier):
    """Target de cada proceso: abre la ventana, hace una pausa para
    poder acomodarla a mano, espera a que los demás también estén
    listos (barrera), corre la simulación (sin resetear la ventana) y
    la deja abierta al final."""
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{pos_x},{pos_y}"
    os.environ["SDL_VIDEO_CENTERED"] = "0"

    import pygame
    from visualizar import iniciar_ventana
    from simular import Criterio

    criterio = getattr(Criterio, criterio_nombre)

    # Abrimos la ventana UNA sola vez; nunca más se vuelve a crear
    pantalla = iniciar_ventana(FILAS + 1, 5)

    # ---- Pausa individual: acá podés arrastrar la ventana ----
    restante = PAUSA_SEGUNDOS
    ultimo_tick = time.time()
    pygame.display.set_caption(f"{criterio_nombre} - moveme, arranca en {restante}s")
    cerrado = False
    while restante > 0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                cerrado = True
        if cerrado:
            break
        ahora = time.time()
        if ahora - ultimo_tick >= 1:
            restante -= 1
            ultimo_tick = ahora
            pygame.display.set_caption(f"{criterio_nombre} - moveme, arranca en {restante}s")
        pygame.time.delay(50)

    if cerrado:
        # Si cerraste esta ventana durante la pausa, no dejamos a las
        # otras 4 esperando para siempre en la barrera.
        try:
            barrera.abort()
        except Exception:
            pass
        pygame.quit()
        return

    # ---- Esperar a que las otras ventanas también terminen su pausa ----
    pygame.display.set_caption(f"{criterio_nombre} - listo, esperando al resto...")
    try:
        barrera.wait()
    except Exception:
        # Si algún otro proceso abortó la barrera (cerró su ventana), salimos también
        pygame.quit()
        return

    # ---- Arrancan las 5 simulaciones a la vez ----
    pygame.display.set_caption(f"{criterio_nombre} - corriendo...")
    random.seed(SEED)

    res = simular_sin_reset(
        FILAS,
        N_PASAJEROS,
        ASIENTOS_VALIDOS,
        P_CARRY_ON,
        T_SENTADO,
        T_CARRYON,
        True,          # VISUALIZAR
        criterio,
        pantalla,
        K_grupos=K_GRUPOS,
        VELOCIDAD=VELOCIDAD,
    )

    queue.put((criterio_nombre, res["tiempo"]))
    pygame.display.set_caption(f"{criterio_nombre} - terminado ({round(res['tiempo']/60, 2)} min)")

    # Mantener la ventana abierta hasta que el usuario la cierre a mano
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
        pygame.time.delay(100)

    pygame.quit()


def main():
    ctx = mp.get_context("spawn")  # más confiable para procesos con pygame
    queue = ctx.Queue()
    barrera = ctx.Barrier(len(CRITERIOS))

    procesos = []
    for i, criterio_nombre in enumerate(CRITERIOS):
        pos_x = MARGEN_X + i * (WIN_W + MARGEN_X)
        p = ctx.Process(target=correr_uno, args=(criterio_nombre, pos_x, POS_Y, queue, barrera))
        procesos.append(p)

    print(f"Lanzando {len(procesos)} ventanas (cada una con {PAUSA_SEGUNDOS}s para acomodarla). "
          f"Las 5 simulaciones arrancan juntas recién cuando todas terminaron su pausa.")
    for p in procesos:
        p.start()
        time.sleep(STAGGER)

    for p in procesos:
        p.join()

    print("\n-- Resultados --")
    while not queue.empty():
        nombre, tiempo = queue.get()
        print(f"{nombre}: {round(tiempo / 60, 2)} minutos")

    print("\nTodas las ventanas quedaron abiertas: cerralas a mano cuando termines de grabar.")


if __name__ == "__main__":
    main()