#!/bin/bash

# Almacena el comando curl en una variable
curl_command="curl -s -X GET --header \"Accept: application/json\" --header \"Grpc-Metadata-Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiZTc0NjBmNWUtNWNjMy00YWM3LWFkMWYtZjZlYTQ3NWYwMDlkIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTcxNDk4Mjg0OSwic3ViIjoiYXBpX2tleSJ9.PhRDrQFKrhXWJyBkHAEyQuousmOPhCI5WOcNpK5hIbU\" \"http://10.0.1.90:8080/api/gateways/00800000a000c55f/frames\""

# Ejecuta el comando curl y extrae la primera línea de la salida (el JSON devuelto)
gateway_data=$(eval $curl_command | head -n 1 | grep -o '"rssi":[^,]*' | cut -d ":" -f 2)

# Imprime la primera línea de los datos del gateway (el JSON devuelto)
echo "RSSI: $gateway_data"

# sudo chmod +x nombre_del_archivo 
# sudo chmod 777 nombre_del_archivo
# dos2unix nombre_del_archivo --> Poner en la terminal para que convierta el archivo a formato Unix


