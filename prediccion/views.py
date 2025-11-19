import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Cargar el modelo entrenado desde el archivo modelo_inventario.pkl
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
    })

