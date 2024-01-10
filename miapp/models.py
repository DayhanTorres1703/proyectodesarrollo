from django.db import models
#class Servidor(models.Model):
 #   nombre = models.CharField(max_length=40)
# Create your models here.

class Bots(models.Model):
    servidor = models.CharField(max_length=50)
    contra = models.CharField(max_length=256)

class Reportes(models.Model):
    hora = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)