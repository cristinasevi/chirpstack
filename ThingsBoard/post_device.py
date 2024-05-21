import requests

def obtener_token_de_acceso():
    # Endpoint de autenticación
    login_endpoint = "http://thingsboard.chemik.es/api/auth/login"

    # Datos de autenticación
    auth_data = {
        "username": "info@inartecnologias.es",
        "password": "Inar.2019"
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


def crear_dispositivo(access_token, device_info):
    # Endpoint para crear un nuevo dispositivo
    create_device_endpoint = f"https://thingsboard.chemik.es:443/api/device-with-credentials" 

    # Encabezado de autorización con el token de acceso
    headers = {
        "Content-Type": "application/json",
        "X-Authorization": "Bearer " + access_token
    }

    try:
        # Realizar la solicitud para crear el dispositivo
        response = requests.post(create_device_endpoint, headers=headers, json=device_info)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            print("Dispositivo creado exitosamente.")
            return response.json()
        else:
            print(f"Error al crear el dispositivo. Código de estado: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print("Error al conectar con ThingsBoard para crear el dispositivo.")
        print(e)
        return None

# Obtener el token de acceso
access_token = obtener_token_de_acceso()
if access_token:
    print("Token de acceso:", access_token)

    # Información del dispositivo a crear
    device_info = {
        "device": {
            "tenantId": {
            "id": "c1b11110-2add-11ee-a4a5-cfc2f26174fe",
            "entityType": "TENANT"
            },
            "customerId": {
            "id": "dc8383c0-f0d9-11ee-a9f5-675b85d8bd3b",
            "entityType": "CUSTOMER"
            },
            "ownerId": {
            "id": "dc8383c0-f0d9-11ee-a9f5-675b85d8bd3b",
            "entityType": "DEVICE"
            },
            "name": "0000000000000002",
            "label": None,
            "deviceProfileId": {
            "id": "45cef3b0-2ad7-11ee-a4a5-cfc2f26174fe",
            "entityType": "DEVICE_PROFILE"
            },
            "deviceData": {
            "configuration": {
                "type": "DEFAULT"
            },
            "transportConfiguration": {
                "type": "DEFAULT"
            }
            },
            "firmwareId": None,
            "softwareId": None,
            "additionalInfo": None
        },
        "credentials": {
            "createdTime": 1715866860000,
            "credentialsType": "ACCESS_TOKEN",
            "credentialsId": "",
        }
    }

    # Crear el dispositivo
    nuevo_dispositivo = crear_dispositivo(access_token, device_info)
    if nuevo_dispositivo:
        print("Nuevo dispositivo creado:", nuevo_dispositivo)
