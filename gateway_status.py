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


def GetGatewayStatus(server, api_token):
    url = f"http://{server}/api/gateways"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    try:
        response = requests.get(url, headers=auth_token)
        if response.status_code == 200:
            gateways = response.json()

            active_gateways = []
            inactive_gateways = []
            never_seen_gateways = []

            for gateway in gateways:
                if gateway["lastSeenAt"] is None:
                    never_seen_gateways.append(gateway)
                elif gateway["status"] == "offline":
                    inactive_gateways.append(gateway)
                else:
                    active_gateways.append(gateway)

            return active_gateways, inactive_gateways, never_seen_gateways
        else:
            print(f"Error al obtener la lista de gateways. Código de estado: {response.status_code}")
            return None, None, None
    except Exception as e:
        print(f"Error al enviar la solicitud GET: {str(e)}")
        return None, None, None

active_gateways, inactive_gateways, never_seen_gateways = GetGatewayStatus(server, api_token)

if active_gateways:
    print("Gateways activos:")
    for gateway in active_gateways:
        print(gateway["id"])

if inactive_gateways:
    print("Gateways inactivos:")
    for gateway in inactive_gateways:
        print(gateway["id"])

if never_seen_gateways:
    print("Gateways nunca vistos:")
    for gateway in never_seen_gateways:
        print(gateway["id"])
