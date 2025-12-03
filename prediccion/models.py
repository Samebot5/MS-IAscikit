from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_ultima_compra = models.DateTimeField(auto_now=True)
    total_gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frecuencia_visitas = models.IntegerField(default=0)
    cluster_ia = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    costo_base = models.DecimalField(max_digits=10, decimal_places=2, default=10.0)
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.FloatField()
    elasticidad_precio = models.FloatField(default=1.0)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    # Campos calculados automáticamente (permitimos blank=True para que el admin no los exija)
    dia_semana = models.IntegerField(blank=True, null=True)
    es_hora_pico = models.BooleanField(default=False)
    clima = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculamos datos automáticos si es un registro nuevo
        if not self.pk:
            ahora = datetime.now()
            self.dia_semana = ahora.weekday()  # 0=Lunes

            # Hora Pico simulada (1pm-3pm y 7pm-9pm)
            hora = ahora.hour
            if (13 <= hora <= 15) or (19 <= hora <= 21):
                self.es_hora_pico = True
            else:
                self.es_hora_pico = False

            if not self.clima:
                self.clima = "Normal"  # Valor por defecto si no se especifica

        super(Venta, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"