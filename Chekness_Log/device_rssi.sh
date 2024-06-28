# #!/bin/bash

# # Lista de dispositivos
# devices=("device1" "device2")

# # Encabezados comunes para el curl
# headers="Accept: application/json"
# authorization="Grpc-Metadata-Authorization: Bearer "{{chirpstack_token}}"

# # Archivo para guardar los datos de RSSI
# output_file="rssi_data.txt"

# # Borramos el archivo si existe previamente
# rm -f "$output_file"

# # Iterar sobre cada dispositivo
# for device in "${devices[@]}"
# do
#     # Comando curl para obtener los datos del dispositivo actual
#     curl_command="curl -s -X GET --header \"$headers\" --header \"$authorization\" \"http://localhost:8080/api/devices/$device/frames\""

#     # Ejecuta el comando curl y extrae el valor de RSSI
#     device_data=$(eval $curl_command | head -n 1 | grep -o '"rssi":[^,]*' | cut -d ":" -f 2)

#     # Si se encontró un valor de RSSI, guarda el valor en el archivo
#     if [ ! -z "$device_data" ]; then
#         echo "$device: $device_data" >> "$output_file"
#         echo "Datos de RSSI agregados en $output_file para dispositivo $device"
#     else
#         echo "No se encontró información de RSSI para dispositivo $device."
#     fi
# done

# echo "Proceso completado. Los datos de RSSI se han guardado en $output_file."

#!/bin/bash

# Lista de dispositivos y sus nombres para el encabezado
devices=("device1" "device2")

# Encabezados comunes para el curl
headers="Accept: application/json"
authorization="Grpc-Metadata-Authorization: Bearer {{chirpstack_token}}"

# Archivo Excel para guardar los datos de RSSI
output_excel="rssi_data.xlsx"

# Borramos el archivo Excel si existe previamente
rm -f "$output_excel"

# Crear archivo Excel y agregar encabezados
echo -e "datetime\t${devices[0]}\t${devices[1]}" > "$output_excel"

# Iterar sobre cada dispositivo
for ((i=0; i<${#devices[@]}; i++))
do
    device="${devices[$i]}"

    # Comando curl para obtener los datos del dispositivo actual
    curl_command="curl -s -X GET --header \"$headers\" --header \"$authorization\" \"http://localhost:8080/api/devices/$device/frames\""

    # Ejecuta el comando curl y extrae el valor de RSSI
    device_data=$(eval $curl_command | head -n 1 | grep -o '"rssi":[^,]*' | cut -d ":" -f 2)

    # Si se encontró un valor de RSSI, guarda el valor en el archivo Excel
    if [ ! -z "$device_data" ]; then
        current_datetime=$(date +"%Y-%m-%d %H:%M:%S")
        echo -e "$current_datetime\t$device_data" >> "$output_excel"
        echo "Datos de RSSI agregados en $output_excel para dispositivo $devices"
    else
        echo "No se encontró información de RSSI para dispositivo $devices."
    fi
done

echo "Proceso completado. Los datos de RSSI se han guardado en $output_excel."


# sudo chmod +x nombre_del_archivo 
# sudo chmod 777 nombre_del_archivo
# dos2unix nombre_del_archivo --> Poner en la terminal para que convierta el archivo a formato Unix