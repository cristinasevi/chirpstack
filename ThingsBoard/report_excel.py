import requests
import openpyxl

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

def obtener_valores_atributos(device_id, access_token, keys=None):
    url = f"http://thingsboard.chemik.es/api/plugins/telemetry/DEVICE/{device_id}/values/attributes"
    headers = {"X-Authorization": f"Bearer {access_token}"}
    
    if keys:
        url += f"?keys={','.join(keys)}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los valores de atributos. Código de estado: {response.status_code}")
        return None

access_token = obtener_token_de_acceso_thingsboard()
if access_token:
    device_id = "0d537d60-21b4-11ef-a4b5-cd877a1ebdc9"
    keys = ["activeDevices", "inactiveDevices", "neverSeenDevices", "activeGateways", "inactiveGateways", "neverSeenGateways"]

    valores_atributos = obtener_valores_atributos(device_id, access_token, keys)
    if valores_atributos:
        # Crear un nuevo libro de Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Añadir encabezados
        headers = ["Dev EUI", "Active Devices", "Inactive Devices", "Never Seen Devices", "Active Gateways", "Inactive Gateways", "Never Seen Gateways"]
        ws.append(headers)
        
        # Obtener valores y añadirlos al libro de Excel
        row_data = [device_id, "", "", "", "", "", "", ""]
        for item in valores_atributos:
            if item['key'] == 'activeDevices':
                row_data[1] = item['value']
            elif item['key'] == 'inactiveDevices':
                row_data[2] = item['value']
            elif item['key'] == 'neverSeenDevices':
                row_data[3] = item['value']
            elif item['key'] == 'activeGateways':
                row_data[4] = item['value']
            elif item['key'] == 'inactiveGateways':
                row_data[5] = item['value']
            elif item['key'] == 'neverSeenGateways':
                row_data[6] = item['value']
            else:
                row_data[0] = item['key']

        # Añadir fila al libro de Excel
        ws.append(row_data)
        
        # Guardar el archivo de Excel
        wb.save("report.xlsx")
        print("Archivo de Excel creado exitosamente.")
