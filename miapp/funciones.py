from django.shortcuts import redirect
import re
import os
import socket

#Función para el manejo de sesiones
def logueado(fun_a_decorar):
    def interna(request, *args, **kwars):
        logueado = request.session.get('usuario', False)
        if not logueado:
            return redirect('/login')
        return fun_a_decorar(request, *args, **kwars)
    return interna

def validar_ip(ip):
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(regex, ip):
        return True
    else:
        return False

def mandarSignal(ip, puerto, signal):
    #Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Dirección del destino
    direccion_destino = (ip, puerto)

    #Enviar la señal
    mensaje = signal
    sock.sendto(mensaje.encode(), direccion_destino)

    #Cerrar el socket
    sock.close()

