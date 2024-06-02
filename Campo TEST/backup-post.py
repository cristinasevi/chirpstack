import grpc
from chirpstack_api.as_pb.external import api
from datetime import datetime
import time
import openpyxl
import os
import configparser

import requests 

import pandas as pd

server = "localhost:8080"
api_token = "{{token_chirpstack}}"

# Leer configuraciones desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')


def PostDeviceActivation(api_token, server, dev_eui, activation_data):
    url = f"http://{server}/api/devices/{dev_eui}/activate"
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    response = requests.post(url, json=activation_data, headers=dict(auth_token))
    
    if response.status_code == 200:
        print(f"Activación del dispositivo {dev_eui} exitosa.")
    else:
        print(f"Error al activar el dispositivo {dev_eui}. Código de error: {response.status_code}")

def PostDeviceActivationXLSX(api_token, server, xlsx_file, start_row, end_row):
    try:
        data = pd.read_excel(xlsx_file)
        data = data.astype(str)  # Convertir todas las columnas a cadenas
        for row_index, row in data.iterrows():
            if start_row <= row_index + 1 <= end_row:
                try:
                    if len(row) >=9:
                        dev_eui = row.iloc[2][3:19]  # Obtener los EUI de la tercera columna del cuarto al decimonoveno caracter
                        activation_data = {
                            "deviceActivation": {
                                "aFCntDown": 0,  
                                "appSKey": "00000000000000000000000000000000",
                                "devAddr": row.iloc[4][3:11],
                                "devEUI": row.iloc[2][3:19],
                                "fCntUp": 138, 
                                "fNwkSIntKey": row.iloc[5][3:35],
                                "nFCntDown": 0,  
                                "nwkSEncKey": row.iloc[7][3:35],
                                "sNwkSIntKey": row.iloc[6][3:35]
                            }
                        }
                        PostDeviceActivation(api_token, server, dev_eui, activation_data)
                    else:
                        print(f"Error: No hay suficientes columnas en la fila {row_index}.")
                except IndexError as e:
                    print(f"Error en la fila {row_index + 1}: {e}")
                    continue
                print(f"Respuesta de activación para el dispositivo {dev_eui}: {activation_data}")
    except FileNotFoundError:
        print(f"El archivo {xlsx_file} no se encontró.")

xlsx_file = "backup.xlsx"
start_row = 619
end_row = 2216

PostDeviceActivationXLSX(api_token, server, xlsx_file, start_row, end_row)
