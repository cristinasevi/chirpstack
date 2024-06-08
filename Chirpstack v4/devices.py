import requests 

server = "localhost:8090"
api_token = "{{token_chirpstack}}"

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

device_id = "{{dev_eui}}"

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
    "devEui": "{{dev_eui}}",
    "name": "{{dev_eui}}",
    "applicationId": "{{applicationId}}",
    "description": "Lo cree automaticamente",
    "deviceProfileId": "{{deviceProfileId}}",
    "skipFCntCheck": True,
    "referenceAltitude": 0,
    "isDisabled": False,
    "tags": {},
    "variables": {}
  }
}

PostDevice(server, api_token, device_data)

# delete /api/devices/{dev_eui}
def DeleteDevice(server, api_token, dev_eui):
    url = f"http://{server}/api/devices/{dev_eui}"
    auth_token = {"authorization": f"Bearer {api_token}"}

    try:
        response = requests.delete(url, headers=auth_token)
        if response.status_code == 200:
            print("Dispositivo eliminado correctamente.")
        else:
            print(f"Error al eliminar el dispositivo. Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar la solicitud DELETE: {str(e)}")

dev_eui = "{{dev_eui}}"

DeleteDevice(server, api_token, dev_eui)
