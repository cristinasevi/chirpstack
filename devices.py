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


def GetDevicesSummary():
    # The API token (retrieved using the web-interface).
    global api_token
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    client = api.ApplicationServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    device = api.ListApplicationRequest()
    device.limit = 10000

    resp = client.List(device, metadata=auth_token)

    device_summaries = {}
    for application in resp.result:
        # Device-queue API client.
        client = api.DeviceServiceStub(channel)

        # Define the API key meta-data.
        auth_token = [("authorization", "Bearer %s" % api_token)]

        # Construct request 
        device = api.ListDeviceRequest()
        device.application_id = application.id
        device.limit = 10000

        resp = client.List(device, metadata=auth_token)

        # Print the downlink frame-counter value.
        for device in resp.result:
            summary = api.GetDeviceRequest()
            summary.dev_eui = device.dev_eui

            # Get the device summary.
            summary = client.Get(summary, metadata=auth_token)

            # Store the device summary in the dictionary.
            device_summaries[device.dev_eui] = summary
            
        print(device_summaries)
    return device_summaries

GetDevicesSummary()

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

device_id = "0004a30b00fef714"

# Get data for the specified device.
device_data = GetDeviceData(api_token, server, device_id)
if device_data is not None:
    print("Device Data:")
    print(device_data)

# Sacar la info de EVENTOS Y FRAMES DE DEVICES

