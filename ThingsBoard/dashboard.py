import requests
import json

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

# Función para obtener el ID del grupo de entidades en ThingsBoard - GET /api/entityGroup/all/{ownerType}/{ownerId}/{groupType}
def obtener_id_de_grupo_de_entidades(ownerType, ownerId, groupType):
    token = obtener_token_de_acceso_thingsboard()
    if not token:
        return None
    
    endpoint = f"http://thingsboard.chemik.es/api/entityGroup/all/{ownerType}/{ownerId}/{groupType}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            grupo = response.json()
            if 'id' in grupo and 'id' in grupo['id']:
                return grupo['id']['id']
            else:
                print("La respuesta no contiene el ID esperado.")
                print(grupo)
                return None
        else:
            print(f"Error al obtener el grupo de entidades. Código de estado: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print("Error al conectar con ThingsBoard para obtener el grupo de entidades.")
        print(e)
        return None

# Función para exportar los dashboards de un grupo de entidades en ThingsBoard y guardar en un archivo JSON - GET /api/entityGroup/{entityGroupId}/dashboards/export{?limit}
def exportar_dashboards(ownerType, ownerId, groupType, limit=None):
    entityGroupId = obtener_id_de_grupo_de_entidades(ownerType, ownerId, groupType)
    if not entityGroupId:
        return None
    
    token = obtener_token_de_acceso_thingsboard()
    if not token:
        return None
    
    endpoint = f"http://thingsboard.chemik.es/api/entityGroup/{entityGroupId}/dashboards/export"
    if limit:
        endpoint += f"?limit={limit}"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            dashboards = response.json()
            with open('dashboard.json', 'w') as file:
                json.dump(dashboards, file, indent=4)
            print("Dashboards exportados y guardados en 'dashboard.json'")
            return dashboards
        else:
            print(f"Error al exportar los dashboards. Código de estado: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print("Error al conectar con ThingsBoard para exportar los dashboards.")
        print(e)
        return None

# Ejemplo de uso de la función
ownerType = "CUSTOMER"  
ownerId = "dc8383c0-f0d9-11ee-a9f5-675b85d8bd3b"  
groupType = "DASHBOARD"  
limit = 1  # Opcional, puedes especificar el límite de dashboards a exportar

dashboards_exportados = exportar_dashboards(ownerType, ownerId, groupType, limit)
if dashboards_exportados:
    print(dashboards_exportados)
else:
    print("No se pudieron exportar los dashboards o hubo un error.")
