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

def obtener_dispositivo_por_dev_eui(dev_eui, token_chirpstack):
    # Endpoint de ChirpStack para buscar un dispositivo por dev_eui
    chirpstack_endpoint = f"http://localhost:8080/api/devices/{device_eui_cs}"
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
device_eui_cs = "0004a30b00f98573"


def enviar_datos_a_thingsboard(datos_dispositivo, cliente_id):
    # Obtener el token de acceso de ThingsBoard
    access_token_thingsboard = obtener_token_de_acceso_thingsboard()
    if access_token_thingsboard:
        # Endpoint de ThingsBoard para enviar datos del dispositivo
        thingsboard_endpoint = f"http://thingsboard.chemik.es/api/v1/{dev_eui_tb}/telemetry"
        headers = {
            "X-Authorization": f"Bearer {access_token_thingsboard}",
            "Content-Type": "application/json"
        }

        # Agregar el cliente_id a los datos del dispositivo
        datos_dispositivo["customerId"] = cliente_id
        datos_dispositivo["deviceProfileId"] = "45cef3b0-2ad7-11ee-a4a5-cfc2f26174fe"  

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

# Obtener datos del dispositivo por su dev_eui
dev_eui_tb = "7b07ef70-167f-11ef-994d-e3af5413ffbe"  

# Obtener el token de acceso de ChirpStack
token_chirpstack = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiZTc0NjBmNWUtNWNjMy00YWM3LWFkMWYtZjZlYTQ3NWYwMDlkIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTcxNDk4Mjg0OSwic3ViIjoiYXBpX2tleSJ9.PhRDrQFKrhXWJyBkHAEyQuousmOPhCI5WOcNpK5hIbU"

# Obtener los datos del dispositivo en ChirpStack
datos_dispositivo = obtener_dispositivo_por_dev_eui(device_eui_cs, token_chirpstack)

if datos_dispositivo:
    # Enviar los datos del dispositivo a ThingsBoard con el cliente PRUEBA
    cliente_id = "dc8383c0-f0d9-11ee-a9f5-675b85d8bd3b"
    enviar_datos_a_thingsboard(datos_dispositivo, cliente_id)


def asignar_dispositivo_a_cliente(dev_eui, cliente_id, device_profile_id):
    # Obtener el token de acceso de ThingsBoard
    access_token_thingsboard = obtener_token_de_acceso_thingsboard()
    if access_token_thingsboard:
        # Endpoint de ThingsBoard para asignar un dispositivo a un cliente y un perfil de dispositivo
        thingsboard_endpoint = "https://thingsboard.chemik.es:443/api/device-with-credentials"

        # Datos a enviar al dispositivo
        datos_dispositivo = {
            "device": {
                "name": dev_eui,
                "type": "checkness",
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
                "credentialsId": access_token_thingsboard,
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

# Llamar a la función para asignar el dispositivo a un cliente y un perfil de dispositivo
dev_eui = "0004a30b00f98573"  # Reemplazar con el dev_eui correcto
cliente_id = "dc8383c0-f0d9-11ee-a9f5-675b85d8bd3b"
device_profile_id = "45cef3b0-2ad7-11ee-a4a5-cfc2f26174fe"  # Reemplazar con el ID correcto del perfil de dispositivo
asignar_dispositivo_a_cliente(dev_eui, cliente_id, device_profile_id)

