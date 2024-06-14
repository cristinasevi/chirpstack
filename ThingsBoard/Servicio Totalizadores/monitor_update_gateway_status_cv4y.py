import requests
import time

# Parámetros de la API de ChirpStack
tenant_id = "52f14cd4-c6f1-4fbd-8f87-4025e1d49242"
base_url = "http://localhost:8090/api/gateways"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjJjYmZjOWIxLWIzZDgtNDU3NC1hMTJjLWVmNzhiYWIwZTAyOCIsInR5cCI6ImtleSJ9.4Qzq6v_KcOvKEgXzewMNbRPS4uxE-pwcGKNjemDsRrk"

# Encabezados de la solicitud con el token de acceso
headers = {
    "Grpc-Metadata-Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

def obtener_status_gateways(base_url, headers, tenant_id, limit=100, offset=0):
    try:
        url = f"{base_url}?limit={limit}&offset={offset}&tenantId={tenant_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def imprimir_status(status):
    active_count = 0
    inactive_count = 0
    never_seen_count = 0

    for gateway in status["result"]:
        if gateway.get("lastSeenAt") is None:
            never_seen_count += 1
        elif gateway.get("status", {}).get("active", False):
            active_count += 1
        else:
            inactive_count += 1

    print(f"activeGateways: {active_count}")
    print(f"inactiveGateways: {inactive_count}")
    print(f"neverSeenGateways: {never_seen_count}")

    return {
        "activeGateways": active_count,
        "inactiveGateways": inactive_count,
        "neverSeenGateways": never_seen_count
    }

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
    access_token_thingsboard = obtener_token_de_acceso_thingsboard()
    if access_token_thingsboard:
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

def actualizar_status_cada_minuto(base_url, headers, tenant_id, telemetry_url):
    while True:
        limit = 100
        offset = 0
        active_count = 0
        inactive_count = 0
        never_seen_count = 0
        
        while True:
            status = obtener_status_gateways(base_url, headers, tenant_id, limit, offset)
            if not status:
                break

            # Imprimir y preparar datos de telemetría
            telemetry_data = imprimir_status(status)

            # Enviar telemetría a ThingsBoard
            enviar_telemetria_thingsboard(telemetry_url, telemetry_data)

            if offset + limit < status["totalCount"]:
                offset += limit
            else:
                break

        time.sleep(60)  # Espera 1 minuto antes de actualizar nuevamente

if __name__ == "__main__":
    telemetry_url = "http://thingsboard.chemik.es/api/plugins/telemetry/DEVICE/398504a0-2a4a-11ef-ae64-65281f8d87bd/SERVER_SCOPE"
    actualizar_status_cada_minuto(base_url, headers, tenant_id, telemetry_url)
