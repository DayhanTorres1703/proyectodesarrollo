from django.db import models
#class Servidor(models.Model):
 #   nombre = models.CharField(max_length=40)
# Create your models here.

class Bots(models.Model):
    servidor = models.CharField(max_length=50)
    contra = models.CharField(max_lenght=256)

#class Reportes(Models.Model):
    #hora = models.