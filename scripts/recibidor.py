import socket
import subprocess
def ejecutar_script(script):
    # Ejecutar el script usando subprocess
    subprocess.run(script, shell=True)

def recibir_signal(ip, puerto):
    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enlazar el socket a una dirección y puerto local
    direccion = (ip, puerto)
    sock.bind(direccion)

    print(f"Esperando señales en {ip}:{puerto}")

    while True:
        # Recibir la señal
        data, address = sock.recvfrom(1024)

        # Cuando se recibe la señal, ejecutar el script
        if data.decode() == "Agregar":
            print("Señal recibida. Ejecutando el script.")
            ejecutar_script("./respaldo.sh")

        else:
            print("Señal recibida. Eliminar cron.")
            ejecutar_script("./eliminar.sh '" + data.decode() + "'")
            print(data.decode())

# Uso del script
ip_local = "192.168.43.7"
puerto_local = 34343
recibir_signal(ip_local, puerto_local)
