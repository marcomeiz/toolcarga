from datetime import datetime
from reports.google_sheets import actualizar_google_sheets
from config.settings import FACTORIAL_API_KEY
from services.factorial_service import obtener_tipos_ausencia, obtener_ausencias
from utils.data_utils import calcular_dias_laborables
import pandas as pd
from config.settings import SPREADSHEET_ID

print(f"La API Key de Factorial es: {FACTORIAL_API_KEY}")

try:
    tipos_ausencia = obtener_tipos_ausencia()
    print("\nTipos de ausencia disponibles:")
    for id_tipo, nombre in tipos_ausencia.items():
        print(f"ID: {id_tipo}, Nombre: {nombre}")

    ausencias = obtener_ausencias()
    print(f"\nTotal de ausencias encontradas: {len(ausencias)}")

    if ausencias:  # Si hay ausencias
        primera = ausencias[0]
        print("\nPrimera ausencia como ejemplo:")
        print(f"Empleado: {primera.get('employee_full_name')}")
        print(f"Inicio: {primera.get('start_on')}")
        print(f"Fin: {primera.get('finish_on')}")
        print(f"Tipo: {tipos_ausencia.get(primera.get('leave_type_id'), 'Desconocido')}")

        # Calcular días laborables
        inicio = datetime.strptime(primera.get('start_on'), "%Y-%m-%d")
        fin = datetime.strptime(primera.get('finish_on'), "%Y-%m-%d")
        dias_laborables = calcular_dias_laborables(inicio, fin)
        print(f"\nDías laborables para la ausencia: {dias_laborables}")

    # Crear un DataFrame con las ausencias
    datos_ausencias = []
    for ausencia in ausencias:
        datos_ausencias.append({
            "Empleado": ausencia.get("employee_full_name"),
            "Inicio": ausencia.get("start_on"),
            "Fin": ausencia.get("finish_on"),
            "Tipo": tipos_ausencia.get(ausencia.get("leave_type_id"), "Desconocido")
        })

    df_ausencias = pd.DataFrame(datos_ausencias)

    # Actualizar Google Sheets
    actualizar_google_sheets(df_ausencias, SPREADSHEET_ID, "Ausencias")

except Exception as e:
    print(f"\nError al obtener los datos: {e}")