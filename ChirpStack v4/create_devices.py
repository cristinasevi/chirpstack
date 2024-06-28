import pandas as pd
import requests

# Configuración del servidor y token API
server = "localhost:8090"
api_token = "{{token_chirpstack}}"

# Función para enviar la solicitud POST y crear el dispositivo
def PostDevice(server, api_token, device_data):
    url = f"http://{server}/api/devices"
    headers = {
        "accept": "application/json",
        "Grpc-Metadata-Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=device_data, headers=headers)
        if response.status_code == 200:
            print(f"Dispositivo {device_data['device']['devEui']} agregado correctamente.")
        else:
            print(f"Error al agregar el dispositivo {device_data['device']['devEui']}. Código de estado: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al enviar la solicitud POST para {device_data['device']['devEui']}: {str(e)}")

# Función para leer el archivo Excel y crear los dispositivos
def create_devices_from_excel(xlsx_file, start_row, end_row):
    try:
        # Leer el archivo Excel
        data = pd.read_excel(xlsx_file)
        data = data.astype(str)  # Convertir todas las columnas a cadenas
        for row_index, row in data.iterrows():
            if start_row <= row_index + 1 <= end_row:
                try:
                    if len(row) >= 3:
                        dev_eui = row.iloc[2][3:19]  # Obtener el devEUI desde la tercera columna

                        # Validar que los datos son correctos
                        if len(dev_eui) != 16:
                            print(f"Datos inválidos en la fila {row_index + 1}: devEUI incorrecto")
                            continue

                        # Crear datos del dispositivo
                        device_data = {
                            "device": {
                                "devEui": dev_eui,
                                "name": dev_eui,
                                "applicationId": "{{applicationId}}",
                                "description": "Lo cree automaticamente",
                                "deviceProfileId": "{{deviceProfileId}}",  
                                "isDisabled": False,
                                "skipFcntCheck": True,
                                "tags": {},
                                "variables": {}
                            }
                        }

                        # Llamar a la función para crear el dispositivo
                        PostDevice(server, api_token, device_data)
                    else:
                        print(f"Error: No hay suficientes columnas en la fila {row_index + 1}.")
                except IndexError as e:
                    print(f"Error en la fila {row_index + 1}: {e}")
                    continue
    except FileNotFoundError:
        print(f"El archivo {xlsx_file} no se encontró.")

# Definir los parámetros para la activación de dispositivos
xlsx_file = "prueba.xlsx"
start_row = 569
end_row = 600

# Llamar a la función para crear dispositivos desde el archivo Excel
create_devices_from_excel(xlsx_file, start_row, end_row)