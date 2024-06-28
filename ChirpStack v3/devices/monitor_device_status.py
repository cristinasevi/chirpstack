import requests
import time

server = "localhost:8080"
api_token = "{{token_chirpstack}}"

def obtener_status_devices(api_url, headers):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def actualizar_status_cada_minuto(api_url, headers):
    while True:
        status = obtener_status_devices(api_url, headers)
        if status:
            print(status)
        time.sleep(60)  # Espera 1 minuto antes de actualizar nuevamente

if __name__ == "__main__":
    api_url = f"http://{server}/api/internal/devices/summary"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    actualizar_status_cada_minuto(api_url, headers)