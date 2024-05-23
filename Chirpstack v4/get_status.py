import requests

server = "localhost:8090"
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjJjYmZjOWIxLWIzZDgtNDU3NC1hMTJjLWVmNzhiYWIwZTAyOCIsInR5cCI6ImtleSJ9.4Qzq6v_KcOvKEgXzewMNbRPS4uxE-pwcGKNjemDsRrk"


def GetDeviceStatus(server, api_token):
    url = f"http://{server}/api/device/status"
    headers = {
        "accept": "application/json",
        "Grpc-Metadata-Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        summary_data = response.json()
        print("Resumen de información sobre los dispositivos internos:")
        print(summary_data)
    else:
        print("Error al obtener el resumen de información sobre los dispositivos internos:", response.status_code)

GetDeviceStatus(server, api_token)


def GetGatewayStatus(server, api_token):
    url = f"http://{server}/api/gateways/status"
    headers = {
        "accept": "application/json",
        "Grpc-Metadata-Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        gateway_stats = response.json()
        print("Resumen de información sobre los gateways internos:")
        print(gateway_stats)
    else:
        print("Error al obtener el resumen de información sobre los gateways internos:", response.status_code)

GetGatewayStatus(server, api_token)