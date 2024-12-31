import os
from dotenv import load_dotenv

load_dotenv()

FACTORIAL_API_KEY = os.getenv("FACTORIAL_API_KEY")
COR_API_KEY = os.getenv("COR_API_KEY")
COR_CLIENT_SECRET = os.getenv("COR_CLIENT_SECRET")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
FACTORIAL_BASE_URL = "https://api.factorialhr.com/api/2024-10-01"
COR_BASE_URL = "https://api.projectcor.com"