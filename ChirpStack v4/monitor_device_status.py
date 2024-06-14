import requests
import time

# Parámetros de la API de ChirpStack
server = "localhost:8090"
base_url = f"http://{server}/api/devices"
application_id = "{{application_id}}"
token = "{{token_chirpstack}}"

# Encabezados de la solicitud con el token de acceso
headers = {
    "Grpc-Metadata-Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

def obtener_status_devices(base_url, headers, limit, offset, application_id):
    try:
        response = requests.get(f"{base_url}?limit={limit}&offset={offset}&applicationId={application_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def actualizar_status_cada_minuto(base_url, headers, application_id):
    limit = 100
    while True:
        offset = 0
        active_count = 0
        inactive_count = 0
        never_seen_count = 0
        
        while True:
            data = obtener_status_devices(base_url, headers, limit, offset, application_id)
            if not data:
                break

            for device in data["result"]:
                if device.get("lastSeenAt") is None:
                    never_seen_count += 1
                elif device.get("status", {}).get("active", False):
                    active_count += 1
                else:
                    inactive_count += 1
            
            if offset + limit < data["totalCount"]:
                offset += limit
            else:
                break

        print("Resumen de estado de los dispositivos:")
        print(f"totalCount: {active_count + inactive_count + never_seen_count}")
        print(f"activeCount: {active_count}")
        print(f"inactiveCount: {inactive_count}")
        print(f"neverSeenCount: {never_seen_count}")

        time.sleep(60)  # Espera 1 minuto antes de actualizar nuevamente

if __name__ == "__main__":
    actualizar_status_cada_minuto(base_url, headers, application_id)
