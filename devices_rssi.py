import grpc
from chirpstack_api.as_pb.external import api
from datetime import datetime
import time
import openpyxl
import os
import configparser

import requests 

server = "localhost:8080"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiNzYyOGE4NGQtOGRhMy00ZDQ1LWJlNmYtZTM4MWY5MzQ5ZWI1IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTY3NzY4NzI5NCwic3ViIjoiYXBpX2tleSJ9.LBx46H_nzGPkSxqsqVxU_5ig0soMF9dWlsuA6obE1EY"
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
