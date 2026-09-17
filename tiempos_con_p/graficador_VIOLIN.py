import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(BASE_DIR, "tiempos_p75_limpio.csv"))
datos = df.melt(var_name="criterio", value_name="tiempo")
datos["tiempo"] = datos["tiempo"] / 60  # a minutos

plt.figure(figsize=(12, 6))
sns.violinplot(data=datos, x="criterio", y="tiempo")
plt.xlabel("Criterio")
plt.ylabel("Tiempo (min)")
plt.title("Distribución del tiempo de embarque por criterio (P=75)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "grafico_violin_p75.jpg"), dpi=150)