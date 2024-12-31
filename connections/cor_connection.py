import requests
from config.settings import COR_API_KEY, COR_CLIENT_SECRET, COR_BASE_URL
import base64

def obtener_token_cor():
    """Obtiene el token de acceso usando client_credentials."""
    url_token = f"{COR_BASE_URL}/v1/oauth/token?grant_type=client_credentials"
    basic_creds = base64.b64encode(f"{COR_API_KEY}:{COR_CLIENT_SECRET}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": "Basic " + basic_creds,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url_token, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")

def obtener_tareas_cor(access_token, page=1, per_page=10):
    """Obtiene las tareas de COR, paginadas."""
    url_tasks = f"{COR_BASE_URL}/v1/tasks?page={page}&perPage={per_page}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url_tasks, headers=headers)
    response.raise_for_status()
    return response.json()