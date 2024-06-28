import grpc
from chirpstack_api.as_pb.external import api
import requests 

server = "localhost:8080"
api_token = {{token_chirpstack}}

def GetGatewaysSummary():
    # The API token (retrieved using the web-interface).
    global api_token
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    client = api.ApplicationServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    gateway = api.ListApplicationRequest()
    gateway.limit = 10000

    resp = client.List(gateway, metadata=auth_token)


    gateway_summaries = {}
    for gateway in resp.result:
        client = api.GatewayServiceStub(channel)
        print(gateway)

    return gateway_summaries

GetGatewaysSummary()

def GetGateways():
    # The API token (retrieved using the web-interface).
    global api_token
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    client = api.GatewayServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    # Construct request.
    gateway = api.ListGatewayRequest()
    gateway.limit = 10000

    resp = client.List(gateway, metadata=auth_token)

    gateway_services = {}
    for gateway in resp.result:
        print(gateway)

    return gateway_services
GetGateways()

# GET /api/internal/gateways/summary 
def GetGatewayStatus(server, api_token):
    url = f"http://{server}/api/internal/gateways/summary"
    auth_token = {"Authorization": f"Bearer {api_token}"}

    response = requests.get(url, headers=auth_token)

    if response.status_code == 200:
        summary_data = response.json()
        print("Resumen de información sobre los gateways internos:")
        print(summary_data)
    else:
        print("Error al obtener el resumen de información sobre los gateways internos:", response.status_code)

GetGatewayStatus(server, api_token)

# GET /api/gateways/{id} 
def GetGateways(api_token, server, gateway_id):
    url = f"http://{server}/api/gateways/{gateway_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.get(url, headers=dict(auth_token))

    if response.status_code == 200:
        gateway_data = response.json()
        return gateway_data
    else:
        print(f"Failed to get gateway data: {response.text}")
        return None

gateway_id = "{{gateway_id}}"

gateway_data = GetGateways(api_token, server, gateway_id)
if gateway_data is not None:
    print("Gateway Data:")
    print(gateway_data)

# POST /api/gateways 
def PostGateway(api_token, server, gateway_data):
    url = f"http://{server}/api/gateways/{gateway_id}"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    response = requests.post(url, json=gateway_data, headers=dict(auth_token))

    if response.status_code == 200:
            print("Gateway creado exitosamente.")
    else:
        print(f"Error al crear el gateway. Código de estado: {response.status_code}")

gateway_data = {
    "gateway": {
        "boards": [],
        "description": "NewGateway",
        "discoveryEnabled": False,
        "gatewayProfileID": "{{gatewayProfileID}}",
        "id": "{{gateway_id}}",
        "location": {
        "accuracy": 0,
        "altitude": 273,
        "latitude": 41.64495,
        "longitude": -1.01179,
        "source": "UNKNOWN"
        },
        "metadata": {},
        "name": "NewGateway",
        "networkServerID": "{{networkServerID}}",
        "organizationID": "{{organizationID}}",
        "serviceProfileID": "{{serviceProfileID}}",
        "tags": {}
    }
}

PostGateway(api_token, server, gateway_data)

# PUT /api/gateways/{gateway.id} 
def PutGateways(server, api_token, gateway_id, gateway_body):
    url = f'http://{server}/api/gateways/{gateway_id}'
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    try:
        resp = requests.put(url, json=gateway_body, headers=dict(auth_token))
        
        if resp.status_code == 200:
            print("Gateway actualizado exitosamente.")
            gateway = resp.json()
            return gateway
        else:
            print("Error al actualizar el gateway. Código de estado:", resp.status_code)
            print("Mensaje de error:", resp.text)
            return None
    except Exception as e:
        print("Error al enviar la solicitud PUT:", str(e))
        return None

gateway_id = "{{gateway_id}}"

gateway_body = {
    "gateway": {
        "boards": [],
        "description": "NewGateway",
        "discoveryEnabled": False,
        "gatewayProfileID": "{{gatewayProfileID}}",
        "id": "{{gateway_id}}",
        "location": {
        "accuracy": 0,
        "altitude": 273,
        "latitude": 41.64495,
        "longitude": -1.01179,
        "source": "UNKNOWN"
        },
        "metadata": {},
        "name": "NewGateway",
        "networkServerID": "{{networkServerID}}",
        "organizationID": "{{organizationID}}",
        "serviceProfileID": "{{serviceProfileID}}",
        "tags": {}
    }
}

gateway_info = PutGateways(server, api_token, gateway_id, gateway_body)
if gateway_info:
    print("Información del gateway actualizado:")
    print(gateway_info)

# DELETE /api/gateways/{id} 
def DeleteGateway(gateway_id, server, api_token):
    url = f"http://{server}/api/gateways/{gateway_id}"

    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    try:
        # Enviar la solicitud DELETE para eliminar el gateway
        response = requests.delete(url, headers=dict(auth_token))
        
        # Verificar el estado de la respuesta
        if response.status_code == 200:
            print(f"Gateway {gateway_id} eliminado correctamente.")
        else:
            print(f"Error al eliminar el gateway {gateway_id}. Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar la solicitud DELETE: {str(e)}")

gateway_id = "{{gateway_id}}"

DeleteGateway(gateway_id, server, api_token)

# GET /api/gateways/{gateway_id}/frames 
def GetGatewayFrames(gateway_id, server, api_token):
    auth_token = [("authorization", "Bearer %s" % api_token)]
    try:
        url = f'http://{server}/api/gateways/{gateway_id}/frames'
        resp = requests.get(url, headers=dict(auth_token))
        if resp.status_code == 200:
            frames = resp.json()
            print("Frames obtenidos exitosamente:")
            print(frames)
        else:
            print("Error al obtener frames. Código de estado:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print("Se produjo un error:", e)

gateway_id = "{{gateway_id}}"

GetGatewayFrames(gateway_id, server, api_token)

# POST /api/gateways/{gateway_id}/generate-certificate 
def PostGatewayGenerateCertificate(server, api_token, gateway_id):
    url = f"http://{server}/api/gateways/{gateway_id}/generate-certificate"
    auth_token = [("authorization", "Bearer %s" % api_token)]

    try:
        response = requests.post(url, headers=dict(auth_token))
        if response.status_code == 200:
            certificate_data = response.json()
            return certificate_data
        else:
            print(f"Error al generar el certificado para el gateway {gateway_id}. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al enviar la solicitud para generar el certificado: {str(e)}")
        return None

gateway_id = "{{gateway_id}}"

certificate_data = PostGatewayGenerateCertificate(server, api_token, gateway_id)
if certificate_data:
    print("Certificado generado exitosamente:")
    print(certificate_data)

# get /api/gateways/{gateway_id}/pings/last 
def GetGatewayPings():    
    url = f"http://{server}/api/gateways/{gateway_id}/pings/last"
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    response = requests.get(url, headers=dict(auth_token))

    if response.status_code == 200:
        last_ping_data = response.json()
        print("Última señal del gateway:")
        print(last_ping_data)
    else:
        print("Error al realizar la solicitud:", response.status_code)

gateway_id =  "{{gateway_id}}"

GetGatewayPings()

# GET /api/gateways/{gateway_id}/stats 
def GetGatewayStats():
    gateway_data = {
    "gateway_id": "{{gateway_id}}",
    "interval": "minute",
    "startTimestamp": "2024-04-30T09:12:09.358Z",  
    "endTimestamp": "2024-04-30T10:12:09.358Z",  
    }

    gateway_id = gateway_data["gateway_id"]
    interval = gateway_data["interval"]
    startTimestamp = gateway_data["startTimestamp"]
    endTimestamp = gateway_data["endTimestamp"]
    
    auth_token = [("authorization", "Bearer %s" % api_token)]

    try:
        url = f'http://{server}/api/gateways/{gateway_id}/stats?interval={interval}&startTimestamp={startTimestamp}&endTimestamp={endTimestamp}'
        resp = requests.get(url, headers=dict(auth_token))

        if resp.status_code == 200:
            gateway_stats = resp.json()
            print("Información de estadísticas del gateway dentro del intervalo de tiempo:")
            print(gateway_stats)
        else:
            print("Error al obtener las estadísticas del gateway. Código de estado:", resp.status_code)
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)

GetGatewayStats()