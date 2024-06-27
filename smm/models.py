from django.db import models
from django.utils import timezone


class Gestion(models.Model):
    consecutivoObligacion = models.CharField(max_length=20)
    nitDeudor = models.CharField(max_length=20)
    fechaGestion = models.DateTimeField(null=True)
    estado = models.CharField(max_length=100)
    descripcionCodigoCobro = models.CharField(max_length=200)
    grabador = models.CharField(max_length=20)
    valorPactado = models.CharField(max_length=100)

class Pagos(models.Model):
    cedula = models.CharField(max_length=200)
    valorRecaudo = models.IntegerField()
    fechaPago = models.DateTimeField(null=True)
   

    