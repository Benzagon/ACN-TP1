from Pasajero import Pasajero, Estado
from visualizar import dibujar, iniciar_ventana
from posiciones import *
from enum import Enum, auto

import pygame
import sys

import numpy as np
import random

class Criterio(Enum):
    random = auto()
    por_zona = auto()
    back_to_front = auto()
    wilma_por_grupos = auto()
    wilma_random = auto()
    wilma_back_to_front = auto()
    steffen = auto()

def simular(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO, T_CARRYON, VISUALIZAR, criterio):
    K = 5
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

    if VISUALIZAR:
        pantalla = iniciar_ventana(FILAS+1, 5)

    avion = np.zeros((FILAS+2, 5), dtype=int)
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
            pygame.time.delay(5) 
        tiempo += 1
    res = {"tiempo": tiempo}
    return res