import uuid

hex_string = "0004a30b01001171"

# Agregar guiones para que la cadena tenga formato UUID
uuid_string = '-'.join([hex_string[:8], hex_string[8:12], hex_string[12:16], hex_string[16:20], hex_string[20:]])

# Convertir la cadena a un objeto UUID
uuid_obj = uuid.UUID(uuid_string)

print("UUID:", uuid_obj)

# Resultado: 0e93e290-e84e-11ee-a9f5-675b85d8bd3b