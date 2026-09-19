from Pasajero import Pasajero, Estado
from visualizar import dibujar, iniciar_ventana
from posiciones import *
from enum import Enum, auto

from simular import simular, Criterio
import random
import statistics
import csv


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

def simular_tiempos(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO, T_CARRYON, VISUALIZAR, criterio, K_grupos=2, VELOCIDAD=0):
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

    tiempo_entrada = {}
    tiempo_sentado = {}

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
            tiempo_entrada[len(pasajeros) - 1] = tiempo
            siguiente += 1

        for i, p in enumerate(pasajeros):
            if p.estado != Estado.SENTADO:
                p.decidirObjetivo(avion)
                if p.estado == Estado.SENTADO:
                    tiempo_sentado[i] = tiempo
                    sentados += 1

        if VISUALIZAR:
            dibujar(pantalla, avion)
            pygame.time.delay(VELOCIDAD)
        tiempo += 1

    tiempos_por_pasajero = [
        (tiempo_sentado[i] - tiempo_entrada[i]) if i in tiempo_sentado else None
        for i in range(len(pasajeros))
    ]

    res = {
        "tiempo": tiempo,
        "tiempos_por_pasajero": tiempos_por_pasajero,
        "tiempo_promedio_sentado": (
            np.mean([t for t in tiempos_por_pasajero if t is not None])
            if any(t is not None for t in tiempos_por_pasajero) else None
        ),
    }
    return res

resultados_por_criterio = {}

def correr_experimento(criterio, iters, seed=100):
    random.seed(seed)
    metricas = {}
    for i in range(iters):
        res = simular_tiempos(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO, T_CARRYON, VISUALIZAR, criterio)
        for key, valor in res.items():
            if isinstance(valor, (int, float)) and valor is not None:
                metricas.setdefault(key, []).append(valor)

    resumen = {
        key: {
            "valores": valores,
            "promedio": statistics.mean(valores),
            "desvio_std": statistics.stdev(valores) if len(valores) > 1 else 0.0,
            "min": min(valores),
            "max": max(valores),
            "mediana": statistics.median(valores),
        }
        for key, valores in metricas.items()
        if valores  # por si tiempo_promedio_sentado quedó vacío en algún criterio
    }
    resultados_por_criterio[criterio] = resumen
    return resumen


def imprimir_resumen(criterio, resumen, n):
    print(f"== {criterio.name} N={n} ==")
    for key, etiqueta in [("tiempo", "Tiempo total"), ("tiempo_promedio_sentado", "Tiempo promedio hasta sentarse")]:
        if key not in resumen:
            continue
        t = resumen[key]
        print(f"  {etiqueta}:")
        print(f"    Promedio: {t['promedio']/60:.2f} min")
        print(f"    Desvío estándar: {t['desvio_std']/60:.2f} min")
        print(f"    Mín: {t['min']/60:.2f} min | Máx: {t['max']/60:.2f} min | Mediana: {t['mediana']/60:.2f} min")


def guardar_csv(resultados, path="tiempos.csv"):
    nombres = [criterio.name for criterio in resultados]
    columnas = [resultados[criterio]["tiempo"]["valores"] for criterio in resultados]
    max_len = max(len(c) for c in columnas)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(nombres)
        for fila in range(max_len):
            writer.writerow([
                col[fila] if fila < len(col) else ""
                for col in columnas
            ])


def guardar_csv_promedio_sentado(resultados, path="tiempos_promedio_sentado.csv"):
    nombres = [criterio.name for criterio in resultados if "tiempo_promedio_sentado" in resultados[criterio]]
    columnas = [
        resultados[criterio]["tiempo_promedio_sentado"]["valores"]
        for criterio in resultados
        if "tiempo_promedio_sentado" in resultados[criterio]
    ]
    max_len = max(len(c) for c in columnas)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(nombres)
        for fila in range(max_len):
            writer.writerow([
                col[fila] if fila < len(col) else ""
                for col in columnas
            ])


FILAS = 25
N_PASAJEROS = 100
VISUALIZAR = False
P_CARRY_ON = 0.75
T_SENTADO = 3
T_CARRYON = 6

ITERS = 1000

ASIENTOS_VALIDOS = [0, 1, 3, 4]

for criterio in Criterio:
    resumen = correr_experimento(criterio, ITERS)
    imprimir_resumen(criterio, resumen, ITERS)

guardar_csv(resultados_por_criterio)
guardar_csv_promedio_sentado(resultados_por_criterio)