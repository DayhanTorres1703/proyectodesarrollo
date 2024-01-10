from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import os
import hashlib
from django.contrib import messages
#importar los modelos 
from . import models 
# Create your views here.

def hello(request):
    return HttpResponse("HOLA PROYECTO WEB")
#mostrar un templates
def index(request):
    return render(request, 'index.html')
def registroServidor (request):
    return render(request, 'registroservidor.html')
def login(request):
    return render(request, 'login.html')

# Código que escribe Benjamin para lo de AJAX

def obtenerReporte(request):
    if request.method == 'POST':
        #Variables que manda el bot del server
        hora = request.POST.get('hora', '')
        estado_respaldo = request.POST.get('estado', '')
        nombre_respaldo = request.POST.get('nombre','')
        contra = request.POST.get('pass','')
        if estado_respaldo == '' or estado_respaldo == 'fallido':
            return JsonResponse({'Errores': 'No se completó el respaldo'})
        
    return JsonResponse({'hora': hora, 'estado': estado_respaldo, 'nombre': nombre_respaldo})

