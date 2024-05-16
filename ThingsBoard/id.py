import requests

def obtener_token_de_acceso(username, password):
    # Endpoint de autenticación
    login_endpoint = "http://thingsboard.chemik.es/api/auth/login"

    # Datos de autenticación
    auth_data = {
        "username": username,
        "password": password
    }

    try:
        # Realizar la solicitud de autenticación
        response = requests.post(login_endpoint, json=auth_data)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            # Extraer el token de acceso de la respuesta
            access_token = response.json().get("token")
            return access_token
        else:
            print(f"Error de autenticación. Código de estado: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print("Error al conectar con ThingsBoard para autenticación.")
        print(e)
        return None

def obtener_ids_dispositivos(access_token):
    # Endpoint para obtener la lista de dispositivos
    devices_endpoint = "http://thingsboard.chemik.es/api/tenant/devices"

    # Encabezado de autorización con el token de acceso
    headers = {
        "Content-Type": "application/json",
        "X-Authorization": "Bearer " + access_token
    }

    try:
        # Realizar la solicitud para obtener la lista de dispositivos
        response = requests.get(devices_endpoint, headers=headers)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            # Extraer los IDs de los dispositivos de la respuesta
            dispositivos = response.json()
            ids_dispositivos = [dispositivo['id']['id'] for dispositivo in dispositivos]
            return ids_dispositivos
        else:
            print(f"Error al obtener la lista de dispositivos. Código de estado: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print("Error al conectar con ThingsBoard para obtener la lista de dispositivos.")
        print(e)
        return None

# Datos de autenticación
username = "info@inartecnologias.es"
password = "Inar.2019"

# Obtener el token de acceso
access_token = obtener_token_de_acceso(username, password)
if access_token:
    print("Token de acceso:", access_token)

    # Utilizar el token de acceso para obtener los IDs de los dispositivos
    ids_dispositivos = obtener_ids_dispositivos(access_token)
    if ids_dispositivos:
        print("IDs de los dispositivos en ThingsBoard:")
        for dispositivo_id in ids_dispositivos:
            print(dispositivo_id)