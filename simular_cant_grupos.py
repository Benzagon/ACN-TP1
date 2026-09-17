from simular import simular, Criterio
import random
import statistics
import csv

resultados_por_k = {}

def correr_experimento(criterio, k_grupos, iters):
    metricas = {}
    for i in range(iters):
        res = simular(
            FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON,
            T_SENTADO, T_CARRYON, VISUALIZAR, criterio,
            K_grupos=k_grupos,   # <- ajustar si simular() lo espera posicional
        )
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
    resultados_por_k[k_grupos] = resumen
    return resumen


def imprimir_resumen(k_grupos, resumen, n):
    t = resumen["tiempo"]
    print(f"== K={k_grupos} N={n} ==")
    print(f"  Promedio: {t['promedio']/60:.2f} min")
    print(f"  Desvío estándar: {t['desvio_std']/60:.2f} min")
    print(f"  Mín: {t['min']/60:.2f} min | Máx: {t['max']/60:.2f} min | Mediana: {t['mediana']/60:.2f} min")


def guardar_csv_valores(resultados, path="tiempos_por_k.csv"):
    """Guarda todos los valores crudos, una columna por K (útil para graficar distribuciones)."""
    ks = sorted(resultados.keys(), reverse=True)
    columnas = [resultados[k]["tiempo"]["valores"] for k in ks]
    max_len = max(len(c) for c in columnas)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"K={k}" for k in ks])
        for fila in range(max_len):
            writer.writerow([col[fila] if fila < len(col) else "" for col in columnas])


def guardar_csv_resumen(resultados, path="resumen_por_k.csv"):
    """Guarda una fila por K con las métricas agregadas (lo que probablemente querés para el gráfico K vs tiempo)."""
    ks = sorted(resultados.keys(), reverse=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["K_grupos", "promedio", "desvio_std", "min", "max", "mediana"])
        for k in ks:
            t = resultados[k]["tiempo"]
            writer.writerow([k, t["promedio"], t["desvio_std"], t["min"], t["max"], t["mediana"]])


FILAS = 25
N_PASAJEROS = 100
VISUALIZAR = False
P_CARRY_ON = 0.75
T_SENTADO = 3
T_CARRYON = 9

ITERS = 1000


ASIENTOS_VALIDOS = [0, 1, 3, 4]
random.seed(100)

for k in range(1, 26, 1):
    resumen = correr_experimento(Criterio.por_zona, k, ITERS)
    imprimir_resumen(k, resumen, ITERS)

guardar_csv_valores(resultados_por_k)
guardar_csv_resumen(resultados_por_k)