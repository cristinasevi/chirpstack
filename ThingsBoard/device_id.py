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
def obtener_device_id(device_name):
    url_base = {{thingsboard_host}}:443/api/tenant/devices"
    params = {"deviceName": device_name}
    access_token = obtener_token_de_acceso_thingsboard()
    if access_token is None:
        print("No se pudo obtener el token de acceso del usuario.")
        return None

    headers = {
        "X-Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url_base, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            # print("Respuesta completa de ThingsBoard:", data) 
            if 'id' in data and 'id' in data['id']:
                device_id = data['id']['id']
                return device_id
            else:
                print("No se encontró el dispositivo.")
                return None
        else:
            print(f"Error: {response.status_code}")
            print(response.text)  
            return None

    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

dev_eui = "{{dev_eui}}"
device_name = dev_eui

device_id = obtener_device_id(device_name)

if device_id:
    print(f"Device ID: {device_id}")
else:
    print("No se pudo obtener el ID del dispositivo.")