import requests
import json
import configparser

# Cargar la configuración desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')

chirpstack_server = "localhost:8080"
thingsboard_server = config['CONFIG']['thingsboard_server']
username = config['CONFIG']['username']
password = config['CONFIG']['password']
api_token = config['CONFIG']['api_token']
device_profile_id = config['CONFIG']['device_profile_id']
device_limit = int(config['CONFIG']['device_limit'])

def activate_integration():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    integration_data = {
        "server": thingsboard_server
    }
    try:
        # Activar la integración en ChirpStack
        response = requests.post(f"http://{chirpstack_server}/api/integration/thingsboard", headers=headers, json=integration_data)
        response.raise_for_status()
        print("Integration activated with ThingsBoard")
    except requests.exceptions.RequestException as e:
        print("Error activating integration:", e)

if __name__ == "__main__":
    activate_integration()
