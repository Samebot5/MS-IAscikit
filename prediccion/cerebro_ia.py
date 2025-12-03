import joblib
import os
import pandas as pd
from django.conf import settings
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans


class CerebroPrediccion:
    def __init__(self):
        # 1. Definimos rutas para DOS cerebros distintos
        self.ruta_ventas = os.path.join(settings.BASE_DIR, 'modelo_ventas.pkl')
        self.ruta_clientes = os.path.join(settings.BASE_DIR, 'modelo_clientes.pkl')

        self.modelo_ventas = None
        self.modelo_clientes = None

        # 2. Intentamos cargar la memoria de VENTAS
        if os.path.exists(self.ruta_ventas):
            try:
                self.modelo_ventas = joblib.load(self.ruta_ventas)
                print(f"✅ IA: Modelo de Ventas cargado.")
            except:
                print("⚠️ IA: Error cargando modelo ventas.")

        # 3. Intentamos cargar la memoria de CLIENTES
        if os.path.exists(self.ruta_clientes):
            try:
                self.modelo_clientes = joblib.load(self.ruta_clientes)
                print(f"✅ IA: Modelo de Clientes cargado.")
            except:
                print("⚠️ IA: Error cargando modelo clientes.")

    def entrenar_todo(self):
        """Método maestro para entrenar ambas IAs de golpe"""
        res_ventas = self.entrenar_prediccion_ventas()
        res_clientes = self.segmentar_clientes_vip()
        return f"{res_ventas} | {res_clientes}"

    def entrenar_prediccion_ventas(self):
        from .models import Venta  # Importamos aquí para evitar errores circulares
        print("🧠 Entrenando predicción de ventas...")

        datos = list(Venta.objects.all().values('dia_semana', 'producto_id', 'cantidad'))
        df = pd.DataFrame(datos)

        if df.empty: return "❌ Sin datos de ventas para entrenar"

        X = df[['dia_semana', 'producto_id']]
        y = df['cantidad']

        nuevo_modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        nuevo_modelo.fit(X, y)

        # Guardamos en disco
        joblib.dump(nuevo_modelo, self.ruta_ventas)
        self.modelo_ventas = nuevo_modelo
        return "✅ Ventas entrenado"

    def segmentar_clientes_vip(self):
        from .models import Cliente  # Importamos aquí
        print("🧠 Segmentando clientes...")

        # Obtenemos solo clientes que hayan comprado algo
        datos = list(Cliente.objects.filter(total_gastado__gt=0).values('id', 'total_gastado', 'frecuencia_visitas'))
        df = pd.DataFrame(datos)

        if df.empty or len(df) < 3:
            # KMeans necesita al menos tantos datos como clusters (3)
            return "⚠️ Muy pocos clientes para segmentar (se necesitan mín. 3)"

        # Entrenamos KMeans (3 grupos: Bronce, Plata, Oro)
        kmeans = KMeans(n_clusters=3, random_state=42)
        # Usamos doble corchete para asegurar formato 2D
        kmeans.fit(df[['total_gastado', 'frecuencia_visitas']])

        # Guardamos el modelo
        joblib.dump(kmeans, self.ruta_clientes)
        self.modelo_clientes = kmeans

        # ACTUALIZAMOS LA BASE DE DATOS
        # Asignamos a cada cliente su etiqueta (0, 1 o 2)
        df['cluster'] = kmeans.labels_

        # Lógica para saber cuál cluster es el "VIP" (el que gasta más)
        # Calculamos el promedio de gasto por cluster
        promedios = df.groupby('cluster')['total_gastado'].mean().sort_values()
        # Mapeamos: el cluster con menor promedio será 0 (Bronce), el mayor será 2 (Oro/VIP)
        mapa_vip = {cluster_id: i for i, cluster_id in enumerate(promedios.index)}

        count = 0
        for index, row in df.iterrows():
            cluster_original = row['cluster']
            nivel_vip = mapa_vip[cluster_original]  # 0, 1 o 2 ordenado por valor

            Cliente.objects.filter(id=row['id']).update(cluster_ia=nivel_vip)
            count += 1

        return f"✅ {count} Clientes segmentados"

    def predecir_demanda_mañana(self, producto_id, dia_mañana):
        if self.modelo_ventas is None:
            return 15  # Valor por defecto si no está entrenado

        try:
            pred = self.modelo_ventas.predict([[dia_mañana, producto_id]])[0]
            return max(0, pred)
        except:
            return 10