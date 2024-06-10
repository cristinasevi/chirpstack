import requests

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

def obtener_valores_atributos(device_id, access_token, keys=None):
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

access_token = obtener_token_de_acceso_thingsboard()
if access_token:
    device_id = "{{device_id}}"
    keys = ["activeDevices", "inactiveDevices", "neverSeenDevices", "activeGateways", "inactiveGateways", "neverSeenGateways"]

    valores_atributos = obtener_valores_atributos(device_id, access_token, keys)
    if valores_atributos:
        for item in valores_atributos:  
            print(f"{item['key']}: {item['value']}")  
