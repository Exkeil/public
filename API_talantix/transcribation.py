import requests
import json
import csv
import os


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Отключаем предупреждения SSL
requests.packages.urllib3.disable_warnings()

# Читаем call_uuid из CSV-файла
def read_call_uuids():
    call_uuids = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            call_uuid = row.get("call_uuid")
            if call_uuid:
                call_uuids.append(call_uuid)
    print(f"Найдено {len(call_uuids)} call_uuid в {csv_file}")
    return call_uuids

# Получаем токен авторизации
def get_token():
    payload = {
        "action": "auth",
        "obj": "User",
        "action_id": "123",
        "params": {
            "login": username,
            "password": password
        }
    }
    response = requests.post(base_url, json=payload, verify=False)
    data = response.json()
    print("Авторизация успешна!")
    return data["body"]["token"]

# Получаем транскрибацию для одного call_uuid
def get_transcription(call_uuid, token):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {
        "action": "get_dialog",
        "obj": "DomainDPEResult",
        "action_id": f"get_dialog_{call_uuid}",
        "params": {
            "call_uuid": call_uuid,
            "domain_id": domain_id
        }
    }

    print(f"Запрашиваю транскрибацию для call_uuid: {call_uuid}")
    response = requests.post(base_url, json=payload, headers=headers, verify=False)
    data = response.json()

    if data.get("code") == 200:
        dialog = data.get("body", {}).get("dialog", {})
        if dialog:
            print(f"Получен диалог для {call_uuid}")
            return dialog
        else:
            print(f"Диалог для {call_uuid} пустой")
            return {}
    else:
        print(f"Ошибка для {call_uuid}: код {data.get('code')}")
        return {}

# Сохраняем транскрибацию в JSON-файл
def save_transcription(call_uuid, dialog):
    output_file = os.path.join(output_dir, f"{call_uuid}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dialog, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {output_file}")

# Основной процесс
token = get_token()
call_uuids = read_call_uuids()

for call_uuid in call_uuids:
    dialog = get_transcription(call_uuid, token)
    if dialog:
        save_transcription(call_uuid, dialog)
    else:
        print(f"Пропускаю {call_uuid} — нет данных")

print("Все транскрибации обработаны!")
