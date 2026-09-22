from simular import simular, Criterio
import random

FILAS = 25
N_PASAJEROS = 100
P_CARRY_ON = 0.75
T_SENTADO = 3
T_CARRYON = 6

ASIENTOS_VALIDOS = [0, 1, 3, 4]

ITERS = 1000
CRITERIO = Criterio.por_zona
VELOCIDAD = 0
VISUALIZAR = False

random.seed(100)  

tiempos = []

for i in range(ITERS):
    res = simular(FILAS, N_PASAJEROS, ASIENTOS_VALIDOS, P_CARRY_ON, T_SENTADO, T_CARRYON, VISUALIZAR, CRITERIO, VELOCIDAD=VELOCIDAD, K_grupos=2, P_DE_VACIO=0.15)
    tiempos.append(res["tiempo"])

print("-- Tiempo promedio: " + str(round((sum(tiempos)/len(tiempos) / 60), 2)) + " minutos")