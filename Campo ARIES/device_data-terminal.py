import re
import json
import subprocess
 
def filter_and_extract_payload(message):
    # Utilizamos expresiones regulares para encontrar la parte de la trama que necesitas
    match_corriente = re.search(r'{"corriente1":.+?}', message)
    match_rssi = re.search(r'"rssi":\s*-?\d+', message)
    
    corriente_part = match_corriente.group() if match_corriente else None
    rssi_part = match_rssi.group() if match_rssi else None
    
    return corriente_part, rssi_part

def mqtt_subscribe():
    # Ejecuta mosquitto_sub y lee los mensajes
    process = subprocess.Popen(['mosquitto_sub', '-h', 'localhost', '-t', 'application/{{application_id}}/device/{{dev_eui}}/event/up'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for line in process.stdout:
        # Filtramos y extraemos las partes de la trama que necesitas
        corriente_part, rssi_part = filter_and_extract_payload(line)
        
        if corriente_part and rssi_part:
            print("Parte de corriente:", corriente_part)
            print("Parte de rssi:", rssi_part)

if __name__ == "__main__":
    mqtt_subscribe()