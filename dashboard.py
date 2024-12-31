import streamlit as st
import pandas as pd
from connections.factorial_connection import obtener_tipos_ausencia, obtener_ausencias
from connections.cor_connection import obtener_token_cor, obtener_tareas_cor
from utils.data_utils import calcular_dias_laborables
from datetime import datetime, date
from calendar import monthrange
from workalendar.europe.spain import Catalonia

# Configuración de la página
st.set_page_config(page_title="Resumen de Empleados por Mes", layout="wide")

# Título del dashboard
st.title("Resumen de Empleados por Mes")

# Obtener datos de Factorial
tipos_ausencia = obtener_tipos_ausencia()
ausencias = obtener_ausencias()

# Función para calcular días laborables y festivos
def calcular_dias_laborables_festivos(anio, mes):
    """Calcula los días laborables y festivos en un mes."""
    cal = Catalonia()
    _, total_dias = monthrange(anio, mes)
    dias_laborables = 0
    festivos = 0
    for dia in range(1, total_dias + 1):
        fecha = date(anio, mes, dia)
        if fecha.weekday() < 5:  # Lunes a viernes
            if cal.is_holiday(fecha):
                festivos += 1
            else:
                dias_laborables += 1
    return dias_laborables, festivos

# Función para calcular horas disponibles
def calcular_horas_disponibles(dias_laborables, horas_por_dia, vacaciones_en_dias, otras_ausencias_en_dias):
    """Calcula las horas disponibles en un mes, restando vacaciones, otras ausencias y buffer."""
    horas_totales = dias_laborables * horas_por_dia
    horas_vacaciones = vacaciones_en_dias * horas_por_dia
    horas_otras_ausencias = otras_ausencias_en_dias * horas_por_dia
    buffer = horas_totales * 0.1  # Buffer del 10%
    horas_disponibles = horas_totales - horas_vacaciones - horas_otras_ausencias - buffer
    return horas_disponibles, horas_totales, horas_vacaciones, horas_otras_ausencias, buffer

# Crear un DataFrame con el resumen de empleados por mes
def crear_resumen_empleados(ausencias, anio, mes):
    """Crea un resumen de empleados con métricas clave para un mes específico."""
    resumen = {}
    for ausencia in ausencias:
        empleado = ausencia.get("employee_full_name")
        inicio = datetime.strptime(ausencia.get("start_on"), "%Y-%m-%d")
        fin = datetime.strptime(ausencia.get("finish_on"), "%Y-%m-%d")
        tipo = tipos_ausencia.get(ausencia.get("leave_type_id"), "Desconocido")

        # Calcular días de vacaciones y otras ausencias
        if tipo == "Vacaciones":
            dias_vacaciones = calcular_dias_laborables(inicio, fin)
            dias_otras_ausencias = 0
        else:
            dias_vacaciones = 0
            dias_otras_ausencias = calcular_dias_laborables(inicio, fin)

        # Calcular horas disponibles
        horas_por_dia = 7 if mes == 8 else 8  # Agosto tiene 7 horas/día, el resto 8
        dias_laborables, festivos = calcular_dias_laborables_festivos(anio, mes)
        horas_disponibles, horas_totales, horas_vacaciones, horas_otras_ausencias, buffer = calcular_horas_disponibles(
            dias_laborables, horas_por_dia, dias_vacaciones, dias_otras_ausencias
        )

        # Agrupar por empleado
        if empleado not in resumen:
            resumen[empleado] = {
                "Colaborador": empleado,
                "Días Laborables": dias_laborables,
                "Días Festivos": festivos,
                "Horas/Día": horas_por_dia,
                "Horas Totales Mes": horas_totales,
                "Horas por Vacaciones": horas_vacaciones,
                "Horas Otras Ausencias": horas_otras_ausencias,
                "Buffer (10%)": buffer,
                "Horas Disponibles Final": horas_disponibles,
                "Horas Cargadas": 0,  # Aquí puedes añadir la lógica para obtener las horas cargadas
                "Horas Estimadas": 0,  # Aquí puedes añadir la lógica para obtener las horas estimadas
                "% Tiempo Estimado": 0,  # Aquí puedes añadir la lógica para calcular el porcentaje
            }
        else:
            resumen[empleado]["Horas por Vacaciones"] += horas_vacaciones
            resumen[empleado]["Horas Otras Ausencias"] += horas_otras_ausencias
            resumen[empleado]["Horas Disponibles Final"] = calcular_horas_disponibles(
                dias_laborables, horas_por_dia, resumen[empleado]["Horas por Vacaciones"], resumen[empleado]["Horas Otras Ausencias"]
            )[0]

    return pd.DataFrame(resumen.values())

# Seleccionar año y mes
st.header("Seleccionar Año y Mes")
anio = st.number_input("Año", min_value=2023, max_value=2100, value=2024)
mes = st.number_input("Mes", min_value=1, max_value=12, value=7)

# Generar el resumen
if st.button("Generar Resumen"):
    resumen_empleados = crear_resumen_empleados(ausencias, anio, mes)
    st.header(f"Resumen de Empleados para {mes}/{anio}")
    st.write(resumen_empleados)