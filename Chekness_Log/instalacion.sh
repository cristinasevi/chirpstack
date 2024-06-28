#!/bin/bash

# Instalar openpyxl
sudo python3 -m pip install openpyxl

# Copiar el archivo del servicio a /etc/systemd/system/
sudo cp /home/{{url_del_servicio}}/log.service /etc/systemd/system/

# Elimina el archivo del servicio
sudo rm -r log.service

# Recargar los demonios de systemd para que reconozca el nuevo servicio
sudo systemctl daemon-reload

# Deshabilitar el servicio para que no se inicie automáticamente al arrancar el sistema
sudo systemctl disable log.service

echo "Instalación completada. Para activar el servicio, ejecuta: sudo systemctl enable log.service"
