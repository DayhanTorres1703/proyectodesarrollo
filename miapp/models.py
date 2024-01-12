from django.db import models
#class Servidor(models.Model):
 #   nombre = models.CharField(max_length=40)
# Create your models here.

class Bots(models.Model):
    servidor = models.CharField(max_length=50)
    contra = models.CharField(max_length=256)

class Servidor(models.Model):
    nombre = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    usuario = models.CharField(max_length=255)
    contrasena_bot = models.CharField(max_length=255)

class RegistroRespaldo(models.Model):
    ip_origen = models.GenericIPAddressField(max_length=255)
    directorio_origen = models.CharField(max_length=255)
    ip_destino = models.GenericIPAddressField(max_length=255)
    directorio_destino = models.CharField(max_length=255)
    periodicidad = models.CharField(max_length=255)
    fecha_respaldo = models.DateTimeField(auto_now_add=True)
    servidor_origen = models.ForeignKey(Servidor, on_delete=models.CASCADE)

class Reportes(models.Model):
    hora = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    respaldo_origen = models.ForeignKey(RegistroRespaldo, on_delete=models.CASCADE)

class Prueba(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    
class Login(models.Model):
    usuario = models.CharField(max_length=50)
    password = models.CharField(max_length=256)