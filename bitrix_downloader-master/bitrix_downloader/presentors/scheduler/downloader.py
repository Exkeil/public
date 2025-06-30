import logging

from dishka import AsyncContainer

from bitrix_downloader.domains.bitrix.services.bitrix import BitrixService

log = logging.getLogger(__name__)


async def download(*, container: AsyncContainer) -> None:
    async with container() as container:
        bitrix_service = await container.get(BitrixService)
        try:
            await bitrix_service.download_ad_mass_recruitment_data()
        except Exception as e:
            log.exception("Ad mass_recruitment downloader error: %s", e)
        try:
            await bitrix_service.download_ad_call_center_data()
        except Exception as e:
            log.exception("Ad call_center downloader error: %s", e)
        try:
            await bitrix_service.download_sng_data()
        except Exception as e:
            log.exception("Sng downloader error: %s", e)
        try:
            await bitrix_service.download_world_data()
        except Exception as e:
            log.exception("World downloader error: %s", e)
        try:
            await bitrix_service.download_ad_world_data()
        except Exception as e:
            log.exception("Ad world downloader error: %s", e)
        try:
            await bitrix_service.download_ad_sng_data()
        except Exception as e:
            log.exception("Ad sng downloader error: %s", e)
        try:
            await bitrix_service.download_mass_selection()
        except Exception as e:
            log.exception("Mass selection downloader error: %s", e)
