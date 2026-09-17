from simular import simular, Criterio
import random
import statistics
import csv

CRITERIOS = [
    Criterio.random,
    Criterio.por_zona,
    Criterio.back_to_front,
    Criterio.wilma_random,
    Criterio.wilma_back_to_front,
    Criterio.steffen
]

VALORES_P = [round(i / 10, 1) for i in range(11)]  # 0.0, 0.1, ..., 1.0

resultados_por_criterio_y_p = {}  # {criterio: {p: promedio}}


def correr_experimento(criterio, p_carry_on, iters, seed=100):
    random.seed(seed)
    tiempos = []
    for i in range(iters):
        res = simular(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, p_carry_on, T_SENTADO, T_CARRYON, VISUALIZAR, criterio)
        tiempos.append(res["tiempo"])

    return {
        "valores": tiempos,
        "promedio": statistics.mean(tiempos),
        "desvio_std": statistics.stdev(tiempos) if len(tiempos) > 1 else 0.0,
        "min": min(tiempos),
        "max": max(tiempos),
        "mediana": statistics.median(tiempos),
    }


def imprimir_resumen(criterio, p, resumen, n):
    print(f"== {criterio.name} P={p} N={n} ==")
    print(f"  Promedio: {resumen['promedio']/60:.2f} min")
    print(f"  Desvío estándar: {resumen['desvio_std']/60:.2f} min")


def guardar_csv(resultados, path="promedios_por_p.csv"):
    nombres = [criterio.name for criterio in resultados]

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["p"] + nombres)
        for p in VALORES_P:
            fila = [p] + [resultados[criterio][p]["promedio"] for criterio in resultados]
            writer.writerow(fila)


FILAS = 25
N_PASAJEROS = 100
VISUALIZAR = False
T_SENTADO = 3
T_CARRYON = 9

ITERS = 200

ASIENTOS_VALIDOS = [0, 1, 3, 4]

for criterio in CRITERIOS:
    resultados_por_criterio_y_p[criterio] = {}
    for p in VALORES_P:
        resumen = correr_experimento(criterio, p, ITERS)
        resultados_por_criterio_y_p[criterio][p] = resumen
        imprimir_resumen(criterio, p, resumen, ITERS)

guardar_csv(resultados_por_criterio_y_p)