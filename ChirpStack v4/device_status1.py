import requests

# Parámetros de paginación
limit = 100
offset = 0

# URL base de la API de ChirpStack
base_url = "http://localhost:8090/api/devices"

# ID de la aplicación
application_id = "application_id"

# Token de acceso
token = "{{token_chirpstack}}"

# Encabezados de la solicitud con el token de acceso
headers = {
    "Grpc-Metadata-Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Inicializar contadores
active_count = 0
inactive_count = 0
never_seen_count = 0

while True:
    # Hacer la solicitud GET a la API con paginación
    response = requests.get(f"{base_url}?limit={limit}&offset={offset}&applicationId={application_id}", headers=headers)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Convertir la respuesta JSON en un diccionario de Python
        data = response.json()
        
        # Incrementar el conteo de dispositivos
        for device in data["result"]:
            if device.get("lastSeenAt") is None:
                never_seen_count += 1
            elif device.get("status", {}).get("active", False):
                active_count += 1
            else:
                inactive_count += 1
        
        # Verificar si hay más dispositivos por recuperar
        if offset + limit < data["totalCount"]:
            offset += limit
        else:
            break
    else:
        print("Error al obtener el estado de los dispositivos:", response.status_code)
        print("Mensaje:", response.text)
        break

# Mostrar el resumen del estado de los dispositivos
print("Resumen de estado de los dispositivos:")
print(f"totalCount: {active_count + inactive_count + never_seen_count}")
print(f"activeCount: {active_count}")
print(f"inactiveCount: {inactive_count}")
print(f"neverSeenCount: {never_seen_count}")
