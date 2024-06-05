from django.db import models

class Gestion(models.Model):
    Id_gestion_campaña = models.CharField(max_length=100)
    Tipo_documento = models.CharField(max_length=100)
    Numero_documento = models.CharField(max_length=100)
    Nombre = models.CharField(max_length=100)
    Fecha_gestion = models.DateTimeField()
    Tipo_llamada = models.CharField(max_length=20)
    Codigo_gestion = models.CharField(max_length=100)
    Resultado = models.CharField(max_length=50)
    Fecha_compromiso = models.DateTimeField(null=True)
    Nombre_asesor = models.CharField(max_length=100)
    Campaña = models.CharField(max_length=100)
    Telefono = models.CharField(max_length=20)
    Obligacion = models.CharField(max_length=100)
    Nro_comparendo = models.CharField(max_length=100)
    Valor = models.CharField(max_length=50)

class Pagos(models.Model):
    Cod_cliente = models.CharField(max_length=100)
    Nit_cliente = models.CharField(max_length=100)
    Numero_obligacion = models.CharField(max_length=200)
    Fecha_pago = models.DateTimeField()
    Valor_pago = models.CharField(max_length=200)
    Aplicacion_final = models.CharField(max_length=200)
    Fecha_sencilla = models.DateTimeField()
   
    
    
# class CruceRegistro(models.Model):
#     Cedula_cliente = models.CharField(max_length=200)
#     Cod_gestion = models.CharField(max_length=200)
#     Nombre_asesor = models.CharField(max_length=200)
#     Fecha_gestion = models.DateTimeField(null=True)
#     Valor_pago = models.CharField(max_length=200)
#     Fecha_pago = models.DateTimeField(null=True)

    