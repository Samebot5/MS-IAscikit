import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from inventario.models import VentaSemanal

# Extraer datos desde Django
qs = VentaSemanal.objects.all().values()
df = pd.DataFrame(qs)

# Asegurar que el campo esté como 0/1
df["reabastecio"] = df["reabastecio"].astype(int)

# --- Corrección automática del dataset ---
# Si el inventario inicial es 0 → es obvio que sí reabasteció
df.loc[df["inventario_inicial"] <= 0, "reabastecio"] = 1

# Variables de entrada
X = df[["ventas_semana", "inventario_inicial"]]
y = df["reabastecio"]

# Entrenar modelo mejorado
model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

joblib.dump(model, "modelo_inventario.pkl")

print("Modelo entrenado correctamente")
