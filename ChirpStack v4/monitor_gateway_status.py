import requests
import time

# Parámetros de la API de ChirpStack
tenant_id = "{{tenant_id}}"
base_url = "http://localhost:8090/api/gateways"
token = "{{token_chirpstack}}"

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

def actualizar_status_cada_minuto(base_url, headers, tenant_id):
    while True:
        limit = 100
        offset = 0
        active_count = 0
        inactive_count = 0
        never_seen_count = 0
        
        while True:
            data = obtener_status_gateways(base_url, headers, tenant_id, limit, offset)
            if not data:
                break
            
            for gateway in data["result"]:
                if gateway.get("lastSeenAt") is None:
                    never_seen_count += 1
                elif gateway.get("status", {}).get("active", False):
                    active_count += 1
                else:
                    inactive_count += 1
            
            if offset + limit < data["totalCount"]:
                offset += limit
            else:
                break

        print("Resumen de estado de los gateways:")
        print(f"totalCount: {active_count + inactive_count + never_seen_count}")
        print(f"activeCount: {active_count}")
        print(f"inactiveCount: {inactive_count}")
        print(f"neverSeenCount: {never_seen_count}")

        time.sleep(60)  # Espera 1 minuto antes de actualizar nuevamente

if __name__ == "__main__":
    actualizar_status_cada_minuto(base_url, headers, tenant_id)
