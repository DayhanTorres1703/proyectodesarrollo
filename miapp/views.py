from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import os
import json
import hashlib
import datetime
from django.contrib import messages
from django.core.serializers import serialize
from miapp import funciones

#importar los modelos 
from . import models 
# Create your views here.
#incio
def hello(request):
    return HttpResponse("HOLA PROYECTO WEB")
#mostrar un templates
#INDEX
def index(request):
    return render(request, 'index.html')
def pruebaFormulario(request):
     if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')

        if nombre and apellido:
            models.Prueba.objects.create(nombre=nombre, apellido=apellido)
            return redirect('login.html')  # Redirige a una página de éxito

     return render(request, 'prueba.html')

#Login de los sysadmin
def login(request):
    return render(request, 'login.html')

#Registrar respaldos
def registroRespaldo(request):
    return render(request, 'registroRespaldo.html')

def registroServidor(request):
    return render(request, 'registroServidor.html')

#Borrar configuracion Respaldo
def borrarRespaldo(request):
    return render(request, 'borrarRespaldo.html')

#Reporte de ejecucion Respaldos
def reporteRespaldo(request):
    return render(request, 'reporteRespaldo.html')

    
# Código que escribe Benjamin para lo de AJAX

def obtenerReporte(request) -> JsonResponse:
    if request.method == 'POST':
        #Variables que manda el bot del server
        hora = request.POST.get('hora', '')
        estado_respaldo = request.POST.get('estado', '')
        nombre_respaldo = request.POST.get('nombre','')
        contra = request.POST.get('pass','')
        if estado_respaldo == '' or estado_respaldo == 'fallido':
            return JsonResponse({'Errores': 'No se completó el respaldo'})
        
    return JsonResponse({'hora': hora, 'estado': estado_respaldo, 'nombre': nombre_respaldo})

def mostrarReportes(request) -> HttpResponse:
    reportes = models.Reportes.objects.all()
    return render(request, "", {'reportes': reportes})

def leerReportes(request) -> JsonResponse:
    if request.method == 'GET':
        #Recuperar reportes
        reportes = models.Reportes.objects.all()
        #Convertir a json
        reportes_serializados = serialize("json",reportes)
        reportes_json = json.loads(reportes_serializados)
        #regresar json
        return JsonResponse(reportes_json, safe=False)

def respaldarServidor(request) -> JsonResponse:
    if request.method == 'POST':
        ipOrigen = request.POST.get('ipOrigen', '').strip
        ipDestino = request.POST.get('ipDestino', '').strip
        dirOrigen = request.POST.get('dirOrigen', '').strip
        dirDestino = request.POST.get('dirDestino', '').strip
        cron = request.POST.get('cron', '').strip
        if funciones.validar_ip(ipOrigen) == True and funciones.validar_ip(ipDestino) == True:
            fecha_actual = datetime.now
            models.Servidor(servidor_origen=ipOrigen, directorio_origen=dirOrigen, servidor_destino=ipDestino, directorio_destino=ipDestino, periodicidad=cron, fecha_respaldo=fecha_actual)
            return JsonResponse({"OK"}, safe=False)
        else:
            return JsonResponse({'ERROR'}, safe=False)