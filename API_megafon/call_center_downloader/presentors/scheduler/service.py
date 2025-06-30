import logging
from aiomisc import Service
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer
from call_center_downloader.domains.call_center.services.call_center import CallCenterService

log = logging.getLogger(__name__)


class DownloaderService(Service):
    def __init__(self, cron_spec: str, container: AsyncContainer):
        super().__init__()
        self.cron_spec = cron_spec
        self.container = container
        self.scheduler = AsyncIOScheduler()

    async def start(self) -> None:
        async with self.container() as request_container:
            service: CallCenterService = await request_container.get(CallCenterService)
            self.scheduler.add_job(
                service.download_all,
                "cron",
                **self.parse_cron(self.cron_spec),
            )
        self.scheduler.start()
        log.info("Сервис загрузки запущен с cron-выражением: %s", self.cron_spec)

    async def stop(self, exception: Exception | None = None) -> None:
        self.scheduler.shutdown()
        log.info("Сервис загрузки остановлен")

    @staticmethod
    def parse_cron(cron_spec: str) -> dict:
        minute, hour, day, month, day_of_week = cron_spec.split()
        return {
            "minute": minute,
            "hour": hour,
            "day": day,
            "month": month,
            "day_of_week": day_of_week,
        }