import requests
import json

# Definir las constantes necesarias
client_id = "{{client_id}}"

# Función para obtener el token de acceso de ThingsBoard
def obtener_token_de_acceso_thingsboard():
    login_endpoint = "{{thingsboard_host}}/api/auth/login"
    auth_data = {
        "username": "{{username}}",
        "password": "{{password}"
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

# Función para obtener la lista de dispositivos de un cliente
def obtener_dispositivos_de_cliente(cliente_id, access_token):
    url = f"{{thingsboard_host}}/api/customer/{cliente_id}/devices"
    headers = {
        "Content-Type": "application/json",
        "X-Authorization": f"Bearer {access_token}"
    }
    
    dispositivos = []
    page = 0
    page_size = 100  # Número de dispositivos por página (puedes ajustarlo según sea necesario)

    while True:
        params = {
            "pageSize": page_size,
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        dispositivos.extend(response_data.get('data', []))

        if response_data.get('hasNext', False):
            page += 1
        else:
            break

    return dispositivos

# Obtener el token de acceso
access_token = obtener_token_de_acceso_thingsboard()

if access_token:
    # Ejecutar las funciones y mostrar los resultados
    dispositivos = obtener_dispositivos_de_cliente(client_id, access_token)
    print("Número total de dispositivos asociados al cliente:", len(dispositivos))
    print("Nombres de los dispositivos asociados al cliente:")
    for dispositivo in dispositivos:
        print(dispositivo.get('name'))