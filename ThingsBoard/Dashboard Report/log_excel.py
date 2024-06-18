import pandas as pd
from datetime import datetime, timedelta

# Obtener la fecha de ayer
fecha_ayer = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

# Construir el nombre del archivo basado en la fecha de ayer
archivo_excel = f"/home/ckcm/Chekness_Log/Test_{fecha_ayer}.xlsx"

# Leer la segunda hoja del archivo Excel
df = pd.read_excel(archivo_excel, sheet_name='Datos_Dispo')

# Filtrar las filas donde la disponibilidad (%) sea menor o igual a 80
df_filtrado = df[df.iloc[:, 1] <= 80]

# Guardar los datos filtrados en un nuevo archivo Excel llamado log_report.xlsx
df_filtrado.to_excel("/home/ckcm/Pruebas/log_report.xlsx", index=False)

print("Datos filtrados guardados en log_report.xlsx")
