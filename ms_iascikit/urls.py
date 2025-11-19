from django.contrib import admin
from django.urls import path
from prediccion.views import predecir

urlpatterns = [
    # Ruta para acceder al panel de administración de Django
    path('admin/', admin.site.urls),

    # Ruta para acceder a tu endpoint de predicción
    # Cuando alguien visite /api/prediccion/ se ejecutará la función predecir
    path('api/prediccion/', predecir),
]
