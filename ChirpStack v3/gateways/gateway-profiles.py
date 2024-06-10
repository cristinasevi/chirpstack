import requests 

server = "localhost:8080"
api_token = "{{token_chirpstack}}"

# GET /api/gateway-profiles/{id} 
def GetGatewayProfiles(server, api_token, gateway_id):
    url = f"http://{server}/api/gateway-profiles/{gateway_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.get(url, headers=dict(auth_token))
    
    if response.status_code == 200:
        gateway_profiles = response.json()
        return gateway_profiles
    else:
        print(f"Error al obtener los perfiles de dispositivos: {response.status_code}")
        return None

gateway_id = "{{gateway_id}}"

gateway_profiles = GetGatewayProfiles(server, api_token, gateway_id)
if gateway_profiles:
    print("Gateway profiles:")
    for key, value in gateway_profiles.items():
        print(f"{key}: {value}")

# POST /api/gateway-profiles 
def PostGatewayProfile(server, api_token, gateway_profile_data):
    url = f"http://{server}/api/gateway-profiles"
    auth_token = [("authorization", "Bearer %s" % api_token)]
    response = requests.post(url, headers=dict(auth_token), json=gateway_profile_data)

    if response.status_code == 200:
        print("Perfil de gateway creado exitosamente.")
        return response.json()
    else:
        print(f"Error al crear el perfil de gateway: {response.status_code}")
        return None
    
gateway_profile_data = {
    "gatewayProfile": {
        "channels": [
        0, 1, 2
        ],
        "extraChannels": [
        {
            "bandwidth": 0,
            "bitrate": 0,
            "frequency": 0,
            "modulation": "LORA",
            "spreadingFactors": [
            0
            ]
        }
        ],
        "id": "{{gateway_id}}",
        "name": "NewGatewayPofile",
        "networkServerID": "27",
        "statsInterval": "30s"
    }
}

response = PostGatewayProfile(server, api_token, gateway_profile_data)

if response:
    print("Gateway Profile:")
    print(response)

# PUT /api/gateway-profiles/{gateway_profile.id} 
def PutGatewayProfile(server, api_token, gateway_id, gateway_profile_data):
    url = f"http://{server}/api/gateway-profiles/{gateway_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.put(url, headers=dict(auth_token), json=gateway_profile_data)

    if response.status_code == 200:
        print(f"Perfil de gateway actualizado para {gateway_id}")
    else:
        print(f"Error al actualizar el perfil de gateway para {gateway_id}: {response.status_code}")

gateway_id = "{{gateway_id}}"

gateway_profile_data = {
    "gatewayProfile": {
        "channels": [
        0, 1, 2
        ],
        "extraChannels": [
        {
            "bandwidth": 0,
            "bitrate": 0,
            "frequency": 0,
            "modulation": "LORA",
            "spreadingFactors": [
            0
            ]
        }
        ],
        "id": "{{gateway_id}}",
        "name": "NewGatewayPofile",
        "networkServerID": "27",
        "statsInterval": "30s"
    }
}

PutGatewayProfile(server, api_token, gateway_id, gateway_profile_data)

# DELETE /api/gateway-profiles/{id} 
def DeleteGatewayProfile(api_token, server, profile_id):
    url = f"http://{server}/api/gateway-profiles/{profile_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.delete(url, headers=dict(auth_token))

    if response.status_code == 200:
        print(f"El perfil del gateway con ID {profile_id} se eliminó correctamente.")
    elif response.status_code == 404:
        print(f"No se encontró un perfil de gateway con ID {profile_id}.")
    else:
        print(f"Error al eliminar el perfil de gateway con ID {profile_id}. Código de error: {response.status_code}")

profile_id = "{{profile_id}}"

DeleteGatewayProfile(api_token, server, profile_id)
