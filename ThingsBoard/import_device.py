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

# Función para obtener información de un dispositivo en ChirpStack usando su DevEUI
def obtener_dispositivo_por_dev_eui(dev_eui, token_chirpstack):
    # Endpoint de ChirpStack para buscar un dispositivo por dev_eui
    chirpstack_endpoint = f"http://localhost:8080/api/devices/{dev_eui}"
    headers = {
        "Grpc-Metadata-Authorization": f"Bearer {token_chirpstack}"
    }

    try:
        # Realizar la solicitud para obtener información del dispositivo en ChirpStack
        response = requests.get(chirpstack_endpoint, headers=headers)
        
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            # Retornar los datos del dispositivo
            return response.json()
        else:
            print(f"Error al obtener información del dispositivo en ChirpStack. Código de estado: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print("Error al conectar con ChirpStack.")
        print(e)
        return None

# Función para obtener el token de un dispositivo en ThingsBoard usando su ID
def obtener_token_de_dispositivo(device_id):
    access_token = obtener_token_de_acceso_thingsboard()
    if access_token is None:
        print("No se pudo obtener el token de acceso del usuario.")
        return None

    device_token_endpoint = f"{{thingsboard_host}}/api/device/{device_id}/credentials"
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

# Función para enviar datos a ThingsBoard
def enviar_datos_a_thingsboard(datos_dispositivo, cliente_id, credentialsId, device_profile_id):
    # Obtener el token de acceso de ThingsBoard
    access_token_thingsboard = obtener_token_de_acceso_thingsboard()
    if access_token_thingsboard:
        # Endpoint de ThingsBoard para enviar datos del dispositivo
        thingsboard_endpoint = f"{{thingsboard_host}}/api/v1/{credentialsId}/telemetry"
        headers = {
            "X-Authorization": f"Bearer {access_token_thingsboard}",
            "Content-Type": "application/json"
        }

        # Agregar el cliente_id a los datos del dispositivo
        datos_dispositivo["customerId"] = cliente_id
        datos_dispositivo["deviceProfileId"] = device_profile_id 

        try:
            # Realizar la solicitud para enviar datos del dispositivo a ThingsBoard
            response = requests.post(thingsboard_endpoint, json=datos_dispositivo, headers=headers)
            
            # Verificar el código de estado de la respuesta
            if response.status_code == 200:
                print("Datos del dispositivo enviados correctamente a ThingsBoard.")
            else:
                print(f"Error al enviar datos del dispositivo a ThingsBoard. Código de estado: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print("Error al conectar con ThingsBoard.")
            print(e)

# Función para asignar un dispositivo a un cliente y perfil en ThingsBoard
def asignar_dispositivo_a_cliente(dev_eui, cliente_id, device_profile_id, credentialsId):
    # Obtener el token de acceso de ThingsBoard
    access_token_thingsboard = obtener_token_de_acceso_thingsboard()
    if access_token_thingsboard:
        # Endpoint de ThingsBoard para asignar un dispositivo a un cliente y un perfil de dispositivo
        thingsboard_endpoint = "{{thingsboard_host}}:443/api/device-with-credentials"

        # Datos a enviar al dispositivo
        datos_dispositivo = {
            "device": {
                "name": dev_eui,
                "customerId": {
                    "id": cliente_id,
                    "entityType": "CUSTOMER"
                },
                "deviceProfileId": {
                    "id": device_profile_id,
                    "entityType": "DEVICE_PROFILE"
                },
            },
            "credentials": {
                "credentialsType": "ACCESS_TOKEN",
                 "credentialsId": credentialsId,
            }
        }

        # Encabezado de autorización con el token de acceso
        headers = {
            "X-Authorization": f"Bearer {access_token_thingsboard}",
            "Content-Type": "application/json"
        }

        try:
            # Realizar la solicitud para asignar el dispositivo a un cliente y un perfil de dispositivo
            response = requests.post(thingsboard_endpoint, json=datos_dispositivo, headers=headers)
            
            # Verificar el código de estado de la respuesta
            if response.status_code == 200:
                print("Dispositivo asignado correctamente a cliente y perfil de dispositivo en ThingsBoard.")
            else:
                print(f"Error al asignar dispositivo a cliente y perfil de dispositivo en ThingsBoard. Código de estado: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print("Error al conectar con ThingsBoard.")
            print(e)

# Variables
device_id = "{{device_id}}"
dev_eui = "{{dev_eui}}"
token_chirpstack = "{{token_chirpstack}}"
cliente_id = "{{cliente_id}}"
device_profile_id = "{{device_profile_id}}"

# Obtener el token de acceso del dispositivo
credentialsId = obtener_token_de_dispositivo(device_id)

# Obtener datos del dispositivo en ChirpStack
datos_dispositivo = obtener_dispositivo_por_dev_eui(dev_eui, token_chirpstack)
if datos_dispositivo:
    enviar_datos_a_thingsboard(datos_dispositivo, cliente_id, credentialsId, device_profile_id)

# Asignar el dispositivo a un cliente y perfil en ThingsBoard
asignar_dispositivo_a_cliente(dev_eui, cliente_id, device_profile_id, credentialsId)
