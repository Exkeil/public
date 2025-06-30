import logging

from aiomisc.service.cron import CronService
from dishka.async_container import AsyncContainer

from bitrix_downloader.presentors.scheduler.downloader import download

log = logging.getLogger(__name__)


class DownloaderService(CronService):
    __required__ = ("cron_spec", "container")

    cron_spec: str
    container: AsyncContainer

    async def start(self) -> None:
        self.register(self.download, spec=self.cron_spec)
        await super().start()

    async def download(self) -> None:
        await download(container=self.container)
