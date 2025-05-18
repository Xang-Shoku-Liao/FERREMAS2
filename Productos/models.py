from django.db import models

# Create your models here.
class Producto(models.Model):
    codigo_del_producto = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)