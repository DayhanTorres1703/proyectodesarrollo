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
from miapp import models
from .models import Login
from .models import Servidor
from .funciones import validar_ip
from .models import RegistroRespaldo
from .funciones import logueado
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

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
#formulario pruba
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = models.Login.objects.get(usuario=username, password=password)
            # Usuario autenticado
            request.session['usuario'] = True
            return redirect('/mostrar_configuraciones/') 
        except Login.DoesNotExist:
            # Usuario no encontrado en la base de datos
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'login.html')

#Registrar respaldos
@funciones.logueado
def registroRespaldo(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        servidor_origen_ip = request.POST.get('servidorOrigen')
        directorio_origen = request.POST.get('directorioOrigen')
        servidor_destino_ip = request.POST.get('servidorDestino')
        directorio_destino = request.POST.get('directorioDestino')
        periodicidad = request.POST.get('minutos') + ' ' + request.POST.get('horas') + ' ' + request.POST.get('dias_mes') + ' ' + request.POST.get('meses') + ' ' + request.POST.get('dias_semana')
        
        # Crear y guardar el objeto RegistroRespaldo en la base de datos
        servidor_origen = models.Servidor.objects.get(ip=servidor_origen_ip)
        servidor_destino = models.Servidor.objects.get(ip=servidor_destino_ip)

        respaldo = RegistroRespaldo(
            ip_origen=servidor_origen.ip,
            directorio_origen=directorio_origen,
            ip_destino=servidor_destino.ip,
            directorio_destino=directorio_destino,
            periodicidad=periodicidad,
            servidor_origen=servidor_origen
        )
        respaldo.save()
        funciones.mandarSignal(servidor_origen_ip, 34343, "Agregar")
        return redirect('/reporteRespaldo/')
    
    servidores = models.Servidor.objects.all()
    minutos = ['*'] + list(range(60))
    horas = ['*'] + list(range(24))
    dias_mes = ['*'] + list(range(1, 32))
    meses = ['*'] + list(range(1, 13))
    dias_semana = ['*'] + list(range(8))
    
    
    return render(request, 'registroRespaldo.html', {'servidores': servidores, 'minutos': minutos, 'horas': horas, 'dias_mes': dias_mes, 'meses': meses, 'dias_semana': dias_semana})
 
@funciones.logueado
def registroServidor(request):
    if request.method == 'POST':
        nombre_servidor = request.POST.get('nombreServidor')
        ip_servidor = request.POST.get('ipServidor')
        usuario_servidor = request.POST.get('usuarioServidor')
        contrasena_bot = request.POST.get('contrasenaBot')

        # Validar la IP antes de guardarla en la base de datos
        if not validar_ip(ip_servidor):
            messages.error(request, 'La dirección IP no es válida.')
            return render(request, 'registroServidor.html')

        # Guardar en la base de datos
        servidor = Servidor(nombre=nombre_servidor, ip=ip_servidor, usuario=usuario_servidor, contrasena_bot=contrasena_bot)
        servidor.save()

        # Redirigir a la página deseada después de guardar
        return redirect('/reporteRespaldo/')

    return render(request, 'registroServidor.html', {'messages': messages.get_messages(request)})

    
# Código que escribe Benjamin para lo de AJAX
@csrf_exempt
def obtenerReporte(request) -> JsonResponse:
    if request.method == 'POST':
        #Variables que manda el bot del server
        #hora = request.POST.get('hora', '')
        estado_respaldo = request.POST.get('estado', '')
        nombre_respaldo = request.POST.get('nombre','')
        contra = request.POST.get('pass','')
        identificador = request.POST.get('id','')
        #print("HOLAAAAA" + identificador + " " + contra + " " + nombre_respaldo)

        respaldo = models.RegistroRespaldo.objects.get(id=identificador)
        respaldo_dic = model_to_dict(respaldo)
        servidor_origen_data = models.Servidor.objects.get(id=respaldo_dic['servidor_origen'])
        servidor_origen_dic = model_to_dict(servidor_origen_data)
        #print(contra == servidor_origen_dic['contrasena_bot'])
        if estado_respaldo == 'Exitoso' and contra == servidor_origen_dic['contrasena_bot']:
            nuevo_reporte = models.Reportes(estado=estado_respaldo,nombre=nombre_respaldo,respaldo_origen=respaldo)
            nuevo_reporte.save()
            return JsonResponse({'status': 'Se completó el respaldo'})
        else:
            nuevo_reporte = models.Reportes(estado=estado_respaldo,nombre=nombre_respaldo,respaldo_origen=respaldo)
            nuevo_reporte.save()
            return JsonResponse({'status':'ERROR'})

@funciones.logueado
def mostrarReportes(request) -> HttpResponse:
    reportes = models.Reportes.objects.all()
    return render(request, "reporteRespaldo.html", {'reportes': reportes})

def leerReportes(request) -> JsonResponse:
    if request.method == 'GET':
        #Recuperar reportes
        reportes = models.Reportes.objects.all()
        #Convertir a json
        reportes_serializados = serialize("json",reportes)
        reportes_json = json.loads(reportes_serializados)
        #regresar json
        return JsonResponse(reportes_json, safe=False)

@csrf_exempt
def respaldarServidor(request) -> JsonResponse:
    if request.method == 'GET':
        return JsonResponse({'status': 'ERROR'}, safe=False)

    if request.method == 'POST':
        contra = request.POST.get('contra', '')
        respaldo_reciente = models.RegistroRespaldo.objects.filter().order_by('-id')[0]
        respaldo_dic = model_to_dict(respaldo_reciente)
        servidor_origen_data = models.Servidor.objects.get(id=respaldo_dic['servidor_origen'])
        servidor_origen_dic = model_to_dict(servidor_origen_data)
        if contra == servidor_origen_dic['contrasena_bot']:
            server_destino_data = models.Servidor.objects.get(ip=respaldo_dic['ip_destino'])
            server_des_dic = model_to_dict(server_destino_data)
            respaldo_dic['userDestino'] = server_des_dic['usuario']
            respaldo_dic['status'] = "OK"
            return JsonResponse(respaldo_dic, safe=False)
        else:
            return JsonResponse({'status':'ERROR'})
#borrar configuracion de respaldos: mostrar configuraciones   
     
@funciones.logueado
def mostrar_configuraciones_respaldo(request):
    configuraciones_respaldo = models.RegistroRespaldo.objects.all()
    return render(request, 'mostrar_configuraciones_respaldo.html', {'configuraciones_respaldo': configuraciones_respaldo})
@funciones.logueado
def borrar_configuracion(request):
    if request.method == 'POST':
        configuracion_id = request.POST.get('configuracion')
        configuracion = models.RegistroRespaldo.objects.filter(id=configuracion_id).first()

        if configuracion:
            config_dic = model_to_dict(configuracion)
            #Inicio de Socket para eliminarlo del cron
            funciones.mandarSignal(config_dic['ip_origen'], 34343, str(config_dic['id']))

            configuracion.delete()

    return redirect('mostrar_configuraciones_respaldo')