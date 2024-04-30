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

def GetGateways():
    # The API token (retrieved using the web-interface).
    global api_token
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    client = api.GatewayServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    # Construct request.
    gateway = api.ListGatewayRequest()
    gateway.limit = 10000

    resp = client.List(gateway, metadata=auth_token)

    gateway_services = {}
    for gateway in resp.result:
        print(gateway)

    return gateway_services
GetGateways()

def PostGateways():
    auth_token = [("authorization", "Bearer %s" % api_token)]
    try:
        url = f'http://{server}/api/gateways'
        resp = requests.get(url, headers=dict(auth_token))
        
        if resp.status_code == 200:
            gateways = resp.json()  
            print("Información de los gateways actualizada:")
            print(gateways)  
        else:
            print("Error al obtener la información de los gateways. Código de estado:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)

PostGateways()

def PutGateways(gateway_body):
    auth_token = [("authorization", "Bearer %s" % api_token)]
    try:
        url = f'http://{server}/api/gateways'
        resp = requests.post(url, json=gateway_body, headers=dict(auth_token))
        
        if resp.status_code == 201:
            print("Gateway added successfully.")
            gateway = resp.json()
            print("Información del nuevo gateway:")
            print(gateway)
        else:
            print("Failed to add gateway. Status code:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

gateway_id = "0000000000000002"

gateway_body = {
    "gateway": {
        "boards": [
            {
                "fineTimestampKey": "", 
                "fpgaID": "",
            }
        ],
        "description": "gateway 2", 
        "discoveryEnabled": True,
        "gatewayProfileID": "6152528c-0d49-4fd4-9a2f-d377a912e0d3", 
        "id": "0000000000000002", 
        "location": {
            "accuracy": 0,
            "altitude": 0,
            "latitude": 0,
            "longitude": 0,
            "source": "UNKNOWN"
        },
        "metadata": {},
        "name": "Gateway 2", 
        "networkServerID": "27", 
        "organizationID": "1", 
        "serviceProfileID": "540e9054-ec59-4098-8fa1-8806e7cf02d4", 
        "tags": {}
    }
}

#PutGateways(gateway_body)

def GetGatewayFrames(gateway_id, server, api_token):
    auth_token = [("authorization", "Bearer %s" % api_token)]
    try:
        url = f'http://{server}/api/gateways/{gateway_id}/frames'
        resp = requests.get(url, headers=dict(auth_token))
        if resp.status_code == 200:
            frames = resp.json()
            print("Frames obtenidos exitosamente:")
            print(frames)
        else:
            print("Error al obtener frames. Código de estado:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print("Se produjo un error:", e)

gateway_id = "00800000a00097b3"

#GetGatewayFrames(gateway_id, server, api_token)

def GetGatewayStats():
    gateway_data = {
    "gateway_id": "00800000a00097b3",
    "interval": "minute",
    "startTimestamp": "2024-04-30T09:12:09.358Z",  
    "endTimestamp": "2024-04-30T10:12:09.358Z",  
    }

    gateway_id = gateway_data["gateway_id"]
    interval = gateway_data["interval"]
    startTimestamp = gateway_data["startTimestamp"]
    endTimestamp = gateway_data["endTimestamp"]
    
    auth_token = [("authorization", "Bearer %s" % api_token)]

    try:
        url = f'http://{server}/api/gateways/{gateway_id}/stats?interval={interval}&startTimestamp={startTimestamp}&endTimestamp={endTimestamp}'
        resp = requests.get(url, headers=dict(auth_token))

        if resp.status_code == 200:
            gateway_stats = resp.json()
            print("Información de estadísticas del gateway dentro del intervalo de tiempo:")
            print(gateway_stats)
        else:
            print("Error al obtener las estadísticas del gateway. Código de estado:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)

GetGatewayStats()

def DeleteGateway(gateway_id, server, api_token):
    url = f"http://{server}/api/gateways/{gateway_id}"

    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    try:
        # Enviar la solicitud DELETE para eliminar el gateway
        response = requests.delete(url, headers=dict(auth_token))
        
        # Verificar el estado de la respuesta
        if response.status_code == 200:
            print(f"Gateway {gateway_id} eliminado correctamente.")
        else:
            print(f"Error al eliminar el gateway {gateway_id}. Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar la solicitud DELETE: {str(e)}")

gateway_id = "0000000000000001"

DeleteGateway(gateway_id, server, api_token)

