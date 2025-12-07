from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Cliente, Producto, Venta

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cluster_ia', 'total_gastado')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock_actual', 'precio_actual')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha', 'dia_semana')