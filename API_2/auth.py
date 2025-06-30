import logging
from typing import Optional
from aiohttp import ClientSession

log = logging.getLogger(__name__)

class AuthService:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password

    async def get_token(self, session: ClientSession) -> Optional[str]:
        payload = {
            "action": "auth",
            "obj": "User",
            "action_id": "123",
            "params": {
                "login": self.username,
                "password": self.password
            }
        }
        try:
            async with session.post(self.base_url, json=payload, ssl=False) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 200:
                        log.info("Авторизация прошла")
                        return data["body"]["token"]
                    else:
                        log.error(f"Ошибка авторизации: код {data.get('code')}, {data.get('msg_id', 'Неизвестная ошибка')}")
                        return None
                else:
                    log.error(f"Ошибка авторизации: код {response.status}, {await response.text()}")
                    return None
        except Exception as e:
            log.error(f"Ошибка при запросе токена: {e}")
            return None