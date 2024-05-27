import grpc
from chirpstack_api.as_pb.external import api
from datetime import datetime
import time
import openpyxl
import os
import configparser

import requests 

import csv

server = "localhost:8080"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiNzYyOGE4NGQtOGRhMy00ZDQ1LWJlNmYtZTM4MWY5MzQ5ZWI1IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTY3NzY4NzI5NCwic3ViIjoiYXBpX2tleSJ9.LBx46H_nzGPkSxqsqVxU_5ig0soMF9dWlsuA6obE1EY"

# Leer configuraciones desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')


def DeleteDeviceActivation(api_token, server, dev_eui):
    url = f"http://{server}/api/devices/{dev_eui}/activation"
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    response = requests.delete(url, headers=dict(auth_token))
    
    if response.status_code == 200:
        print(f"Activación del dispositivo {dev_eui} eliminada con éxito.")
    else:
        print(f"Error al eliminar la activación del dispositivo {dev_eui}. Código de error: {response.status_code}")

# Función para leer los EUI de un archivo CSV y eliminar las activaciones llamando al código anterior
def DeleteDeviceActivationsCSV(api_token, server, csv_file, start_row, end_row):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row_index, row in enumerate(csv_reader, 1):
            if start_row <= row_index <= end_row:
                dev_eui = row[0][3:19]  # Obtener los EUI de la primera columna del cuarto al decimonoveno carácter
                DeleteDeviceActivation(api_token, server, dev_eui)    

csv_file = "backup.csv"
start_row = 443
end_row = 611

DeleteDeviceActivationsCSV(api_token, server, csv_file, start_row, end_row)
