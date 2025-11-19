import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# ==== RUTA BASE DEL PROYECTO ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # carpeta prediccion/

# ==== RUTA DEL CSV ====
csv_path = os.path.join(BASE_DIR, "dataset_inventario.csv")

print(f"Usando dataset: {csv_path}")

# Cargar dataset
df = pd.read_csv(csv_path)

# Convertir reabastecio a entero (True=1, False=0)
df["reabastecio"] = df["reabastecio"].astype(int)

# Corrección automática:
# si inventario inicial es 0, entonces obligatoriamente debe reabastecer
df.loc[df["inventario_inicial"] <= 0, "reabastecio"] = 1

# Variables del modelo
X = df[["ventas_semana", "inventario_inicial"]]
y = df["reabastecio"]

# Entrenar modelo
model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

# Guardar modelo en la misma carpeta
model_path = os.path.join(BASE_DIR, "modelo_inventario.pkl")
joblib.dump(model, model_path)

print("Modelo entrenado correctamente y guardado en:")
print(model_path)
