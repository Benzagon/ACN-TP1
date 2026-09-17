from simular import simular, Criterio
import random

FILAS = 25
N_PASAJEROS = 100
VISUALIZAR = True
P_CARRY_ON = 0.75
T_SENTADO = 3
T_CARRYON = 9

ITERS = 1

ASIENTOS_VALIDOS = [0, 1, 3, 4]

CRITERIO = Criterio.back_to_front

random.seed(100)  

tiempos = []

for i in range(ITERS):
    res = simular(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO, T_CARRYON, VISUALIZAR, CRITERIO)
    tiempos.append(res["tiempo"])

print("-- Tiempo promedio: " + str(round((sum(tiempos)/len(tiempos) / 60), 2)) + " minutos")