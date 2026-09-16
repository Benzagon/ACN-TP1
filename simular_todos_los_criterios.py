from simular import simular, Criterio
import random
import statistics
import csv

resultados_por_criterio = {}

def correr_experimento(criterio, iters, seed=100):
    random.seed(seed)
    metricas = {}
    for i in range(iters):
        res = simular(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO, T_CARRYON, VISUALIZAR, criterio)
        for key, valor in res.items():
            if isinstance(valor, (int, float)):
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
    }
    resultados_por_criterio[criterio] = resumen
    return resumen


def imprimir_resumen(criterio, resumen, n):
    t = resumen["tiempo"]
    print(f"== {criterio.name} N={n} ==")
    print(f"  Promedio: {t['promedio']/60:.2f} min")
    print(f"  Desvío estándar: {t['desvio_std']/60:.2f} min")
    print(f"  Mín: {t['min']/60:.2f} min | Máx: {t['max']/60:.2f} min | Mediana: {t['mediana']/60:.2f} min")

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


FILAS = 25
N_PASAJEROS = 100
VISUALIZAR = False
P_CARRY_ON = 1
T_SENTADO = 3
T_CARRYON = 9

ITERS = 200

ASIENTOS_VALIDOS = [0, 1, 3, 4]

for criterio in Criterio:
    resumen = correr_experimento(criterio, ITERS)
    imprimir_resumen(criterio, resumen, ITERS)

guardar_csv(resultados_por_criterio)