import requests
import pandas as pd
import os


from dotenv import load_dotenv


load_dotenv()

TALANTICS_API_KEY = os.getenv("TALANTICS_API_KEY")
BASE_URL = os.getenv("BASE_URL")
HEADERS = {"Authorization": f"Bearer {TALANTICS_API_KEY}"}

def fetch_candidates_from_api():
    url = f"{BASE_URL}/candidates"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("results", []):
        candidate = {
            "age": item.get("age", None),
            "experience_years": item.get("experience_years", None),
            "profession": item.get("profession", "Unknown"),
            "salary_expectation": item.get("salary_expectation", None),
            "city": item.get("city", "Unknown"),
            "education_level": item.get("education_level", "Unknown"),
            "num_prev_jobs": item.get("num_prev_jobs", 0),
            "num_interviews": item.get("num_interviews", 0),
            "was_hired": item.get("was_hired", 0)  # если нет — 0
        }
        results.append(candidate)

    df = pd.DataFrame(results)
    df.to_csv("data/raw/candidates.csv", index=False)
    return df

if __name__ == "__main__":
    df = fetch_candidates_from_api()
    print(df.head())
