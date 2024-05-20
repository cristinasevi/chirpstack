import requests

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

def obtener_token_de_dispositivo(device_id):
    access_token = obtener_token_de_acceso_thingsboard()
    if access_token is None:
        print("No se pudo obtener el token de acceso del usuario.")
        return None

    device_token_endpoint = f"http://thingsboard.chemik.es/api/device/{device_id}/credentials"
    headers = {
        "X-Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(device_token_endpoint, headers=headers)
        if response.status_code == 200:
            device_credentials = response.json()
            device_token = device_credentials.get("credentialsId")
            return device_token
        else:
            print(f"Error al obtener el token del dispositivo. Código de estado: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print("Error al conectar con ThingsBoard para obtener el token del dispositivo.")
        print(e)
        return None

device_id = "20988cd0-1683-11ef-994d-e3af5413ffbe"
token = obtener_token_de_dispositivo(device_id)
if token:
    print(f"El token de acceso del dispositivo es: {token}")
else:
    print("No se pudo obtener el token de acceso del dispositivo.")