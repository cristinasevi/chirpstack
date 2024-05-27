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

# Leer configuraciones desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')


# get /api/gateway-profiles/{id} 
def GetGatewayProfiles(server, api_token, gateway_id):
    url = f"http://{server}/api/gateway-profiles/{gateway_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.get(url, headers=dict(auth_token))
    
    if response.status_code == 200:
        gateway_profiles = response.json()
        return gateway_profiles
    else:
        print(f"Error al obtener los perfiles de dispositivos: {response.status_code}")
        return None

gateway_id = "6152528c-0d49-4fd4-9a2f-d377a912e0d3"

gateway_profiles = GetGatewayProfiles(server, api_token, gateway_id)
if gateway_profiles:
    print("Gateway profiles:")
    for key, value in gateway_profiles.items():
        print(f"{key}: {value}")

# post /api/gateway-profiles 
def PostGatewayProfile(server, api_token, gateway_profile_data):
    url = f"http://{server}/api/gateway-profiles"
    auth_token = [("authorization", "Bearer %s" % api_token)]
    response = requests.post(url, headers=dict(auth_token), json=gateway_profile_data)

    if response.status_code == 200:
        print("Perfil de gateway creado exitosamente.")
        return response.json()
    else:
        print(f"Error al crear el perfil de gateway: {response.status_code}")
        return None
    
gateway_profile_data = {
    "gatewayProfile": {
        "channels": [
        0, 1, 2
        ],
        "extraChannels": [
        {
            "bandwidth": 0,
            "bitrate": 0,
            "frequency": 0,
            "modulation": "LORA",
            "spreadingFactors": [
            0
            ]
        }
        ],
        "id": "f0f2edea-5151-4aa1-b16b-44e47347c92f",
        "name": "NewGatewayPofile",
        "networkServerID": "27",
        "statsInterval": "30s"
    }
}

response = PostGatewayProfile(server, api_token, gateway_profile_data)

if response:
    print("Gateway Profile:")
    print(response)

# put /api/gateway-profiles/{gateway_profile.id} 
def PutGatewayProfile(server, api_token, gateway_id, gateway_profile_data):
    url = f"http://{server}/api/gateway-profiles/{gateway_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.put(url, headers=dict(auth_token), json=gateway_profile_data)

    if response.status_code == 200:
        print(f"Perfil de gateway actualizado para {gateway_id}")
    else:
        print(f"Error al actualizar el perfil de gateway para {gateway_id}: {response.status_code}")

gateway_id = "f0f2edea-5151-4aa1-b16b-44e47347c92f"

gateway_profile_data = {
    "gatewayProfile": {
        "channels": [
        0, 1, 2
        ],
        "extraChannels": [
        {
            "bandwidth": 0,
            "bitrate": 0,
            "frequency": 0,
            "modulation": "LORA",
            "spreadingFactors": [
            0
            ]
        }
        ],
        "id": "f0f2edea-5151-4aa1-b16b-44e47347c92f",
        "name": "NewGatewayPofile",
        "networkServerID": "27",
        "statsInterval": "30s"
    }
}

PutGatewayProfile(server, api_token, gateway_id, gateway_profile_data)

# delete /api/gateway-profiles/{id} 
def DeleteGatewayProfile(api_token, server, profile_id):
    url = f"http://{server}/api/gateway-profiles/{profile_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.delete(url, headers=dict(auth_token))

    if response.status_code == 200:
        print(f"El perfil del gateway con ID {profile_id} se eliminó correctamente.")
    elif response.status_code == 404:
        print(f"No se encontró un perfil de gateway con ID {profile_id}.")
    else:
        print(f"Error al eliminar el perfil de gateway con ID {profile_id}. Código de error: {response.status_code}")

profile_id = "9822c51d-5ce6-4109-bbc0-09e068c7d9e7"

DeleteGatewayProfile(api_token, server, profile_id)
