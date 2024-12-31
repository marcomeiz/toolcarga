from workalendar.europe.spain import Catalonia
from datetime import datetime, date
import pandas as pd

def calcular_dias_laborables(inicio, fin):
    """Calcula los días laborables entre dos fechas, excluyendo festivos"""
    cal = Catalonia()
    dias = pd.date_range(start=inicio, end=fin, freq='B')  # Días laborables (excluye sábados y domingos)
    dias_laborables = [dia for dia in dias if not cal.is_holiday(dia)]
    return len(dias_laborables)