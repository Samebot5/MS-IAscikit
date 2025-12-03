import joblib
import os
import pandas as pd
from django.conf import settings
import random

from sklearn.ensemble import RandomForestRegressor


class CerebroPrediccion:
    def __init__(self):
        self.modelo = None
        # Ruta dinámica al archivo .pkl (asumiendo que está en la raíz del proyecto)
        ruta_modelo = os.path.join(settings.BASE_DIR, 'modelo_inventario.pkl')

        try:
            self.modelo = joblib.load(ruta_modelo)
            print("IA: Modelo cargado exitosamente.")
        except FileNotFoundError:
            print(f"ADVERTENCIA: No se encontró el modelo en {ruta_modelo}")
            self.modelo = None

    def predecir_demanda_mañana(self, producto_id, dia_semana):
        """
        Predice cuántas unidades se venderán mañana.
        """
        if not self.modelo:
            return 10  # Valor por defecto si no hay modelo

        # Aquí debes adaptar los datos a como tu modelo los espera.
        # Ejemplo: Si tu modelo espera [dia_semana, producto_id]
        try:
            # Nota: El formato [[x, y]] es porque scikit espera una lista de listas
            prediccion = self.modelo.predict([[dia_semana, producto_id]])[0]
            return max(0, prediccion)  # No devolver negativos
        except Exception as e:
            print(f"Error en predicción: {e}")
            return 5  # Fallback seguro

    # Agrega este metodo dentro de tu clase CerebroPrediccion en cerebro.py

    def entrenar_modelo(self):
        print("Iniciando entrenamiento con datos de la DB...")

        # 1. Obtener datos de Django
        # Importación local para evitar errores de carga circular
        from .models import Venta

        datos = list(Venta.objects.all().values('dia_semana', 'producto_id', 'cantidad'))
        df = pd.DataFrame(datos)

        if df.empty:
            return "Error: No hay datos suficientes en la base de datos."

        # 2. Entrenar (Random Forest)
        X = df[['dia_semana', 'producto_id']]
        y = df['cantidad']

        nuevo_modelo = RandomForestRegressor(n_estimators=100)
        nuevo_modelo.fit(X, y)

        # 3. Guardar el nuevo cerebro
        self.modelo = nuevo_modelo
        joblib.dump(self.modelo, os.path.join(settings.BASE_DIR, 'modelo_inventario.pkl'))

        return "¡Modelo re-entrenado y guardado con éxito!"