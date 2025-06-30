import requests
import csv

# Данные для авторизации
base_url = "https://lk-al.cprt.su/api/"
username = "admin@callcenter-al.cprt.su"
password = "RNEvCAkt"

# 1. Авторизация
auth_payload = {
    "action": "auth",
    "obj": "User",
    "action_id": "123",
    "params": {
        "login": username,
        "password": password
    }
}

try:
    auth_response = requests.post(base_url, json=auth_payload)
    auth_response.raise_for_status()  # Проверка на ошибки
    auth_data = auth_response.json()

    if auth_data.get("code") != 200:
        raise Exception(f"Ошибка авторизации: {auth_data}")

    auth_token = auth_data["body"]["token"]
    print("Авторизация успешна. Токен получен.")
except Exception as e:
    print(f"Ошибка при авторизации: {e}")
    exit()

# 2. Получение списка тарифов
tariff_payload = {
    "action": "list",
    "obj": "Tariff",
    "action_id": "123",
    "params": {
        "domain_id": 2
    }
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {auth_token}"
}

try:
    tariff_response = requests.post(base_url, json=tariff_payload, headers=headers)
    tariff_response.raise_for_status()
    tariff_data = tariff_response.json()

    if tariff_data.get("code") != 200:
        raise Exception(f"Ошибка при запросе тарифов: {tariff_data}")

    tariffs = tariff_data.get("body", [])
    print(f"Получено {len(tariffs)} тарифов.")
except Exception as e:
    print(f"Ошибка при получении тарифов: {e}")
    exit()

# 3. Сохранение в CSV
csv_file = "tariffs.csv"
csv_columns = ["id", "name", "is_base", "mode", "status", "billing_id"]

try:
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()

        for tariff in tariffs:
            # Выбираем только нужные поля (можно добавить другие)
            row = {
                "id": tariff.get("id"),
                "name": tariff.get("name"),
                "is_base": tariff.get("is_base"),
                "mode": tariff.get("mode"),
                "status": tariff.get("status"),
                "billing_id": tariff.get("billing_id")
            }
            writer.writerow(row)

    print(f"Данные сохранены в файл: {csv_file}")
except Exception as e:
    print(f"Ошибка при сохранении в CSV: {e}")