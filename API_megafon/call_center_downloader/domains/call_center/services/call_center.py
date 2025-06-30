import logging
from typing import List

from call_center_downloader.domains.call_center.repositories.call_center import ICallCenterRepository
from call_center_downloader.infrastructure.storage.csv_storage import CSVStorage

log = logging.getLogger(__name__)


class CallCenterService:
    def __init__(self, repository: ICallCenterRepository, storage: CSVStorage, domain_id: int):
        self.repository = repository
        self.storage = storage
        self.domain_id = domain_id
        self.objects = [
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
            {"obj_name": "DomainAgent", "time_filter": False},
            {"obj_name": "DomainAgentStatus", "time_filter": True},
            {"obj_name": "DomainUser", "time_filter": False},
            {"obj_name": "DomainRole", "time_filter": False},
            {"obj_name": "DomainPermission", "time_filter": False},
            {"obj_name": "DomainVoiceMail", "time_filter": True},
            {"obj_name": "DomainNotify", "time_filter": True},
            {"obj_name": "DomainCRMEvent", "time_filter": True},
            {"obj_name": "DomainConferenceCdr", "time_filter": True},
            {"obj_name": "DomainConferenceMemberCDR", "time_filter": True},
            {"obj_name": "DomainFax", "time_filter": True},
            {"obj_name": "DomainLocalStream", "time_filter": False},
            {"obj_name": "SystemAudioFile", "time_filter": False},
            {"obj_name": "SystemFileStorage", "time_filter": False},
            {"obj_name": "SystemLocalStream", "time_filter": False},
        ]

    async def download_all(self) -> None:
        token = await self.repository.authenticate()
        for obj in self.objects:
            await self.download_object(obj["obj_name"], obj["time_filter"], token)

    async def download_object(self, obj_name: str, time_filter: bool, token: str) -> None:
        log.info(f"Загрузка {obj_name} (time_filter={time_filter})...")
        limit = 1000
        offset = 0
        all_records = []

        while True:
            records, total = await self.repository.fetch_object_data(
                obj_name=obj_name,
                time_filter=time_filter,
                token=token,
                limit=limit,
                offset=offset,
            )
            all_records.extend(records)
            log.info(
                f"{obj_name}: Получено {len(records)} записей, всего {total}, смещение {offset}"
            )
            if records and offset == 0 and records[0]:
                log.info(f"Поля в {obj_name}: {list(records[0].keys())}")
            if len(records) < limit or offset >= total:
                break
            offset += limit

        if all_records:
            self.storage.save_to_csv(obj_name, all_records)
            log.info(f"Сохранено {len(all_records)} записей для {obj_name}")
        else:
            log.info(f"Нет данных для {obj_name}")