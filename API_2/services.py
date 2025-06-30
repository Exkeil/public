import csv
import json
import os
import asyncio
from typing import List, Dict, Any
from aiohttp import ClientSession
from aiohttp_retry import RetryClient, ExponentialRetry
from dependency_injector import containers

from config import Config

class CSVRepository:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def save_to_csv(self, obj_name: str, data: List[Dict[str, Any]]):
        if not data:
            return
        cleaned_data = [
            {k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else "" if v is None else str(v)
             for k, v in record.items()}
            for record in data
        ]
        csv_file = os.path.join(self.output_dir, f"{obj_name.lower()}.csv")
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cleaned_data[0].keys())
            writer.writeheader()
            writer.writerows(cleaned_data)

class APIService:
    def __init__(self, base_url: str, domain_id: int):
        self.base_url = base_url
        self.domain_id = domain_id

    async def fetch_object(
        self, session: RetryClient, token: str, obj_name: str, time_filter: bool, time_filter_start: int,
        limit: int = 1000, offset: int = 0
    ) -> List[Dict[str, Any]]:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "action": "list",
            "obj": obj_name,
            "action_id": f"list_{obj_name.lower()}",
            "params": {"domain_id": self.domain_id},
            "limit": limit,
            "offset": offset
        }
        if time_filter:
            payload["filter"] = {
                "field_list": [{"field": "dt", "condition_type": 5, "value": time_filter_start}],
                "type": 0
            }
        async with session.post(self.base_url, json=payload, headers=headers, ssl=False) as response:
            data = await response.json()
            return data.get("list", data.get("body", []))

class DownloaderService:
    def __init__(self, cron_spec: str, container: containers.DynamicContainer):
        self.cron_spec = cron_spec
        self.container = container

    async def run(self):
        api_service = self.container.api_service()
        csv_repository = self.container.csv_repository()
        auth_service = self.container.auth_service()
        config = self.container.config()

        objects = [
            {"obj_name": "DomainUser", "time_filter": False},
            {"obj_name": "DomainAgent", "time_filter": False},
            {"obj_name": "DomainAgentStatus", "time_filter": True},
            {"obj_name": "DomainRole", "time_filter": False},
            {"obj_name": "DomainPermission", "time_filter": False},
            {"obj_name": "DomainDPEResult", "time_filter": True},
            {"obj_name": "DomainQueueCDR", "time_filter": True},
            {"obj_name": "DomainQueueMemberCDR", "time_filter": True},
            {"obj_name": "DomainDialerBatch", "time_filter": False},
            {"obj_name": "DomainDialerContact", "time_filter": True},
            {"obj_name": "DomainDialerAttempt", "time_filter": True},
            {"obj_name": "DomainDialerBatchDPQueue", "time_filter": False},
            {"obj_name": "DomainDialerBatchDPPlayback", "time_filter": False},
            {"obj_name": "DomainDialerBatchDPDP", "time_filter": False},
            {"obj_name": "DomainDialerBatchDPCheck", "time_filter": False},
            {"obj_name": "DomainDialerBatchDPQuestions", "time_filter": False},
            {"obj_name": "DomainAutoDialingBatchSchedule", "time_filter": False},
            {"obj_name": "GSSystem", "time_filter": False}
        ]

        retry_options = ExponentialRetry(attempts=3, start_timeout=1.0, factor=2.0)
        async with ClientSession() as session, RetryClient(client_session=session, retry_options=retry_options) as retry_session:
            token = await auth_service.get_token(session)
            for obj in objects:
                obj_name = obj["obj_name"]
                time_filter = obj["time_filter"] and config.time_filter_enabled
                all_data = []
                offset = 0
                limit = 1000
                while True:
                    records = await api_service.fetch_object(
                        retry_session, token, obj_name, time_filter, config.time_filter_start, limit, offset
                    )
                    all_data.extend(records)
                    if len(records) < limit:
                        break
                    offset += limit
                    await asyncio.sleep(0.5)
                await csv_repository.save_to_csv(obj_name, all_data)