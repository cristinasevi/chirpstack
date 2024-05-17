import datetime

# Definir la fecha y hora en UTC
fecha_hora_utc = datetime.datetime(2024, 5, 16, 15, 41)

# Obtener la marca de tiempo en segundos desde la época Unix
timestamp_seconds = datetime.datetime.timestamp(fecha_hora_utc)

# Convertir la marca de tiempo a milisegundos
timestamp_millis = int(timestamp_seconds * 1000)

print("Marca de tiempo para el 16 de mayo de 2024 a las 15:41h (UTC):", timestamp_millis)

# Resultado: 1715866860000
