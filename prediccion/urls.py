'''
  # --- Vistas normales (HTML) ---
    path('', views.home, name='home'),  # Tu vista principal actual

    # --- ENDPOINTS API (Aquí conecta tu JS / Android Studio) ---

    # Endpoint 1: El Dashboard General (Punto 9 de tu lista)
    # Devuelve: Alertas de stock, resumen de ventas y tendencias.
    path('api/dashboard-ia/', views.dashboard_inteligente, name='api_dashboard'),

    # Endpoint 2: Predicción específica por producto (Punto 1 y 4)
    # Ejemplo de uso: /api/predecir/5/ (donde 5 es el ID del producto)
    path('api/predecir/<int:producto_id>/', views.predecir_demanda_producto, name='api_predecir_producto'),

    # Endpoint 3: Segmentación de Clientes (Punto 5)
    # Devuelve: Si el cliente ID 10 es VIP, Regular o Riesgo
    path('api/cliente/<int:cliente_id>/perfil/', views.analizar_cliente, name='api_analisis_cliente'),
'''

# prediccion/urls.py
from django.urls import path
from prediccion import views
from django.http import JsonResponse

urlpatterns = [
    # Página de inicio
    path('', views.home, name='home'),

    # Dashboard Principal
    path('api/dashboard-ia/', views.dashboard_inteligente, name='api_dashboard'),

    # --- FUTURAS FUNCIONES (Descomentar solo cuando crees las funciones en views.py) ---
    # path('api/predecir/<int:producto_id>/', views.predecir_demanda_producto, name='api_predecir_producto'),
    # path('api/cliente/<int:cliente_id>/perfil/', views.analizar_cliente, name='api_analisis_cliente'),
]

# En prediccion/views.py

# ... (tus imports y la función dashboard_inteligente que ya tenías) ...

def home(request):
    return JsonResponse({
        "estado": "Activo",
        "mensaje": "Bienvenido al Sistema IA. Ve a /api/dashboard-ia/ para ver datos."
    })