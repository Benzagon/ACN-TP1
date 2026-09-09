from Pasajero import Pasajero
from visualizar import dibujar, iniciar_ventana
import pygame
import sys

import numpy as np
import os
import time
import random

FILAS = 25
N_PASAJEROS = 80
ASIENTOS_VALIDOS = [0, 1, 3, 4]

P_CARRY_ON = 0.85
T_SENTADO = 3
T_CARRYON = 6

pantalla = iniciar_ventana(FILAS+1, 5)

avion = np.zeros((FILAS+2, 5), dtype=int)
avion[0][0] = -1
avion[0][1] = -1
avion[0][3] = -1
avion[0][4] = -1

random.seed(100)  

posiciones = random.sample(
    [(f, a) for f in range(1, FILAS+1) for a in ASIENTOS_VALIDOS],
    N_PASAJEROS
)

spawns = [
    (i * 20, list(pos), P_CARRY_ON, T_SENTADO, T_CARRYON)
    for i, pos in enumerate(posiciones)
]

pasajeros = []
siguiente = 0

for t in range(60 * 60):
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
        p.decidirObjetivo(avion)

    dibujar(pantalla, avion)
    pygame.time.delay(10) 