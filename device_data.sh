#!/bin/bash

# Almacena el comando curl en una variable
curl_command="curl -s -X GET --header 'Accept: application/json' --header 'Grpc-Metadata-Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiZTc0NjBmNWUtNWNjMy00YWM3LWFkMWYtZjZlYTQ3NWYwMDlkIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTcxNDk4Mjg0OSwic3ViIjoiYXBpX2tleSJ9.PhRDrQFKrhXWJyBkHAEyQuousmOPhCI5WOcNpK5hIbU' 'http://10.0.1.90:8080/api/devices/0004a30b00f98573/events'"

# Ejecuta el comando curl y extrae la primera línea de la salida (el JSON devuelto)
device_data=$(eval $curl_command | head -n 1)

# Imprime la primera línea de los datos del dispositivo (el JSON devuelto)
echo "$device_data"
