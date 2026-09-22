import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar ambos archivos
df_sin = pd.read_csv(os.path.join(BASE_DIR, "tiemposSinPriority.csv"))
df_con = pd.read_csv(os.path.join(BASE_DIR, "tiemposPriority.csv"))

criterios = ["steffen", "por_zona"]

print("Tiempos promedio (en minutos)\n" + "-" * 35)

for criterio in criterios:
    prom_sin = df_sin[criterio].mean() / 60
    prom_con = df_con[criterio].mean() / 60
    print(f"\n{criterio}:")
    print(f"  Sin Priority: {prom_sin:.2f} min")
    print(f"  Con Priority: {prom_con:.2f} min")
    print(f"  Diferencia:   {prom_con - prom_sin:+.2f} min")