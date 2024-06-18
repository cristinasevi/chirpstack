import requests
import json
import openpyxl
import datetime

client_id = "583a31f0-0d48-11ef-8724-b1dfb72e4ebd"

# Función para obtener el token de acceso de ThingsBoard
def obtener_token_de_acceso_thingsboard():
    login_endpoint = "http://thingsboard.chemik.es/api/auth/login"
    auth_data = {
        "username": "info@inartecnologias.es",
        "password": "Inar.2019"
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
    url = f"http://thingsboard.chemik.es/api/customer/{cliente_id}/devices"
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
    url = f"http://thingsboard.chemik.es/api/plugins/telemetry/DEVICE/{device_id}/values/attributes"
    headers = {"X-Authorization": f"Bearer {access_token}"}
    
    if keys:
        url += f"?keys={','.join(keys)}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los valores de atributos para el dispositivo {device_id}. Código de estado: {response.status_code}")
        return None

# Función para obtener los valores de telemetría de un dispositivo
def obtener_timeseries_dispositivo(device_id, access_token, keys=None):
    url = f"http://thingsboard.chemik.es/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
    headers = {"X-Authorization": f"Bearer {access_token}"}
    
    if keys:
        url += f"?keys={','.join(keys)}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los valores de telemetría. Código de estado: {response.status_code}")
        return None

# Convertir tiempo Unix a formato de fecha y hora
def convertir_unix_a_fecha_hora(unix_time):
    return datetime.datetime.fromtimestamp(unix_time / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Obtener el token de acceso
access_token = obtener_token_de_acceso_thingsboard()

if access_token:
    dispositivos = obtener_dispositivos_de_cliente(client_id, access_token)
    
    if dispositivos:
        # Crear un nuevo libro de Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Añadir encabezados
        headers = ["Power station", "Inversor", "Caja string", "Harness", "N Chekness", "EUI", "Estado", "Corriente 1", "Corriente 2", "Corriente 3", "Corriente 4", "RSSI", "Contador msj", "Ubicación", "lastActivityTime"]
        ws.append(headers)
        
        # Iterar sobre los dispositivos
        for dispositivo in dispositivos:
            device_id = dispositivo['id']['id']
            nombre_dispositivo = dispositivo['name']
            
            valores_atributos = obtener_telemetria_dispositivo(device_id, access_token)
            timeseries_data = obtener_timeseries_dispositivo(device_id, access_token)
            
            # Inicializar los datos de la fila con valores vacíos
            row_data = [""] * len(headers)  # Inicializar con celdas vacías
            
            # Llenar datos de atributos si están disponibles
            if valores_atributos:
                for item in valores_atributos:
                    if item['key'] == 'power station':
                        row_data[headers.index('Power station')] = item['value']
                    elif item['key'] == 'inversor':
                        row_data[headers.index('Inversor')] = item['value']
                    elif item['key'] == 'caja string':
                        row_data[headers.index('Caja string')] = item['value']
                    elif item['key'] == 'harness':
                        row_data[headers.index('Harness')] = item['value']
                    elif item['key'] == 'N chekness':
                        row_data[headers.index('N Chekness')] = item['value']
                    elif item['key'] == 'active':
                        row_data[headers.index('Estado')] = item['value']
                    elif item['key'] == 'ubicacion':
                        row_data[headers.index('Ubicación')] = item['value']
                    elif item['key'] == 'lastActivityTime':
                        row_data[headers.index('lastActivityTime')] = convertir_unix_a_fecha_hora(item['value'])

            # Llenar datos de series temporales si están disponibles
            if timeseries_data:
                for ts_key, ts_values in timeseries_data.items():
                    if ts_key == 'data_corriente1' and ts_values:
                        row_data[headers.index('Corriente 1')] = ts_values[-1]['value']
                    elif ts_key == 'data_corriente2' and ts_values:
                        row_data[headers.index('Corriente 2')] = ts_values[-1]['value']
                    elif ts_key == 'data_corriente3' and ts_values:
                        row_data[headers.index('Corriente 3')] = ts_values[-1]['value']
                    elif ts_key == 'data_corriente4' and ts_values:
                        row_data[headers.index('Corriente 4')] = ts_values[-1]['value']
                    elif ts_key == 'rssi' and ts_values:
                        row_data[headers.index('RSSI')] = ts_values[-1]['value']
                    elif ts_key == 'msgDailyCounter' and ts_values:
                        row_data[headers.index('Contador msj')] = ts_values[-1]['value']
            
            # Insertar el nombre del dispositivo en la sexta columna
            row_data[headers.index('EUI')] = nombre_dispositivo

            # Añadir fila al libro de Excel
            ws.append(row_data)
        
        # Guardar el archivo de Excel
        wb.save("report0.xlsx")
        print("Archivo de Excel creado exitosamente.")
