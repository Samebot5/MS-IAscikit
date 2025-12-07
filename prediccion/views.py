from django.http import JsonResponse
from datetime import datetime
import random # Solo para simular si no hay datos históricos suficientes aún

'''# Cargar el modelo entrenado desde el archivo modelo_inventario.pkl
model = joblib.load("modelo_inventario.pkl")

# Declarar que esta función será un endpoint API que acepta solicitudes POST
@api_view(["POST"])
def predecir(request):
    # Obtener los valores enviados desde el cliente (ventas e inventario)
    # Se convierten a float por seguridad y consistencia
    ventas = float(request.data["ventas_semana"])
    inventario = float(request.data["inventario_inicial"])

    # REGLA DE NEGOCIO (no depende del modelo):
    # Si el inventario es menor o igual a 0, automáticamente debe reabastecer.
    # Esto evita predicciones incorrectas y asegura que la lógica empresarial se cumpla.
    if inventario <= 0:
        return Response({
            "reabastecer": 1,  # 1 significa "sí reabastecer"
            "mensaje": "Sí debes reabastecer (inventario agotado)"
        })

    # Hacer predicción con el modelo de Machine Learning
    # Se envían los valores como una lista dentro de una lista, ya que el modelo
    # espera una matriz de datos [[ventas, inventario]]
    pred = model.predict([[ventas, inventario]])[0]

    # Respuesta de la API en formato JSON
    return Response({
        "reabastecer": int(pred),  # Convertir la predicción (0 o 1) a entero
        "mensaje": "Sí debes reabastecer" if pred == 1 else "No es necesario"
    })'''

# Importamos tus modelos
'''from .models import Producto

# Importamos tu clase de IA (Asegúrate que el archivo se llame cerebro.py)
try:
    from .cerebro import CerebroPrediccion

    cerebro_ia = CerebroPrediccion()  # Inicializamos la IA una sola vez
except ImportError:
    print("ADVERTENCIA: No se pudo importar CerebroPrediccion. Usando modo simulación.")
    cerebro_ia = None


def dashboard_inteligente(request):
    """
    Este endpoint alimenta el Dashboard principal.
    Devuelve un JSON con:
    1. Alertas de stock (basado en predicción de demanda).
    2. Sugerencias de precios (basado en elasticidad/demanda).
    3. Resumen rápido de ventas.
    """

    # 1. Preparar el contexto (Datos de fecha)
    hoy = datetime.now()
    # weekday(): 0=Lunes, 6=Domingo.
    dia_semana_actual = hoy.weekday()

    response_data = {
        "fecha": hoy.strftime("%Y-%m-%d"),
        "alertas_inventario": [],
        "sugerencias_precio": [],
        "resumen_ia": {}
    }

    productos = Producto.objects.all()

    # Recorremos cada producto para que la IA lo analice individualmente
    for p in productos:
        # --- A. PREDICCIÓN DE DEMANDA (Punto 1 y 4) ---
        venta_esperada = 0

        if cerebro_ia:
            # Si tienes la IA lista, le preguntamos
            # Asegúrate que tu metodo en cerebro.py acepte estos argumentos
            venta_esperada = cerebro_ia.predecir_demanda_mañana(p.id, dia_semana_actual)
        else:
            # FALLBACK: Si no hay IA aún, usamos un random para probar que el frontend funciona
            venta_esperada = random.randint(5, 50)

        # Calculamos días restantes de inventario
        # Evitamos división por cero si la venta esperada es 0
        if venta_esperada > 0:
            dias_restantes = p.stock_actual / venta_esperada
        else:
            dias_restantes = 999  # Stock infinito si no se vende nada

        # Generar Alerta si queda poco tiempo
        if dias_restantes < 3:  # Menos de 3 días de stock
            urgencia = "ALTA" if dias_restantes < 1 else "MEDIA"

            response_data["alertas_inventario"].append({
                "producto_id": p.id,
                "producto_nombre": p.nombre,
                "stock_actual": p.stock_actual,
                "venta_diaria_predicha": round(venta_esperada, 1),
                "dias_restantes": round(dias_restantes, 1),
                "urgencia": urgencia,
                "mensaje": f"Se agota en {round(dias_restantes, 1)} días."
            })

        # --- B. OPTIMIZACIÓN DE PRECIOS (Punto 3) ---
        # Lógica: Si queda poco stock y la demanda es alta -> SUGERIR SUBIR PRECIO
        # Si hay mucho stock y demanda baja -> SUGERIR BAJAR PRECIO (Promo)

        accion_precio = "MANTENER"
        razon = ""

        # Convertimos decimal a float para comparaciones si es necesario
        precio_float = float(p.precio_actual)

        if dias_restantes < 2 and venta_esperada > 20:
            accion_precio = "SUBIR"
            razon = "Alta demanda y poco stock (Escasez)"
        elif dias_restantes > 15 and venta_esperada < 5:
            accion_precio = "BAJAR"
            razon = "Producto estancado (Exceso de inventario)"

        if accion_precio != "MANTENER":
            nuevo_precio = precio_float * 1.10 if accion_precio == "SUBIR" else precio_float * 0.90

            response_data["sugerencias_precio"].append({
                "producto": p.nombre,
                "precio_actual": precio_float,
                "accion": accion_precio,
                "razon_ia": razon,
                "nuevo_precio_sugerido": round(nuevo_precio, 2)
            })

    # --- C. RESUMEN GENERAL ---
    response_data["resumen_ia"] = {
        "total_productos_analizados": productos.count(),
        "productos_en_riesgo": len(response_data["alertas_inventario"]),
        "nota_del_modelo": "Predicciones basadas en Random Forest v1.0"
    }

    return JsonResponse(response_data)'''

from django.shortcuts import render
from django.http import JsonResponse  # <--- ESTA ES LA LÍNEA QUE PROBABLEMENTE TE FALTA
from datetime import datetime
import random
from django.views.decorators.csrf import csrf_exempt

# Importamos tus modelos
from .models import Producto, Venta

# Importamos tu clase de IA (Manejo de errores por si no existe aún)
try:
    from .cerebro_ia import CerebroPrediccion
    cerebro_ia = CerebroPrediccion()  # Inicializamos la IA
except ImportError:
    print("ADVERTENCIA: No se pudo importar CerebroPrediccion. Usando modo simulación.")
    cerebro_ia = None

@csrf_exempt
def dashboard_inteligente(request):
    """
    Endpoint principal del Dashboard.
    """
    hoy = datetime.now()
    dia_semana_actual = hoy.weekday()

    response_data = {
        "fecha": hoy.strftime("%Y-%m-%d"),
        "alertas_inventario": [],
        "sugerencias_precio": [],
        "resumen_ia": {}
    }

    productos = Producto.objects.all()

    for p in productos:
        # 1. Predicción
        venta_esperada = 0
        if cerebro_ia:
            venta_esperada = cerebro_ia.predecir_demanda_mañana(p.id, dia_semana_actual)
        else:
            venta_esperada = random.randint(5, 50) # Fallback

        # 2. Días restantes
        if venta_esperada > 0:
            dias_restantes = p.stock_actual / venta_esperada
        else:
            dias_restantes = 999

        # 3. Alertas
        if dias_restantes < 3:
            urgencia = "ALTA" if dias_restantes < 1 else "MEDIA"
            response_data["alertas_inventario"].append({
                "producto_id": p.id,
                "producto_nombre": p.nombre,
                "stock_actual": p.stock_actual,
                "dias_restantes": round(dias_restantes, 1),
                "urgencia": urgencia,
                "mensaje": f"Se agota en {round(dias_restantes, 1)} días."
            })

        # 4. Precios
        accion_precio = "MANTENER"
        razon = ""
        precio_float = float(p.precio_actual)

        if dias_restantes < 2 and venta_esperada > 20:
            accion_precio = "SUBIR"
            razon = "Escasez inminente y alta demanda"
        elif dias_restantes > 15 and venta_esperada < 5:
            accion_precio = "BAJAR"
            razon = "Exceso de inventario"

        if accion_precio != "MANTENER":
            nuevo_precio = precio_float * 1.10 if accion_precio == "SUBIR" else precio_float * 0.90
            response_data["sugerencias_precio"].append({
                "producto": p.nombre,
                "accion": accion_precio,
                "razon_ia": razon,
                "nuevo_precio_sugerido": round(nuevo_precio, 2)
            })

    # Resumen final
    response_data["resumen_ia"] = {
        "total_productos": productos.count(),
        "alertas_activas": len(response_data["alertas_inventario"])
    }

    return JsonResponse(response_data)


def home(request):
    """
    Vista de bienvenida para la raíz del sitio.
    """
    return JsonResponse({
        "estado": "Activo",
        "mensaje": "Bienvenido al Sistema IA. Ve a /api/dashboard-ia/ para ver datos."
    })