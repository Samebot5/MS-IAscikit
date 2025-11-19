from django.contrib import admin
from django.urls import path
from prediccion.views import predecir

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/prediccion/', predecir),
]
