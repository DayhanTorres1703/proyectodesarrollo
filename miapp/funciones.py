from django.shortcuts import redirect
import re
import os

#Función para el manejo de sesiones
def logueado(fun_a_decorar):
    def interna(request, *args, **kwars):
        logueado = request.session.get('logueado', False)
        if not logueado:
            return redirect('/login')
        return fun_a_decorar(request, *args, **kwars)

def validar_ip(ip):
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(regex, ip):
        return True
    else:
        return False

#def preguntarEstadoServidor(ip):
#    ping
