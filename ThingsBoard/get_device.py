import requests

def obtener_token_de_acceso():
    # Endpoint de autenticación
    login_endpoint = "{{thingsboard_host}}/api/auth/login"

    # Datos de autenticación
    auth_data = {
        "username": "{{username}}",
        "password": "{{password}}"
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

def obtener_datos_dispositivo(access_token, device_id):
    # Endpoint para obtener datos de un dispositivo específico
    device_endpoint = f"{{thingsboard_host}}/api/device/info/{device_id}"

    # Encabezado de autorización con el token de acceso
    headers = {
        "Content-Type": "application/json",
        "X-Authorization": "Bearer " + access_token
    }

    try:
        # Realizar la solicitud para obtener datos del dispositivo específico
        response = requests.get(device_endpoint, headers=headers)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            # Extraer los datos del dispositivo de la respuesta
            device_data = response.json()
            return device_data
        else:
            print(f"Error al obtener datos del dispositivo. Código de estado: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print("Error al conectar con ThingsBoard para obtener datos del dispositivo.")
        print(e)
        return None

# Obtener el token de acceso
access_token = obtener_token_de_acceso()
if access_token:
    print("Token de acceso:", access_token)

    # ID del dispositivo específico al que deseas acceder
    dispositivo_id = "{{device_id}}"

    # Utilizar el token de acceso para obtener datos del dispositivo específico
    datos_dispositivo = obtener_datos_dispositivo(access_token, dispositivo_id)
    if datos_dispositivo:
        print("Datos del dispositivo en ThingsBoard:", datos_dispositivo)
