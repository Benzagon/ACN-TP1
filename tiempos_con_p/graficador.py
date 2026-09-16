import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("GOLA")


archivos = {
    "p0": "tiempos_p0.csv",
    "p25": "tiempos_p25.csv",
    "p50": "tiempos_p50.csv",
    "p75": "tiempos_p75.csv",
    "p100": "tiempos_p100.csv",
}

filas = []
for p, path in archivos.items():
    df = pd.read_csv(path)
    promedios = df.mean()  # promedio por columna (criterio)
    for criterio, promedio in promedios.items():
        filas.append({"criterio": criterio, "p": p, "tiempo_promedio": promedio / 60})  # a minutos

datos = pd.DataFrame(filas)

plt.figure(figsize=(12, 6))
sns.barplot(data=datos, x="criterio", y="tiempo_promedio", hue="p")
plt.xlabel("Criterio")
plt.ylabel("Tiempo promedio (min)")
plt.title("Tiempo promedio de embarque por criterio y % de carry-on")
plt.xticks(rotation=30, ha="right")
plt.legend(title="P carry-on")
plt.tight_layout()
plt.savefig("grafico.jpg")