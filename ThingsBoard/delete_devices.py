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

# Función para eliminar varios dispositivos en ThingsBoard
def eliminar_dispositivos_thingsboard(device_ids):
    access_token = obtener_token_de_acceso_thingsboard()
    if access_token:
        delete_endpoint = "{{thingsboard_host}}/api/device"
        headers = {
            "Content-Type": "application/json",
            "X-Authorization": f"Bearer {access_token}"
        }
        try:
            for device_id in device_ids:
                response = requests.delete(f"{delete_endpoint}/{device_id}", headers=headers)
                if response.status_code == 200:
                    print(f"Dispositivo con ID {device_id} eliminado correctamente.")
                else:
                    print(f"No se pudo eliminar el dispositivo con ID {device_id}. Código de estado: {response.status_code}")
                    print(response.text)
        except Exception as e:
            print("Error al eliminar dispositivos en ThingsBoard.")
            print(e)

dispositivos_a_eliminar = ["{{device_id1}}", "{{device_id2}}"]
eliminar_dispositivos_thingsboard(dispositivos_a_eliminar)