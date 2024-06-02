import pandas as pd
import paho.mqtt.publish as publish
import time
def leer_dispositivos_desde_excel(ruta_excel):
    # Lee el archivo Excel
    df = pd.read_excel(ruta_excel)
    
    # Extrae la columna que contiene los dispositivos
    dispositivos = df["Dispositivos"].tolist()
    
    return dispositivos

def enviar_mensaje_mqtt(dispositivos):
    broker_address = "localhost"
    base_topic = "application/{{application_id}}/device/"
    suffix_topic = "/command/down"
    message = '{"fport": 2, "confirmed": true, "data": "BAM="}'
    qos = 1

    for dispositivo in dispositivos:
        topic = base_topic + dispositivo + suffix_topic
        publish.single(topic, payload=message, qos=qos, hostname=broker_address)
        time.sleep(1)

# Ruta del archivo Excel que contiene la lista de dispositivos (Cambiar a la ruta necesaria)
ruta_excel = "C:\\Users\\{{user_name}}\\Desktop\\Disp_lab_pruebas.xlsx"

# Lee los dispositivos desde el archivo Excel
dispositivos = leer_dispositivos_desde_excel(ruta_excel)

# Llamada a la función para enviar el mensaje MQTT a todos los dispositivos
enviar_mensaje_mqtt(dispositivos)
