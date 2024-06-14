import requests
import json
import pandas as pd
import openpyxl

client_id = "{{client_id}}"

# Función para obtener el token de acceso de ThingsBoard
def obtener_token_de_acceso_thingsboard():
    login_endpoint = "{{thingsboard_host}}/api/auth/login"
    auth_data = {
        "username": "{{username}}",
        "password": "{{password}}"
    }
    try:
        response = requests.post(login_endpoint, json=auth_data)
        if response.status_code == 200:
            access_token = response.json().get("token")
            return access_token
        else:
            print(f"Error de autenticación en ThingsBoard. Código de estado: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print("Error al conectar con ThingsBoard para autenticación.")
        print(e)
        return None

# Función para obtener la lista de dispositivos de un cliente
def obtener_dispositivos_de_cliente(cliente_id, access_token):
    url = f"{{thingsboard_host}}/api/customer/{cliente_id}/devices"
    headers = {
        "Content-Type": "application/json",
        "X-Authorization": f"Bearer {access_token}"
    }
    
    dispositivos = []
    page = 0
    page_size = 100  # Número de dispositivos por página (puedes ajustarlo según sea necesario)

    while True:
        params = {
            "pageSize": page_size,
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        dispositivos.extend(response_data.get('data', []))

        if response_data.get('hasNext', False):
            page += 1
        else:
            break

    return dispositivos

# Función para obtener los valores de atributos de un dispositivo
def obtener_telemetria_dispositivo(device_id, access_token, keys=None):
    url = f"{{thingsboard_host}}/api/plugins/telemetry/DEVICE/{device_id}/values/attributes"
    headers = {"X-Authorization": f"Bearer {access_token}"}
    
    if keys:
        url += f"?keys={','.join(keys)}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los valores de atributos. Código de estado: {response.status_code}")
        return None

# Obtener el token de acceso
access_token = obtener_token_de_acceso_thingsboard()

# Obtener el token de acceso
access_token = obtener_token_de_acceso_thingsboard()
if access_token:
    device_id = "{{device_id}}"
    keys = ["eui", "active", "caja string", "campo", "canal 1", "canal 2", "canal 3", "canal 4", "fecha hora", "harness"]

    valores_atributos = obtener_telemetria_dispositivo(device_id, access_token, keys)
    if valores_atributos:
        # Crear un nuevo libro de Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Añadir encabezados
        headers = ["eui", "active", "caja string", "campo", "canal 1", "canal 2", "canal 3", "canal 4", "fecha hora", "harness"]
        ws.append(headers)
        
        # Obtener valores y añadirlos al libro de Excel
        row_data = [device_id, "", "", "", "", "", "", "", "", ""]
        for item in valores_atributos:
            if item['key'] == 'active':
                row_data[1] = item['value']
            elif item['key'] == 'caja string':
                row_data[2] = item['value']
            elif item['key'] == 'campo':
                row_data[3] = item['value']
            elif item['key'] == 'canal 1':
                row_data[4] = item['value']
            elif item['key'] == 'canal 2':
                row_data[5] = item['value']
            elif item['key'] == 'canal 3':
                row_data[6] = item['value']
            elif item['key'] == 'canal 4':
                row_data[7] = item['value']
            elif item['key'] == 'fecha hora':
                row_data[8] = item['value']
            elif item['key'] == 'harness':
                row_data[9] = item['value']
            else:
                row_data[0] = item['key']

        # Añadir fila al libro de Excel
        ws.append(row_data)
        
        # Guardar el archivo de Excel
        wb.save("report.xlsx")
        print("Archivo de Excel creado exitosamente.")
