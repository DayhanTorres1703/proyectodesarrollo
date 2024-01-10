from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import os
import json
import hashlib
from django.contrib import messages
from django.core.serializers import serialize
from miapp import funciones

#importar los modelos 
from . import models 
# Create your views here.

def hello(request):
    return HttpResponse("HOLA PROYECTO WEB")
#mostrar un templates
def index(request):
    return render(request, 'index.html')
def registroRespaldo(request):
    return render(request, 'registroRespaldo.html')

def registroServidor(request):
    return render(request, 'registroServidor.html')
def login(request):
    return render(request, 'login.html')

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

def respaldarServidor(ipOrigen, ipDestino, dirOrigen, dirDestino, cron) -> JsonResponse:
    if funciones.validar_ip(ipOrigen) == True and funciones.validar_ip(ipDestino) == True:
        return JsonResponse({'ipOrigen': ipOrigen, 'ipDestino': ipDestino, 'dirOrigen': dirOrigen, 'dirDestino': dirDestino, 'cron': cron})