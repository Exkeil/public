import requests
from dotenv import load_dotenv
import os

load_dotenv()

TALANTICS_API_KEY = os.getenv("TALANTICS_API_KEY")
BASE_URL = os.getenv("BASE_URL")
HEADERS = {"Authorization": f"Bearer {TALANTICS_API_KEY}"}

def fetch_candidates():
    url = f"{BASE_URL}/candidates"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return [item["description"] for item in data.get("results", []) if "description" in item]

def fetch_vacancies():
    url = f"{BASE_URL}/vacancies"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return [item["description"] for item in data.get("results", []) if "description" in item]