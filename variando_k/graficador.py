import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv("resumen_por_k.csv")

df = df.sort_values("K_grupos")
df["tiempo_promedio"] = df["promedio"] / 60  # a minutos

plt.figure(figsize=(10, 6))

# Línea principal
sns.lineplot(
    data=df,
    x="K_grupos",
    y="tiempo_promedio",
    marker="o",
    label="Por zona"
)

# Marcar el mínimo en K=1
k1 = df[df["K_grupos"] == 2].iloc[0]
min_tiempo = k1["tiempo_promedio"]

plt.scatter(
    k1["K_grupos"],
    min_tiempo,
    color="tab:blue",
    s=80,
    zorder=5
)

plt.annotate(
    f"(2, {min_tiempo:.2f})",
    (k1["K_grupos"], min_tiempo),
    xytext=(10, -15),
    textcoords="offset points",
    ha="left",
    color="tab:blue",
    fontweight="bold"
)

# Líneas horizontales
random =  40.76
back_to_front = 43.88

plt.axhline(y=random, color="green", linestyle="--")
plt.axhline(y=back_to_front, color="red", linestyle="--")

# Títulos sobre las líneas
plt.text(
    df["K_grupos"].max(),
    random + 0.2,
    "Promedio Random",
    color="green",
    ha="right",
    va="bottom",
    fontweight="bold"
)

plt.text(
    df["K_grupos"].max(),
    back_to_front + 0.2,
    "Promedio Back-to-front",
    color="red",
    ha="right",
    va="bottom",
    fontweight="bold"
)

plt.xlabel("K (cantidad de grupos)")
plt.ylabel("Tiempo promedio (min)")
plt.title("Tiempo promedio de embarque según K, criterio por_zona (1000 iteraciones)")

# Obtener ticks actuales y agregar los de las líneas horizontales
ax = plt.gca()
ticks = list(ax.get_yticks())

if random not in ticks:
    ticks.append(random)
if back_to_front not in ticks:
    ticks.append(back_to_front)

ticks = sorted(ticks)
ax.set_yticks(ticks)

# Resaltar los ticks correspondientes
for tick in ax.get_yticklabels():
    value = float(tick.get_text())

    if abs(value - random) < 0.01:
        tick.set_color("green")
        tick.set_fontweight("bold")

    elif abs(value - back_to_front) < 0.01:
        tick.set_color("red")
        tick.set_fontweight("bold")

plt.tight_layout()

plt.savefig(
    os.path.join(BASE_DIR, "grafico_lineas_k.jpg"),
    dpi=150
)