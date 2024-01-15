#!/bin/bash

#Obtener JSON de la página web

datos_json=$(curl -X POST -d "contra=servidor2" http://192.168.43.26:8000/respaldar_servidor/)

error=$(echo $datos_json | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")

if [ $error == "ERROR" ];then
	echo "Las contraseñas no coinciden"
else
	id=$(echo $datos_json | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

	idOrigen=$(echo $datos_json | python3 -c "import sys, json; print(json.load(sys.stdin)['servidor_origen'])")

	dirOrigen=$(echo $datos_json | python3 -c "import sys, json; print(json.load(sys.stdin)['directorio_origen'])")

	ipDestino=$(echo $datos_json | python3 -c "import sys, json; print(json.load(sys.stdin)['ip_destino'])")

	dirDestino=$(echo $datos_json | python3 -c "import sys, json; print(json.load(sys.stdin)['directorio_destino'])")

	userDestino=$(echo $datos_json | python3 -c "import sys, json; print(json.load(sys.stdin)['userDestino'])")

	cron=$(echo "$datos_json" | python3 -c "import sys, json; print(json.load(sys.stdin)['periodicidad'])")

	ruta="/home/servidor2/codigo.sh"

	crontab -l > cron_temp
	nuevo_cron="$cron $ruta $dirOrigen $ipDestino $dirDestino $userDestino $id"
	echo "$nuevo_cron" >> cron_temp
	cat cron_temp | crontab -
fi
