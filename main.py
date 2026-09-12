from Pasajero import Pasajero, Estado
from visualizar import dibujar, iniciar_ventana
from posiciones import *

import pygame
import sys

import numpy as np
import random

FILAS = 25
N_PASAJEROS = 100
ASIENTOS_VALIDOS = [0, 1, 3, 4]

P_CARRY_ON = 0.75
T_SENTADO = 3
T_CARRYON = 9

ITERS = 100

random.seed(100)  

tiempos = []

for i in range(100):

    pantalla = iniciar_ventana(FILAS+1, 5)

    avion = np.zeros((FILAS+2, 5), dtype=int)
    avion[0][0] = -1
    avion[0][1] = -1
    avion[0][3] = -1
    avion[0][4] = -1

    posiciones = posiciones_random(FILAS, ASIENTOS_VALIDOS, N_PASAJEROS)

    pasajeros = []
    siguiente = 0

    sentados = 0
    tiempo = 0

    while tiempo <= (60 * 60) and sentados < N_PASAJEROS:
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

        # dibujar(pantalla, avion)
        # pygame.time.delay(0) 
        tiempo += 1
    tiempos.append(tiempo)
print("-- Tiempo total: " + str(round((sum(tiempos)/len(tiempos) / 60), 2)) + " minutos")