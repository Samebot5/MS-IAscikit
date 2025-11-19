import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Cargar CSV
df = pd.read_csv("dataset_inventario.csv")

# Convertir booleanos a 0/1
df["reabastecio"] = df["reabastecio"].astype(int)

# Variables de entrada para el modelo
X = df[["ventas_semana", "inventario_inicial"]]
y = df["reabastecio"]

# Entrenar
model = DecisionTreeClassifier()
model.fit(X, y)

# Guardar modelo entrenado
joblib.dump(model, "modelo_inventario.pkl")

print("Modelo entrenado y guardado")