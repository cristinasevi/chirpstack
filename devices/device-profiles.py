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


# get /api/device-profiles/{id}
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

# post /api/device-profiles
def PostDeviceProfile(server, api_token, device_profile_data):
    url = f"http://{server}/api/device-profiles"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.post(url, headers=dict(auth_token), json=device_profile_data)

    if response.status_code == 200:
        print("Perfil de dispositivo creado exitosamente.")
        return response.json()
    else:
        print(f"Error al crear el perfil de dispositivo: {response.status_code}")
        return None

device_profile_data = {
    "deviceProfile": {
        "adrAlgorithmID": "default",
        "classBTimeout": 0,
        "classCTimeout": 0,
        "factoryPresetFreqs": [],
        "geolocBufferTTL": 0,
        "geolocMinBufferSize": 0,
        "macVersion": "1.0.2",
        "maxDutyCycle": 0,
        "maxEIRP": 14,
        "name": "NewDeviceProfile",
        "networkServerID": "27",
        "organizationID": "1",
        "payloadCodec": "CAYENNE_LPP",
        "payloadDecoderScript": "",
        "payloadEncoderScript": "",
        "pingSlotDR": 0,
        "pingSlotFreq": 0,
        "pingSlotPeriod": 0,
        "regParamsRevision": "RP002-1.0.2",
        "rfRegion": "EU868",
        "rxDROffset1": 0,
        "rxDataRate2": 0,
        "rxDelay1": 0,
        "rxFreq2": 0,
        "supports32BitFCnt": False,
        "supportsClassB": False,
        "supportsClassC": False,
        "supportsJoin": True, 
        "tags": {}, 
        "uplinkInterval": "300s"
    }
}

response = PostDeviceProfile(server, api_token, device_profile_data)

if response:
    print("Device Profile:")
    print(response)

# put /api/device-profiles/{device_profile.id}
def PutDeviceProfile(server, api_token, dev_eui, device_profile_data):
    url = f"http://{server}/api/device-profiles/{dev_eui}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.put(url, headers=dict(auth_token), json=device_profile_data)

    if response.status_code == 200:
        print(f"Perfil de dispositivo actualizado para {dev_eui}")
    else:
        print(f"Error al actualizar el perfil de dispositivo para {dev_eui}: {response.status_code}")

dev_eui = "6bdf9a7d-cc64-4fd2-91a2-41b0a7f00c93"

device_profile_data = {
    "deviceProfile": {
        "adrAlgorithmID": "default",
        "classBTimeout": 0,
        "classCTimeout": 0,
        "factoryPresetFreqs": [],
        "geolocBufferTTL": 0,
        "geolocMinBufferSize": 0,
        "macVersion": "1.0.2",
        "maxDutyCycle": 0,
        "maxEIRP": 14,
        "name": "NewDeviceProfile",
        "networkServerID": "27",
        "organizationID": "1",
        "payloadCodec": "CAYENNE_LPP",
        "payloadDecoderScript": "",
        "payloadEncoderScript": "",
        "pingSlotDR": 0,
        "pingSlotFreq": 0,
        "pingSlotPeriod": 0,
        "regParamsRevision": "RP002-1.0.2",
        "rfRegion": "EU868",
        "rxDROffset1": 0,
        "rxDataRate2": 0,
        "rxDelay1": 0,
        "rxFreq2": 0,
        "supports32BitFCnt": False,
        "supportsClassB": False,
        "supportsClassC": False,
        "supportsJoin": True, 
        "tags": {}, 
        "uplinkInterval": "300s"
    }
}

PutDeviceProfile(server, api_token, dev_eui, device_profile_data)

# delete /api/device-profiles/{id}
def DeleteDeviceProfile(api_token, server, profile_id):
    url = f"http://{server}/api/device-profiles/{profile_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.delete(url, headers=dict(auth_token))

    if response.status_code == 200:
        print(f"El perfil de dispositivo con ID {profile_id} se eliminó correctamente.")
    elif response.status_code == 404:
        print(f"No se encontró un perfil de dispositivo con ID {profile_id}.")
    else:
        print(f"Error al eliminar el perfil de dispositivo con ID {profile_id}. Código de error: {response.status_code}")

profile_id = "6bdf9a7d-cc64-4fd2-91a2-41b0a7f00c93"
DeleteDeviceProfile(api_token, server, profile_id)


