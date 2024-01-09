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