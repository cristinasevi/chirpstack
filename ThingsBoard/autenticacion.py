import requests

# Datos de autenticación
username = "info@inartecnologias.es"
password = "Inar.2019"

# Endpoint de autenticación
login_endpoint = "http://thingsboard.chemik.es/api/auth/login"

# Datos de autenticación
auth_data = {
    "username": username,
    "password": password
}

try:
    # Realizar la solicitud de autenticación
    response = requests.post(login_endpoint, json=auth_data)

    # Verificar el código de estado de la respuesta
    if response.status_code == 200:
        # Extraer el token de acceso de la respuesta
        access_token = response.json().get("token")

        # Ahora puedes usar access_token en tus solicitudes a la API de ThingsBoard
        print("Autenticación exitosa. Token de acceso:", access_token)
    else:
        print(f"Error de autenticación. Código de estado: {response.status_code}")
        print(response.text)
        exit(1)

except Exception as e:
    print("Error al conectar con ThingsBoard para autenticación.")
    print(e)
    exit(1)
