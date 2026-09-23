from simular import simular, Criterio
import random
import statistics

def fmt(segundos):
    m, s = divmod(round(segundos), 60)
    return f"{m}m {s}s"

FILAS = 25
N_PASAJEROS = 100
P_CARRY_ON = 0.75
P_DE_VACIO = 0
T_SENTADO = 3
T_CARRYON = 6

ASIENTOS_VALIDOS = [0, 1, 3, 4]

ITERS = 1
CRITERIO = Criterio.por_zona
VELOCIDAD = 10
VISUALIZAR = True

random.seed(100)  

tiempos = []

print("== Método " + str(CRITERIO) + " cantidad de iteraciones N=" + str(ITERS) + " ==")

for i in range(ITERS):
    res = simular(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO, T_CARRYON, VISUALIZAR, CRITERIO, VELOCIDAD=VELOCIDAD, K_grupos=2, P_DE_VACIO=P_DE_VACIO)
    tiempos.append(res["tiempo"])

n = ITERS
promedio = sum(tiempos) / n

print("-- Tiempo promedio: " + fmt(promedio))

if ITERS > 1:
    desvio = statistics.stdev(tiempos)
    error = desvio / (n ** 0.5)
    print("-- Desvío estándar: " + fmt(desvio))
    print("-- Error estándar: " + fmt(error))