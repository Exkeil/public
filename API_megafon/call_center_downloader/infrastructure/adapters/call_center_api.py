import json
from typing import Any, List, Tuple
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from yarl import URL
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from call_center_downloader.domains.call_center.models import APIResponse, AuthResponse
from call_center_downloader.domains.call_center.repositories.call_center import ICallCenterRepository


class CallCenterAPIClient(ICallCenterRepository):
    def __init__(
        self, session: ClientSession, base_url: URL, username: str, password: str, domain_id: int
    ):
        self.session = session
        self.base_url = base_url
        self.username = username
        self.password = password
        self.domain_id = domain_id

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(ClientError),
    )
    async def authenticate(self) -> str:
        payload = {
            "action": "auth",
            "obj": "User",
            "action_id": "auth_123",
            "params": {"login": self.username, "password": self.password},
        }
        async with self.session.post(self.base_url, json=payload, ssl=False) as response:
            response.raise_for_status()
            data = APIResponse(**(await response.json()))
            if data.code == 200 and data.body:
                auth_data = AuthResponse(**data.body)
                return auth_data.token
            raise ValueError(f"Ошибка аутентификации: код {data.code}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(ClientError),
    )
    async def fetch_object_data(
        self, obj_name: str, time_filter: bool, token: str, limit: int, offset: int
    ) -> Tuple[List[dict], int]:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "action": "list",
            "obj": obj_name,
            "action_id": f"list_{obj_name.lower()}",
            "params": {"domain_id": self.domain_id},
            "limit": limit,
            "offset": offset,
        }
        if time_filter:
            payload["filter"] = {
                "field_list": [
                    {"field": "dt", "condition_type": 5, "value": 1704067200}
                ],
                "type": 0,
            }
        async with self.session.post(
            self.base_url, json=payload, headers=headers, ssl=False
        ) as response:
            response.raise_for_status()
            data = APIResponse(**(await response.json()))
            records = data.list or data.body or []
            total = data.total_count or len(records)
            return records, total