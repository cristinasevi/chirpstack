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

def PostDeviceActivation(api_token, server, dev_eui, activation_data):
    url = f"http://{server}/api/devices/{dev_eui}/activate"
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    response = requests.post(url, json=activation_data, headers=dict(auth_token))
    
    if response.status_code == 200:
        print("Activación del dispositivo exitosa.")
    else:
        print(f"Error al activar el dispositivo: {response.status_code}")

def PostDeviceActivationCSV(api_token, server, csv_file, start_row, end_row):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row_index, row in enumerate(csv_reader, 1):
            if start_row <= row_index <= end_row:
                try:
                    if len(row) >=9:
                        dev_eui = row[2][3:19]  # Obtener los EUI de la tercera columna del cuarto al decimonoveno caracter
                        activation_data = {
                            "deviceActivation": {
                                "aFCntDown": 0,  
                                "appSKey": 0,
                                "devAddr": row[4][3:11],
                                "fCntUp": 138, 
                                "fNwkSIntKey": row[5][3:35],
                                "nFCntDown": 0,  
                                "nwkSEncKey": row[7][3:35],
                                "sNwkSIntKey": row[6][3:35]
                            }
                        }
                        PostDeviceActivation(api_token, server, dev_eui, activation_data)
                    else:
                        print(f"Error: No hay suficientes columnas en la fila {row_index}.")
                except IndexError:
                    print(f"Error: No se pudo obtener la información completa de la fila {row_index}.")
                    continue
csv_file = "backup.csv"
start_row = 620
end_row = 2217

PostDeviceActivationCSV(api_token, server, csv_file, start_row, end_row)