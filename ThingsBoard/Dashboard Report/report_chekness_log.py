import pandas as pd
from datetime import datetime, timedelta
import os

# Obtener la fecha de ayer
fecha_ayer = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

# Construir el nombre del archivo basado en la fecha de ayer
archivo_excel = f"/home/ckcm/Chekness_Log/Test_{fecha_ayer}.xlsx"

# Leer la segunda hoja del archivo Excel
df = pd.read_excel(archivo_excel, sheet_name='Datos_Dispo')

# Filtrar las filas donde la disponibilidad (%) sea menor o igual a 80
df_filtrado = df[df.iloc[:, 1] <= 80]

# Crear la ruta del directorio de salida si no existe
output_dir = "/home/ckcm/Report_Chekness_Log"
os.makedirs(output_dir, exist_ok=True)

# Construir el nombre del archivo de salida
output_file = os.path.join(output_dir, f"Report_{fecha_ayer}.xlsx")

# Guardar los datos filtrados en un nuevo archivo Excel
df_filtrado.to_excel(output_file, index=False)

print(f"Datos filtrados guardados en {output_file}")
