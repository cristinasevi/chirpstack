import requests
import time

server = "localhost:8080"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiNzYyOGE4NGQtOGRhMy00ZDQ1LWJlNmYtZTM4MWY5MzQ5ZWI1IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTY3NzY4NzI5NCwic3ViIjoiYXBpX2tleSJ9.LBx46H_nzGPkSxqsqVxU_5ig0soMF9dWlsuA6obE1EY"

def obtener_status_gateways(api_url, headers):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def imprimir_status(status):
    active_gateways = status.get('activeCount', 'N/A')
    inactive_gateways = status.get('inactiveCount', 'N/A')
    never_seen_gateways = status.get('neverSeenCount', 'N/A')

    print(f"Active Gateways: {active_gateways}")
    print(f"Inactive Gateways: {inactive_gateways}")
    print(f"Never Seen Gateways: {never_seen_gateways}")

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

def enviar_telemetria_thingsboard(telemetry_url, telemetry_data):
    # Obtener el token de acceso de ThingsBoard
    access_token_thingsboard = obtener_token_de_acceso_thingsboard()
    if access_token_thingsboard:
        # Endpoint de ThingsBoard para enviar datos del dispositivo
        headers = {
            "X-Authorization": f"Bearer {access_token_thingsboard}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(telemetry_url, json=telemetry_data, headers=headers)
            if response.status_code == 200:
                print("Telemetría enviada exitosamente a ThingsBoard.")
            else:
                print(f"Error al enviar telemetría a ThingsBoard. Código de estado: {response.status_code}")
                print(response.text)
        except Exception as e:
            print("Error al conectar con ThingsBoard para enviar telemetría.")
            print(e)
    else:
        print("No se pudo obtener el token de acceso de ThingsBoard.")

def actualizar_status_cada_minuto(api_url, headers, telemetry_url):
    while True:
        status = obtener_status_gateways(api_url, headers)
        if status:
            imprimir_status(status)

            # Preparar datos de telemetría
            telemetry_data = {
                "activeGateways": status.get('activeCount', 'N/A'),
                "inactiveGateways": status.get('inactiveCount', 'N/A'),
                "neverSeenGateways": status.get('neverSeenCount', 'N/A')
            }

            # Enviar telemetría a ThingsBoard
            enviar_telemetria_thingsboard(telemetry_url, telemetry_data)

        time.sleep(60)  # Espera 1 minuto antes de actualizar nuevamente

if __name__ == "__main__":
    api_url = f"http://{server}/api/internal/gateways/summary"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    telemetry_url = "http://thingsboard.chemik.es/api/plugins/telemetry/DEVICE/0d537d60-21b4-11ef-a4b5-cd877a1ebdc9/SERVER_SCOPE"

    actualizar_status_cada_minuto(api_url, headers, telemetry_url)
