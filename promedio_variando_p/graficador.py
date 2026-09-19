import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(BASE_DIR, "promedios_por_p_75.csv"))

datos = df.melt(id_vars="p", var_name="criterio", value_name="tiempo_promedio")
datos["tiempo_promedio"] = datos["tiempo_promedio"] / 60  # a minutos

plt.figure(figsize=(10, 6))
sns.lineplot(data=datos, x="p", y="tiempo_promedio", hue="criterio", marker="o")
plt.xlabel("P (probabilidad de carry-on)")
plt.ylabel("Tiempo promedio (min)")
plt.title("Tiempo promedio de embarque según P, por criterio")
plt.legend(title="Criterio")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "grafico_lineas_p.jpg"), dpi=150)