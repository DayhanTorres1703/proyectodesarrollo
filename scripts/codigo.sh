#!/bin/bash

PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games

fecha_actual=`date +%H%M%S-%d-%m-%Y`

tar -cvf $fecha_actual.tar $1/*

scp $fecha_actual.tar $4@$2:$3
echo $? >> logs.txt
if [ $? -eq 0 ];then
	#Reporte de respaldo exitoso
	curl -X POST -d "estado=Exitoso&nombre='$fecha_actual.tar'&pass=servidor1&id=$5" http://192.168.1.79:8000/subir_reporte/ >> logs.txt
else
	#Reporte de respaldo fallido
	curl -X POST -d "estado=Fallido&nombre='$fecha_actual.tar'&pass=servidor1&id=$5" http://192.168.1.79:8000/subir_reporte/ >> logs.txt
fi

rm $fecha_actual.tar


