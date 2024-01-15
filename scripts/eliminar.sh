#!/bin/bash

archivo_cron=$(crontab -l)

cron=$(echo "$archivo_cron" | grep "$1$")

if [ -z "$cron" ]; then
	echo "No existe ese cron"
	exit 1
fi

echo "$archivo_cron" | grep -v "$1$" | crontab -

crontab -l > cron_temp

