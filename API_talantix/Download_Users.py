import requests
import json
import csv
import os

from get_domain import base_url
from get_domain import token
from get_domain import domain_id

requests.packages.urllib3.disable_warnings()

data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def send_request(payload):
    response = requests.post(
        base_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        data=json.dumps(payload),
        verify=False
    )
    return response.json()


domain_users_payload = {
    "action": "list",
    "obj": "DomainUser",
    "action_id": "123",
    "params": {
        "domain_id": domain_id
    }
}
domain_users_data = send_request(domain_users_payload)
with open(os.path.join(data_dir, "domain_users.json"), "w", encoding="utf-8") as f:
    json.dump(domain_users_data, f, ensure_ascii=False, indent=2)

domain_users_count = len(domain_users_data.get("list", []))



system_users_payload = {
    "action": "list",
    "obj": "User",
    "action_id": "124",
    "params": {}
}
system_users_data = send_request(system_users_payload)
with open(os.path.join(data_dir, "system_users.json"), "w", encoding="utf-8") as f:
    json.dump(system_users_data, f, ensure_ascii=False, indent=2)

system_users_count = len(system_users_data.get("list", []))


user_id_to_info = {
    user["id"]: {
        "first_name": user.get("name", "Unknown"),
        "last_name": user.get("surname", "Unknown"),
        "login": user.get("login", "Unknown"),
        "email": user.get("email", "Unknown"),
        "role_id": user.get("role_id", "Unknown"),
        "user_status": user.get("status", "Unknown"),
        "numbers": ", ".join(user.get("numbers", [])) if user.get("numbers") else "None"
    } for user in system_users_data.get("list", [])
}

missing_ids = [user["user_id"] for user in domain_users_data["list"] if user["user_id"] not in user_id_to_info]


additional_users = []
for user_id in missing_ids[:10]:
    payload = {
        "action": "get",
        "obj": "User",
        "action_id": f"125_{user_id}",
        "params": {"id": user_id}
    }
    response = send_request(payload)
    if response.get("code") == 200 and response.get("list"):
        additional_users.append(response["list"][0])
    else:
        print(f"Ошибка для user_id {user_id}: {response}")

if additional_users:
    system_users_data["list"].extend(additional_users)
    with open(os.path.join(data_dir, "system_users.json"), "w", encoding="utf-8") as f:
        json.dump(system_users_data, f, ensure_ascii=False, indent=2)
    print(f"Добавлено {len(additional_users)} системных пользователей")
    system_users_count = len(system_users_data.get("list", []))
    print(f"Обновлено системных пользователей (User): {system_users_count}")

user_id_to_info = {
    user["id"]: {
        "first_name": user.get("name", "Unknown"),
        "last_name": user.get("surname", "Unknown"),
        "login": user.get("login", "Unknown"),
        "email": user.get("email", "Unknown"),
        "role_id": user.get("role_id", "Unknown"),
        "user_status": user.get("status", "Unknown"),
        "numbers": ", ".join(user.get("numbers", [])) if user.get("numbers") else "None"
    } for user in system_users_data.get("list", [])
}

merged_users = []
matched_count = 0
not_found_count = 0

for domain_user in domain_users_data.get("list", []):
    user_id = domain_user["user_id"]
    user_info = user_id_to_info.get(user_id, {
        "first_name": "Not Found",
        "last_name": "Not Found",
        "login": "Not Found",
        "email": "Not Found",
        "role_id": "Not Found",
        "user_status": "Not Found",
        "numbers": "Not Found"
    })
    agent = domain_user.get("agent", {})
    merged_users.append({
        "id": domain_user["id"],
        "uid": domain_user["uid"],
        "pin": domain_user["pin"],
        "first_name": user_info["first_name"],
        "last_name": user_info["last_name"],
        "login": user_info["login"],
        "email": user_info["email"],
        "role_id": user_info["role_id"],
        "user_status": user_info["user_status"],
        "agent_status_id": agent.get("status_id", "Not Set") if agent else "Not Set",
        "group_outbound": ", ".join(map(str, domain_user["group_outbound"])),
        "group_interception": ", ".join(map(str, domain_user["group_interception"])),
        "group_eavesdrop": ", ".join(map(str, domain_user["group_eavesdrop"])),
        "numbers": user_info["numbers"]
    })
    if user_info["first_name"] != "Not Found":
        matched_count += 1
    else:
        not_found_count += 1

with open(os.path.join(data_dir, "merged_users.csv"), "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "ID", "UID", "PIN", "First Name", "Last Name", "Login", "Email",
        "Role ID", "User Status", "Agent Status ID", "Group Outbound",
        "Group Interception", "Group Eavesdrop", "Numbers"
    ])
    for user in merged_users:
        writer.writerow([
            user["id"],
            user["uid"],
            user["pin"],
            user["first_name"],
            user["last_name"],
            user["login"],
            user["email"],
            user["role_id"],
            user["user_status"],
            user["agent_status_id"],
            user["group_outbound"],
            user["group_interception"],
            user["group_eavesdrop"],
            user["numbers"]
        ])

for user in merged_users[:10]:
    print(f"ID: {user['id']}, UID: {user['uid']}, PIN: {user['pin']}, "
          f"First Name: {user['first_name']}, Last Name: {user['last_name']}, "
          f"Login: {user['login']}, Email: {user['email']}, Role ID: {user['role_id']}, "
          f"User Status: {user['user_status']}, Agent Status ID: {user['agent_status_id']}, "
          f"Group Outbound: {user['group_outbound']}, Group Interception: {user['group_interception']}, "
          f"Group Eavesdrop: {user['group_eavesdrop']}, Numbers: {user['numbers']}")