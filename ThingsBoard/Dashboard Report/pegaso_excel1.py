import requests
import json
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
        print(f"Error al obtener los valores de atributos para el dispositivo {device_id}. Código de estado: {response.status_code}")
        return None

# Función para obtener los valores de telemetría de un dispositivo
def obtener_timeseries_dispositivo(device_id, access_token, keys=None):
    url = f"{{thingsboard_host}}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
    headers = {"X-Authorization": f"Bearer {access_token}"}
    
    if keys:
        url += f"?keys={','.join(keys)}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los valores de telemetría. Código de estado: {response.status_code}")
        return None

# Obtener el token de acceso
access_token = obtener_token_de_acceso_thingsboard()

if access_token:
    dispositivos = obtener_dispositivos_de_cliente(client_id, access_token)
    
    if dispositivos:
        # Crear un nuevo libro de Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Añadir encabezados
        headers = ["EUI", "Estado", "Caja string", "Campo", "Canal 1", "Canal 2", "Canal 3", "Canal 4", "Fecha Hora", "Harness", "Power station", "Inversor", "Ubicación", "N Chekness", "lastActivityTime", "Corriente 1", "Corriente 2", "Corriente 3", "Corriente 4", "RSSI", "Date 1", "Date 2", "firstMsg", "Contador msj", "SNR"]
        ws.append(headers)
        
        # Iterar sobre los dispositivos
        for dispositivo in dispositivos:
            device_id = dispositivo['id']['id']
            nombre_dispositivo = dispositivo['name']
            
            valores_atributos = obtener_telemetria_dispositivo(device_id, access_token)
            timeseries_data = obtener_timeseries_dispositivo(device_id, access_token)
            
            if valores_atributos and timeseries_data:
                row_data = [nombre_dispositivo] + [""] * 24  # 25 columnas en total
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
                    elif item['key'] == 'power station':
                        row_data[10] = item['value']
                    elif item['key'] == 'inversor':
                        row_data[11] = item['value']
                    elif item['key'] == 'ubicacion':
                        row_data[12] = item['value']
                    elif item['key'] == 'N chekness':
                        row_data[13] = item['value']
                    elif item['key'] == 'lastActivityTime':
                        row_data[14] = item['value']
                        
            if timeseries_data: # -1 hace referencia al último valor de la serie
                for ts_key, ts_values in timeseries_data.items():
                    if ts_key == 'data_corriente1' and ts_values:
                        row_data[15] = ts_values[-1]['value']
                    elif ts_key == 'data_corriente2' and ts_values:
                        row_data[16] = ts_values[-1]['value']
                    elif ts_key == 'data_corriente3' and ts_values:
                        row_data[17] = ts_values[-1]['value']
                    elif ts_key == 'data_corriente4' and ts_values:
                        row_data[18] = ts_values[-1]['value']
                    elif ts_key == 'rssi' and ts_values:
                        row_data[19] = ts_values[-1]['value']
                    elif ts_key == 'date1' and ts_values:
                        row_data[20] = ts_values[-1]['value']
                    elif ts_key == 'date2' and ts_values:
                        row_data[21] = ts_values[-1]['value']
                    elif ts_key == 'firstMsg' and ts_values:
                        row_data[22] = ts_values[-1]['value']
                    elif ts_key == 'msgDailyCounter' and ts_values:
                        row_data[23] = ts_values[-1]['value']
                    elif ts_key == 'snr' and ts_values:
                        row_data[24] = ts_values[-1]['value']

            # Añadir fila al libro de Excel
            ws.append(row_data)
        
        # Guardar el archivo de Excel
        wb.save("report1.xlsx")
        print("Archivo de Excel creado exitosamente.")