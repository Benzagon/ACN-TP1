import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

archivos = {
    "p0": "tiempos_p0.csv",
    "p25": "tiempos_p25.csv",
    "p50": "tiempos_p50.csv",
    "p75": "tiempos_p75.csv",
    "p100": "tiempos_p100.csv",
}

filas = []
for p, path in archivos.items():
    df = pd.read_csv(os.path.join(BASE_DIR, path))
    promedios = df.mean(numeric_only=True)  # promedio por columna (criterio)
    for criterio, promedio in promedios.items():
        filas.append({"criterio": criterio, "p": p, "tiempo_promedio": promedio / 60})  # a minutos

datos = pd.DataFrame(filas)

fig, axes = plt.subplots(1, len(archivos), figsize=(24, 6), sharey=True)

for ax, p in zip(axes, archivos.keys()):
    subset = datos[datos["p"] == p]
    sns.barplot(data=subset, x="criterio", y="tiempo_promedio", ax=ax)
    ax.set_title(p)
    ax.set_xlabel("Criterio")
    ax.set_ylabel("Tiempo promedio (min)" if ax is axes[0] else "")
    ax.tick_params(axis="x", rotation=30)
    for label in ax.get_xticklabels():
        label.set_ha("right")

fig.suptitle("Tiempo promedio de embarque por criterio, según % de carry-on")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "grafico.jpg"), dpi=150)