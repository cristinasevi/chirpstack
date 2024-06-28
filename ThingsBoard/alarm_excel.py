import pandas as pd
import requests

# Función para obtener el token de acceso del usuario en ThingsBoard
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

# Función para obtener el device id de un dispositivo en ThingsBoard usando su device name
def obtener_device_id(device_name, access_token):
    url_base = "{{thingsboard_host}}/api/tenant/devices"
    params = {"deviceName": device_name}
    headers = {
        "X-Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url_base, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'id' in data and 'id' in data['id']:
                device_id = data['id']['id']
                return device_id
            else:
                print("No se encontró el dispositivo.")
                return None
        else:
            print(f"Error: {response.status_code}")
            print(response.text)  # Imprimir respuesta de error para depuración
            return None

    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

# Función para actualizar el valor de inactivityTimeout de un dispositivo
def actualizar_inactivity_timeout(device_name, access_token):
    device_id = obtener_device_id(device_name, access_token)
    if device_id is None:
        print(f"No se pudo obtener el ID del dispositivo: {device_name}.")
        return False
    
    url = f"{{thingsboard_host}}/api/plugins/telemetry/DEVICE/{device_id}/SERVER_SCOPE"
    payload = {
        "inactivityTimeout": 6000
    }
    headers = {
        "Content-Type": "application/json",
        "X-Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Valor de inactivityTimeout actualizado correctamente para el dispositivo: {device_name}.")
            return True
        else:
            print(f"Error al actualizar el valor para el dispositivo: {device_name}. Código de estado: {response.status_code}")
            print(response.text)
            return False
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud para el dispositivo: {device_name}.")
        print(e)
        return False

# Función para actualizar el inactivityTimeout de múltiples dispositivos
def actualizar_inactivity_timeout_multiples_dispositivos(device_names):
    access_token = obtener_token_de_acceso_thingsboard()
    if access_token is None:
        print("Error con el token de acceso.")
        return

    for device_name in device_names:
        actualizado = actualizar_inactivity_timeout(device_name, access_token)
        if actualizado:
            print(f"Actualización exitosa para el dispositivo: {device_name}.")
        else:
            print(f"Actualización fallida para el dispositivo: {device_name}.")

# Función para leer nombres de dispositivos desde un archivo Excel
def leer_nombres_dispositivos_desde_excel(xlsx_file, start_row, end_row):
    try:
        data = pd.read_excel(xlsx_file)
        data = data.astype(str)  # Convertir todas las columnas a cadenas
        device_names = []
        for row_index, row in data.iterrows():
            if start_row <= row_index + 1 <= end_row:
                dev_eui = row.iloc[5][0:16]  # Obtener los EUI de la tercera columna del cuarto al decimonoveno caracter
                device_names.append(dev_eui)
        return device_names
    except FileNotFoundError:
        print(f"El archivo {xlsx_file} no se encontró.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo {xlsx_file}: {e}")
        return []

# Ejemplo de uso
if __name__ == "__main__":
    xlsx_file = "devices.xlsx"
    start_row = 1
    end_row = 774
    device_names = leer_nombres_dispositivos_desde_excel(xlsx_file, start_row, end_row)
    actualizar_inactivity_timeout_multiples_dispositivos(device_names)