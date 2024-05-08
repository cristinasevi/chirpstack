import grpc
from chirpstack_api.as_pb.external import api
from datetime import datetime
import time
import openpyxl
import os
import configparser

import requests 

server = "localhost:8080"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiZTc0NjBmNWUtNWNjMy00YWM3LWFkMWYtZjZlYTQ3NWYwMDlkIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTcxNDk4Mjg0OSwic3ViIjoiYXBpX2tleSJ9.PhRDrQFKrhXWJyBkHAEyQuousmOPhCI5WOcNpK5hIbU"
Com_Count = 0
last_checked_day = None
Device_List = []
Gateway_List = []

# Leer configuraciones desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')

Comm_Threshold = config['DEFAULT'].getint('Comm_Threshold', 300)  # Convertir a entero, usar 300 por defecto si no se encuentra
Log_Rate = config['DEFAULT'].getint('Log_Rate', 60)  # Convertir a entero, usar 60 por defecto si no se encuentra
Plant_Name = config['DEFAULT'].get('Plant_Name', 'Test')  # Si no se encuentra, usar 'Test' por defecto


def GetDevicesRSSI(server, api_token):
    url = f"http://{server}/api/devices"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    try:
        response = requests.get(url, headers=dict(auth_token))
        if response.status_code == 200:
            devices = response.json()
            return devices
        else:
            print(f"Error al obtener la lista de dispositivos. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al enviar la solicitud GET: {str(e)}")
        return None

def GetDevicesLastPacketRSSI(server, api_token, device_id):
    url = f"http://{server}/api/devices/{device_id}/frames"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    try:
        response = requests.get(url, headers=dict(auth_token))
        if response.status_code == 200:
            packets = response.json()
            if packets:
                last_packet_rssi = packets[0].get("rxInfo")[0].get("rssi")
                return last_packet_rssi
            else:
                print(f"No se encontraron paquetes recibidos para el dispositivo {device_id}.")
                return None
        else:
            print(f"Error al obtener los paquetes recibidos para el dispositivo {device_id}. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al enviar la solicitud GET: {str(e)}")
        return None

devices = GetDevicesRSSI(server, api_token)

if devices:
    for device in devices:
        device_id = device["id"]
        last_packet_rssi = GetDevicesLastPacketRSSI(server, api_token, device_id)
        if last_packet_rssi is not None:
            print(f"Valor RSSI del último paquete recibido para el dispositivo {device_id}: {last_packet_rssi}")


def GetDeviceRSSI(server, api_token, device_eui):
    url = f"http://{server}/api/devices/{device_eui}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.get(url, headers=dict(auth_token))

    if response.status_code == 200:
        device_info = response.json()
        return device_info.get("lastDevStatusRxInfo", [{}])[0].get("rssi")

    print(f"Error: {response.status_code} - {response.text}")
    return None

device_eui = "0004a30b00fef714"
rssi = GetDeviceRSSI(server, api_token, device_eui)
if rssi is not None:
    print(f"RSSI del dispositivo {device_eui}: {rssi}")
else:
    print("No se pudo obtener el RSSI del dispositivo.")

def GetDeviceRSSI(dev_eui):
    url = f"http://{server}/api/devices/{dev_eui}"
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    response = requests.get(url, headers=dict(auth_token))

    if response.status_code == 200:
        device_info = response.json()
        if "rxInfo" in device_info:
            rssi = device_info["rxInfo"][0]["rssi"]
            print("Mensaje de RSSI del dispositivo:", device_info)
            print("RSSI:", rssi)
        else:
            print("No se encontró información de RSSI para el dispositivo.")
    else:
        print("Error al obtener información del dispositivo:", response.status_code)
dev_eui = "0004a30b00f98573"
GetDeviceRSSI(dev_eui)

#########################################
import subprocess

dev_eui = "0004a30b00f98573"

curl_command = f'curl -X GET --header "Accept: application/json" --header "Grpc-Metadata-Authorization: Bearer {api_token}" "http://{server}/api/devices/{dev_eui}/frames"'
result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

print("Resultado de la ejecución de curl:")
print(result.stdout)
print("Errores:")
########################################
import subprocess

# Define el dev_eui y la URL base
dev_eui = "0004a30b00f98573"
base_url = "http://10.0.1.90:8080/api/devices/{}/frames"

# Construye la URL utilizando format() para insertar el dev_eui
url = base_url.format(dev_eui)

# Define el comando curl con la URL construida
curl_command = [
    'curl', 
    '-X', 'GET', 
    '--header', 'Accept: application/json', 
    '--header', 'Grpc-Metadata-Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiZTc0NjBmNWUtNWNjMy00YWM3LWFkMWYtZjZlYTQ3NWYwMDlkIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTcxNDk4Mjg0OSwic3ViIjoiYXBpX2tleSJ9.PhRDrQFKrhXWJyBkHAEyQuousmOPhCI5WOcNpK5hIbU', 
    url
]

try:
    # Ejecutar el comando curl y capturar su salida
    output = subprocess.check_output(curl_command, stderr=subprocess.STDOUT)
    # Decodificar la salida y mostrarla
    print(output.decode('utf-8'))
except subprocess.CalledProcessError as e:
    # Manejar el error si ocurre
    print(f"Error al ejecutar el comando curl: {e}")
print(result.stderr)
# Imprimir la salida del comando
print(result.stdout)

# curl -X GET --header 'Accept: application/json' --header 'Grpc-Metadata-Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiZTc0NjBmNWUtNWNjMy00YWM3LWFkMWYtZjZlYTQ3NWYwMDlkIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTcxNDk4Mjg0OSwic3ViIjoiYXBpX2tleSJ9.PhRDrQFKrhXWJyBkHAEyQuousmOPhCI5WOcNpK5hIbU' 'http://10.0.1.90:8080/api/devices/0004a30b00f98573/frames'
