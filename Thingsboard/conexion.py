import paho.mqtt.client as mqtt
import json
import requests

# Configuración de ChirpStack MQTT
chirpstack_mqtt_host = "localhost"  
chirpstack_mqtt_port = 1883
chirpstack_mqtt_topic = "application/1/device/+/event/up"

# Configuración de ThingsBoard MQTT
thingsboard_mqtt_host = "thingsboard.chemik.es"
thingsboard_mqtt_port = 1883
thingsboard_mqtt_topic = "v1/devices/me/telemetry"
thingsboard_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiNzYyOGE4NGQtOGRhMy00ZDQ1LWJlNmYtZTM4MWY5MzQ5ZWI1IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTY3NzY4NzI5NCwic3ViIjoiYXBpX2tleSJ9.LBx46H_nzGPkSxqsqVxU_5ig0soMF9dWlsuA6obE1EY"

# Callback que se ejecuta cuando se conecta al broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
    else:
        print("Error de conexión al broker MQTT. Código de resultado:", rc)

# Callback que se ejecuta cuando se recibe un mensaje MQTT desde ChirpStack
def on_message(client, userdata, msg):
    print("Mensaje recibido de ChirpStack:")
    print("Topic:", msg.topic)
    print("Payload:", msg.payload)
    payload = json.loads(msg.payload)
    # Procesar los datos recibidos según sea necesario
    # Por ejemplo, aquí podrías agregar lógica para filtrar o transformar los datos

    # Enviar los datos a ThingsBoard
    tb_payload = {"ts": payload["received_at"], "values": payload["object"]}
    tb_client.publish(thingsboard_mqtt_topic, json.dumps(tb_payload))

# Configurar el cliente MQTT para ChirpStack
chirpstack_client = mqtt.Client()
chirpstack_client.on_connect = on_connect
chirpstack_client.on_message = on_message
chirpstack_client.connect(chirpstack_mqtt_host, chirpstack_mqtt_port)
chirpstack_client.subscribe(chirpstack_mqtt_topic)

# Configurar el cliente MQTT para ThingsBoard
tb_client = mqtt.Client()
tb_client.username_pw_set(thingsboard_access_token)
tb_client.connect(thingsboard_mqtt_host, thingsboard_mqtt_port)

# Mantener los clientes MQTT conectados
chirpstack_client.loop_forever()
