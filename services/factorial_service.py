import requests
from config.settings import FACTORIAL_API_KEY, FACTORIAL_BASE_URL

HEADERS = {
    "accept": "application/json",
    "x-api-key": FACTORIAL_API_KEY,
}

def obtener_tipos_ausencia():
    """Obtiene los tipos de ausencia desde Factorial"""
    url = f"{FACTORIAL_BASE_URL}/resources/timeoff/leave_types"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()  # Lanza una excepción si la respuesta no es 200
    tipos = response.json().get('data', [])
    return {tipo['id']: tipo['translated_name'] for tipo in tipos}

def obtener_ausencias():
    """Obtiene todas las ausencias desde Factorial"""
    url = f"{FACTORIAL_BASE_URL}/resources/timeoff/leaves"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get('data', [])