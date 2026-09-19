import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(BASE_DIR, "tiempos_promedio_sentado.csv"))
datos = df.melt(var_name="criterio", value_name="tiempo")
datos["tiempo"] = datos["tiempo"] / 60  # a minutos

resumen = datos.groupby("criterio")["tiempo"].agg(["min", "max"]).reset_index()
resumen = resumen.sort_values("max", ascending=False)

plt.figure(figsize=(12, 6))
y_pos = range(len(resumen))

plt.hlines(y=y_pos, xmin=resumen["min"], xmax=resumen["max"], color="gray", alpha=0.6, zorder=1)
plt.scatter(resumen["min"], y_pos, color="tab:blue", label="Mínimo", zorder=3)
plt.scatter(resumen["max"], y_pos, color="tab:red", label="Máximo", zorder=3)

for x, y in zip(resumen["min"], y_pos):
    plt.annotate(f"{x:.1f}", (x, y), textcoords="offset points", xytext=(-5, 5),
                 ha="right", fontsize=9, color="tab:blue")
for x, y in zip(resumen["max"], y_pos):
    plt.annotate(f"{x:.1f}", (x, y), textcoords="offset points", xytext=(5, 5),
                 ha="left", fontsize=9, color="tab:red")

plt.yticks(y_pos, resumen["criterio"])
plt.xlabel("Tiempo (min)")
plt.ylabel("Criterio")
plt.title("Rango (mín–máx) del tiempo de espera hasta sentarse por criterio (N=1000)")

ax = plt.gca()
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax.grid(axis="x", linestyle="--", alpha=0.4, zorder=0)
margen = (resumen["max"].max() - resumen["min"].min()) * 0.1
plt.xlim(resumen["min"].min() - margen, resumen["max"].max() + margen)

plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "grafico_rango_minmax_p75.jpg"), dpi=150)