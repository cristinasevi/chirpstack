import grpc
from chirpstack_api.as_pb.external import api
from datetime import datetime
import time
#import openpyxl
import os
import configparser

import requests 

import csv

server = "localhost:8080"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiYzA2OGEwYmEtYzBlMC00MjEyLWE4ODgtOTJmN2MwOGFmN2YzIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTY3NDQ4ODQzNywic3ViIjoiYXBpX2tleSJ9.RJL-sufSNfSAjbCNsprihZdZzvCeMWhBPPBgmZH4qQk"
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
            if start_row <= row_index <= end_row and row_index not in exclude_rows:
                dev_eui = row[0][3:19]  # Obtener los EUI de la primera columna del cuarto al decimonoveno carácter
                DeleteDeviceActivation(api_token, server, dev_eui)    

csv_file = "prueba.csv"
start_row = 465
end_row = 561
exclude_rows = [536, 516, 470]

DeleteDeviceActivationsCSV(api_token, server, csv_file, start_row, end_row)

