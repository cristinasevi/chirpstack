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

def GetDeviceProfiles(server, api_token, device_id):
    url = f"http://{server}/api/device-profiles/{device_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.get(url, headers=dict(auth_token))
    
    if response.status_code == 200:
        device_profiles = response.json()
        return device_profiles
    else:
        print(f"Error al obtener los perfiles de dispositivos: {response.status_code}")
        return None

device_id = "3363bcd9-6520-48c6-8d9d-845608aa5e57"

device_profiles = GetDeviceProfiles(server, api_token, device_id)
if device_profiles:
    print("Device profiles:")
    for key, value in device_profiles.items():
        print(f"{key}: {value}")
