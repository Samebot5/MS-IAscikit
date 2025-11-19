import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response

model = joblib.load("modelo_inventario.pkl")


@api_view(["POST"])
def predecir(request):
    ventas = float(request.data["ventas_semana"])
    inventario = float(request.data["inventario_inicial"])

    # Regla obligatoria de negocio
    if inventario <= 0:
        return Response({
            "reabastecer": 1,
            "mensaje": "Sí debes reabastecer (inventario agotado)"
        })

    pred = model.predict([[ventas, inventario]])[0]

    return Response({
        "reabastecer": int(pred),
        "mensaje": "Sí debes reabastecer" if pred == 1 else "No es necesario"
    })
