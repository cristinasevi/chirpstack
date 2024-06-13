import requests

application_id = "{{application_id}}"

# URL para obtener el estado de los dispositivos
url = f"{{chirpstack_host}}/api/devices?limit=1000&offset=0&applicationId={application_id}"

# Token de acceso para autenticación
token = "{{token_chirpstack}}"

# Encabezados de la solicitud con el token de acceso
headers = {
    "Grpc-Metadata-Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Hacer la solicitud GET a la API
response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Convertir la respuesta JSON en un diccionario de Python
    data = response.json()
    
    # Obtener el número total de dispositivos
    total_count = data["totalCount"]
    
    # Inicializar los contadores de estado
    active_count = 0
    inactive_count = 0
    never_seen_count = 0
    
    # Iterar sobre los dispositivos y contar su estado
    for device in data["result"]:
        if device.get("lastSeenAt") is None:
            never_seen_count += 1
        elif device.get("status", {}).get("active", False):
            active_count += 1
        else:
            inactive_count += 1
    
    # Mostrar los resultados
    print("Resumen de estado de los dispositivos:")
    print(f"totalCount: {total_count}")
    print(f"activeCount: {active_count}")
    print(f"inactiveCount: {inactive_count}")
    print(f"neverSeenCount: {never_seen_count}")
else:
    print("Error al obtener el estado de los dispositivos:", response.status_code)
    print("Mensaje:", response.text)
