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

class Servidor(models.Model):
    nombre = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    usuario = models.CharField(max_length=255)
    contrasena_bot = models.CharField(max_length=255)

class RegistroRespaldo(models.Model):
    servidor_origen = models.CharField(max_length=255)
    directorio_origen = models.CharField(max_length=255)
    servidor_destino = models.CharField(max_length=255)
    directorio_destino = models.CharField(max_length=255)
    periodicidad = models.CharField(max_length=255)
    fecha_respaldo = models.DateTimeField(auto_now_add=True)


class Prueba(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)