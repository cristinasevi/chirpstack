import grpc
from chirpstack_api.as_pb.external import api

import requests 

server = "localhost:8090"
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjJjYmZjOWIxLWIzZDgtNDU3NC1hMTJjLWVmNzhiYWIwZTAyOCIsInR5cCI6ImtleSJ9.4Qzq6v_KcOvKEgXzewMNbRPS4uxE-pwcGKNjemDsRrk"

# get /api/devices/{dev_eui}  
def GetDeviceData(api_token, server, device_id):
    # Define the API endpoint to get data for a specific device.
    url = f"http://{server}/api/devices/{device_id}"

    # Define headers with authorization token.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Make a GET request to the API endpoint.
    response = requests.get(url, headers=dict(auth_token))

    # Check if the request was successful.
    if response.status_code == 200:
        # Parse the response JSON.
        device_data = response.json()
        return device_data
    else:
        # Print error message if request failed.
        print(f"Failed to get device data: {response.text}")
        return None

device_id = "0123456789abcdef"

# Get data for the specified device.
device_data = GetDeviceData(api_token, server, device_id)
if device_data is not None:
    print("Device Data:")
    print(device_data)


# post /api/devices
def PostDevice(server, api_token, device_data):
    url = f"http://{server}/api/devices"
    headers = {
        "accept": "application/json",
        "Grpc-Metadata-Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=device_data, headers=headers)
        if response.status_code == 200:
            print("Dispositivo agregado correctamente.")
        else:
            print(f"Error al agregar el dispositivo. Código de estado: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al enviar la solicitud POST: {str(e)}")

device_data = {
  "device": {
    "devEui": "0000000000000001",
    "name": "0000000000000001",
    "applicationId": "d56beb5c-5f84-4916-b54b-18c6dd7b2178",
    "description": "Lo cree automaticamente",
    "deviceProfileId": "9e9c356b-434b-4cf6-8862-78a57ab8b524",
    "skipFCntCheck": True,
    "referenceAltitude": 0,
    "isDisabled": False,
    "tags": {},
    "variables": {}
  }
}

PostDevice(server, api_token, device_data)
