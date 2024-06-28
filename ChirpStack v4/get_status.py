import requests

# URL base de la API de ChirpStack
base_url = "http://localhost:8090/api"

# Endpoint para obtener el estado de las gateways
endpoint = "/gateways?limit=100"

# Token de acceso para autenticación
token = "{{token_chirpstack}}"

# Encabezados de la solicitud con el token de acceso
headers = {
    "Grpc-Metadata-Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Hacer la solicitud GET a la API
response = requests.get(base_url + endpoint, headers=headers)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Convertir la respuesta JSON en un diccionario de Python
    gateways = response.json()["result"]

    # Contadores para los estados de las gateways
    active_count = 0
    inactive_count = 0
    never_seen_count = 0

    # Iterar sobre las gateways y contar su estado
    for gateway in gateways:
        last_seen_at = gateway.get("lastSeenAt")
        if last_seen_at is None:
            never_seen_count += 1
        elif gateway.get("status", {}).get("connected", False):
            active_count += 1
        else:
            inactive_count += 1

    # Mostrar los resultados
    print("Resumen de estado de los gateways:")
    print(f"activeCount: {active_count}")
    print(f"inactiveCount: {inactive_count}")
    print(f"neverseenCount: {never_seen_count}")
else:
    print("Error al obtener el estado de los gateways:", response.status_code)
    print("Mensaje:", response.text)