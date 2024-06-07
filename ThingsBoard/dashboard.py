import requests

# Función para obtener el token de acceso del usuario en ThingsBoard
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


# Función para obtener información de un dashboard específico en ThingsBoard - GET /api/dashboard/info/{dashboardId}
def obtener_informacion_del_dashboard(dashboard_id):
    token = obtener_token_de_acceso_thingsboard()
    if not token:
        return None
    
    dashboard_info_endpoint = f"http://thingsboard.chemik.es/api/dashboard/info/{dashboard_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(dashboard_info_endpoint, headers=headers)
        if response.status_code == 200:
            dashboard_info = response.json()
            return dashboard_info
        else:
            print(f"Error al obtener la información del dashboard. Código de estado: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print("Error al conectar con ThingsBoard para obtener la información del dashboard.")
        print(e)
        return None

# Ejemplo de uso
dashboard_id = "55eb6320-0d4c-11ef-8724-b1dfb72e4ebd"  # Reemplaza con el ID del dashboard que deseas obtener
dashboard_info = obtener_informacion_del_dashboard(dashboard_id)
if dashboard_info:
    print("Información del Dashboard:")
    print(dashboard_info)
else:
    print("No se pudo obtener la información del dashboard.")
