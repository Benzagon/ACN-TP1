from Pasajero import Pasajero, Estado
from visualizar import dibujar, iniciar_ventana
from posiciones import *
from enum import Enum, auto

import pygame
import sys

import numpy as np
import random

def aplicar_priority_boarding(posiciones, n_priority=10):
    """Mueve n_priority pasajeros elegidos al azar al frente de la lista."""
    posiciones = list(posiciones)
    n = len(posiciones)
    n_priority = min(n_priority, n)

    indices_priority = random.sample(range(n), n_priority)
    indices_priority_set = set(indices_priority)

    prioritarios = [posiciones[i] for i in indices_priority]
    resto = [posiciones[i] for i in range(n) if i not in indices_priority_set]

    random.shuffle(prioritarios)

    return prioritarios + resto

class Criterio(Enum):
    random = auto()
    por_zona = auto()
    back_to_front = auto()
    wilma_por_grupos = auto()
    wilma_random = auto()
    wilma_back_to_front = auto()
    steffen = auto()

def simularConPriority10(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO, T_CARRYON, VISUALIZAR, criterio, K_grupos=2, VELOCIDAD=0, P_DE_VACIO=0):
    K = K_grupos
    posiciones = []
    if criterio == Criterio.random:
        posiciones = posiciones_random(FILAS, ASIENTOS_VALIDOS, N_PASAJEROS, P_DE_VACIO=P_DE_VACIO)
    elif criterio == Criterio.por_zona:
        posiciones = posiciones_por_zona(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, K, P_DE_VACIO=P_DE_VACIO)
    elif criterio == Criterio.back_to_front:
        posiciones = posiciones_por_zona(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, K=FILAS, P_DE_VACIO=P_DE_VACIO)
    elif criterio == Criterio.wilma_por_grupos:
        posiciones = posiciones_por_WILMA_por_grupos(FILAS, N_PASAJEROS, K, P_DE_VACIO=P_DE_VACIO)
    elif criterio == Criterio.wilma_random:
        posiciones = posiciones_por_WILMA_random(FILAS, N_PASAJEROS, P_DE_VACIO=P_DE_VACIO)
    elif criterio == Criterio.wilma_back_to_front:
        posiciones = posiciones_por_WILMA_back_to_front(FILAS, N_PASAJEROS, P_DE_VACIO=P_DE_VACIO)
    elif criterio == Criterio.steffen:
        posiciones = posiciones_steffen2(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_DE_VACIO=P_DE_VACIO)
    else:
        raise ValueError(f"Criterio no soportado: {criterio}")

    posiciones = aplicar_priority_boarding(posiciones)

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


    PASAJEROS_QUE_ATENDIERON = len(posiciones)
    listening_ayo = 0
    while tiempo <= (60 * 60) and (sentados + listening_ayo < PASAJEROS_QUE_ATENDIERON):
        listening_ayo = 0
        if VISUALIZAR:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if siguiente < PASAJEROS_QUE_ATENDIERON and avion[0][2] == 0:
            objetivo = list(posiciones[siguiente])
            nuevo = Pasajero(objetivo, avion, P_CARRY_ON, T_SENTADO, T_CARRYON)
            pasajeros.append(nuevo)
            siguiente += 1

        for p in pasajeros:
            if p.estado != Estado.SENTADO:
                p.decidirObjetivo(avion)
                sentados += p.estado == Estado.SENTADO
                listening_ayo += p.estado == Estado.LISTENING_AYO

        if VISUALIZAR:
            dibujar(pantalla, avion)
            pygame.time.delay(VELOCIDAD) 
        tiempo += 1
    res = {"tiempo": tiempo}
    return res

