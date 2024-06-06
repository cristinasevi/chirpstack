import uuid

hex_string = "0004a30b00f98573"

# Pad the hex string to ensure it is 32 characters long
padded_hex_string = hex_string.ljust(32, '0')

# Add dashes to format the padded hex string as a UUID
uuid_string = '-'.join([padded_hex_string[:8], padded_hex_string[8:12], padded_hex_string[12:16], padded_hex_string[16:20], padded_hex_string[20:]])

# Convert the string to a UUID object
uuid_obj = uuid.UUID(uuid_string)

print("UUID:", uuid_obj)

# Resultado: 0004a30b-00f9-8573-0000-000000000000
