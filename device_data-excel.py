import re
import json
import subprocess
from openpyxl import Workbook

def filter_and_extract_payload(message):
    # Utilizamos expresiones regulares para encontrar la parte de la trama que necesitas
    match_corriente = re.search(r'{"corriente1":.+?}', message)
    match_rssi = re.search(r'"rssi":\s*-?\d+', message)
    
    corriente_part = match_corriente.group() if match_corriente else None
    rssi_part = match_rssi.group() if match_rssi else None
    
    return corriente_part, rssi_part

def mqtt_subscribe():
    # Ejecuta mosquitto_sub y lee los mensajes
    process = subprocess.Popen(['mosquitto_sub', '-h', '10.139.15.30', '-t', 'application/1/device/0004a30b00fef592/event/up'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    # Creamos un libro de trabajo de Excel y seleccionamos la primera hoja
    wb = Workbook()
    ws = wb.active

    # Añadimos encabezados de columna
    ws.append(["device_eui", "corriente1", "corriente2", "corriente3", "corriente4", "rssi"])
    
    
    
    for line in process.stdout:
        # Filtramos y extraemos las partes de la trama que necesitas
        corriente_part, rssi_part = filter_and_extract_payload(line)
        
        if corriente_part and rssi_part:
            # print("Parte de corriente:", corriente_part)
            # print("Parte de rssi:", rssi_part)
           # Convertimos la parte de la trama en un diccionario JSON
            corriente_data = json.loads(corriente_part)
            rssi_data = re.search(r'-?\d+', rssi_part).group()  # Extraemos el valor de RSSI 

            # Añadimos los datos a la fila actual
            ws.append([corriente_data.get("device_eui", ""), 
                       corriente_data.get("corriente1", ""), 
                       corriente_data.get("corriente2", ""), 
                       corriente_data.get("corriente3", ""), 
                       corriente_data.get("corriente4", ""), 
                       rssi_data])

    # Guardamos el libro de trabajo en un archivo XLSX
    wb.save("device_data.xlsx")

if __name__ == "__main__":
    mqtt_subscribe()
