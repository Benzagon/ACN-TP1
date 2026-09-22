import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar ambos archivos
df_sin = pd.read_csv(os.path.join(BASE_DIR, "tiemposSinPriority.csv"))
df_con = pd.read_csv(os.path.join(BASE_DIR, "tiemposPriority.csv"))

# Pasar a formato largo y etiquetar el origen
datos_sin = df_sin.melt(var_name="criterio", value_name="tiempo")
datos_sin["priority"] = "Sin Priority"

datos_con = df_con.melt(var_name="criterio", value_name="tiempo")
datos_con["priority"] = "Con Priority"

# Unir todo
datos = pd.concat([datos_sin, datos_con], ignore_index=True)
datos["tiempo"] = datos["tiempo"] / 60  # a minutos

# Filtrar solo los criterios que nos interesan (steffen y por_zona)
datos = datos[datos["criterio"].isin(["steffen", "por_zona"])]

# Aclarar K=2 en por_zona
datos["criterio"] = datos["criterio"].replace({"por_zona": "por_zona (K=2)"})

plt.figure(figsize=(8, 6))
sns.boxplot(data=datos, x="criterio", y="tiempo", hue="priority", width=0.5)
plt.xlabel("Criterio")
plt.ylabel("Tiempo (min)")
plt.title("Tiempo de embarque por criterio con y sin 10 pasajes de priority boarding")
plt.xticks(rotation=30, ha="right")
plt.legend(title="")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "grafico_boxplot_priority_p75.jpg"), dpi=150)