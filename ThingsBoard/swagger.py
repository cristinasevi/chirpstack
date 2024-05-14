import grpc
from datetime import datetime
import time
import openpyxl
import os
import configparser

import requests 
import json

server = "thingsboard.chemik.es"
username = "info@inartecnologias.es"
password = "Inar.2019"
api_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJpbmZvQGluYXJ0ZWNub2xvZ2lhcy5lcyIsInVzZXJJZCI6ImMxYjExMTEwLTJhZGQtMTFlZS1hNGE1LWNmYzJmMjYxNzRmZSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiMDU4MjRkOTYtMmI1Yy00NzJlLTkwNzktZmUyM2YxMWQ2OGZiIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MTU2ODMzNjEsImV4cCI6MTcxNTY5MjM2MSwiZmlyc3ROYW1lIjoiUnViw6luIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6Ijg0Yzc4ZWMwLTJhMTMtMTFlZS1hODdkLWUzMjMwNWE4OWZkMyIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.VFHJrBmuSvefXz1boO4RceZoUX6yigojM8ioLDOW9QSeQ6KrYhbx4eQe8fFfbDdaICOJI-sEGrdpBQUoSwfVKg"

# Leer configuraciones desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')


# GET /api/device/{deviceId}
def GetDevice(device_id, server, api_token):
    url = f"http://{server}/api/device/{device_id}"
    auth_token = {"Authorization": f"Bearer {api_token}"}
    
    try:
        response = requests.get(url, headers=auth_token)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener información del dispositivo. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None


device_id = "17fcd4e0-110c-11ef-9e2d-e3d7e84d7513"

info_dispositivo = GetDevice(device_id, server, api_token)

if info_dispositivo:
    print("Información del dispositivo:")
    print(info_dispositivo)
