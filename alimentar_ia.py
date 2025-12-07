import os
import django
import pandas as pd
import random
from datetime import datetime, timedelta

# Configurar Django para que el script pueda usar los modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ms_iascikit.settings')
django.setup()

from prediccion.models import Producto, Venta


def simular_datos_diarios():
    print("--- Iniciando transformación de datos ---")

    # 1. Leer tu CSV actual
    try:
        df = pd.read_csv('dataset_inventario.csv')
    except FileNotFoundError:
        print("ERROR: No encuentro 'dataset_inventario.csv'")
        return

    registros_creados = 0

    # 2. Recorrer cada fila del CSV (que representa 1 semana)
    for index, row in df.iterrows():
        nombre_producto = row['producto']
        ventas_totales_semana = row['ventas_semana']
        semana_id = row['semana']

        # A. Asegurar que el producto existe en la BD
        producto, _ = Producto.objects.get_or_create(
            nombre=nombre_producto,
            defaults={
                'costo_base': 15.0,
                'precio_actual': 45.0,
                'stock_actual': row['inventario_final'],
                'elasticidad_precio': 1.2
            }
        )

        # B. DISTRIBUCIÓN INTELIGENTE (La clave del éxito)
        # No dividimos igual entre 7. Simulamos comportamiento real:
        # Lunes/Martes: flojo (10%)
        # Miércoles: normal (12%)
        # Jueves: sube (15%)
        # Viernes/Sábado: explota (20% cada uno)
        # Domingo: baja un poco (13%)
        pesos_semanales = [0.10, 0.10, 0.12, 0.15, 0.20, 0.20, 0.13]

        # Fecha base ficticia (para que la IA tenga historial antiguo)
        # Asumimos que la semana 1 fue hace 20 semanas
        fecha_base = datetime.now() - timedelta(weeks=(25 - semana_id))

        for dia_idx, peso in enumerate(pesos_semanales):
            # Calculamos venta del día según el peso + un factor aleatorio (ruido)
            venta_base = ventas_totales_semana * peso
            variacion = random.uniform(0.8, 1.2)  # +/- 20% de aleatoriedad
            cantidad_final = int(venta_base * variacion)

            if cantidad_final > 0:
                # Simulamos Hora Pico vs Hora Valle
                es_pico = random.choice([True, False]) if dia_idx >= 4 else False  # Fines de semana más horas pico

                # Simulamos clima (Viernes lluviosos venden más a domicilio, etc.)
                clima = random.choice(["Soleado", "Nublado", "Lluvia"])

                Venta.objects.create(
                    producto=producto,
                    cantidad=cantidad_final,
                    dia_semana=dia_idx,  # 0=Lunes
                    es_hora_pico=es_pico,
                    clima=clima
                    # Nota: 'fecha' se pondrá como "ahora" automáticamente por auto_now_add
                    # Si quieres fechas históricas reales, necesitas quitar auto_now_add del modelo temporalmente
                    # o usar un update posterior. Para la IA básica, el dia_semana es lo más importante.
                )
                registros_creados += 1

    print(f"✅ ¡Listo! Convertimos tus datos semanales en {registros_creados} registros de ventas diarias detalladas.")
    print("Ahora tu IA podrá detectar patrones como 'Los viernes se vende más'.")


if __name__ == '__main__':
    simular_datos_diarios()
