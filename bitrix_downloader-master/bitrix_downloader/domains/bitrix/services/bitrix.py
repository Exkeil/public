import logging

from bitrix_downloader.domains.bitrix.repositories.bitrix import IBitrixRepository
from bitrix_downloader.infrastructure.adapters.bitrix import BitrixClient

log = logging.getLogger(__name__)


class BitrixService:
    __bitrix_repository: IBitrixRepository
    __bitrix_client: BitrixClient
    __sng_entity_id: int
    __world_entity_id: int
    __chunk_size: int
    __call_center_entity_id: int
    __mass_recruitment_entity_id: int

    def __init__(
        self,
        *,
        bitrix_repository: IBitrixRepository,
        bitrix_client: BitrixClient,
        sng_entity_id: int,
        world_entity_id: int,
        call_center_entity_id: int,
        mass_recruitment_entity_id: int,
        chunk_size: int,
    ) -> None:
        self.__bitrix_repository = bitrix_repository
        self.__bitrix_client = bitrix_client
        self.__world_entity_id = world_entity_id
        self.__sng_entity_id = sng_entity_id
        self.__call_center_entity_id = call_center_entity_id
        self.__mass_recruitment_entity_id = mass_recruitment_entity_id
        self.__chunk_size = chunk_size

    async def download_sng_data(self) -> None:
        log.info("Start create sng items")
        models = await self.__bitrix_client.fetch_sng_models()
        for i in range(0, len(models), self.__chunk_size):
            log.info("Write chunk from %s to %s", i, i + self.__chunk_size)
            await self.__bitrix_repository.create_many_sng(
                items=models[i : i + self.__chunk_size]
            )
        log.info("Finish create sng items")

    async def download_world_data(self) -> None:
        log.info("Start create world items")
        items = await self.__bitrix_client.fetch_world_models()
        for i in range(0, len(items), self.__chunk_size):
            log.info("Write chunk from %s to %s", i, i + self.__chunk_size)
            await self.__bitrix_repository.create_many_world(
                items=items[i : i + self.__chunk_size]
            )
        log.info("Finish create world items")

    async def download_ad_sng_data(self) -> None:
        log.info("Start create ad sng items")
        models = await self.__bitrix_client.fetch_ad_sng_models()
        for i in range(0, len(models), self.__chunk_size):
            log.info("Write chunk from %s to %s", i, i + self.__chunk_size)
            await self.__bitrix_repository.create_many_ad_sng(
                items=models[i : i + self.__chunk_size]
            )
        log.info("Finish create ad sng items")

    async def download_ad_world_data(self) -> None:
        log.info("Start create ad world items")
        items = await self.__bitrix_client.fetch_ad_world_models()
        for i in range(0, len(items), self.__chunk_size):
            log.info("Write chunk from %s to %s", i, i + self.__chunk_size)
            await self.__bitrix_repository.create_many_ad_world(
                items=items[i : i + self.__chunk_size]
            )
        log.info("Finish create ad world items")

    async def download_ad_call_center_data(self) -> None:
        log.info("Start create ad call_center items")
        models = await self.__bitrix_client.fetch_ad_call_center_models()
        for i in range(0, len(models), self.__chunk_size):
            log.info("Write chunk from %s to %s", i, i + self.__chunk_size)
            await self.__bitrix_repository.create_many_ad_call_center(
                items=models[i : i + self.__chunk_size]
            )
        log.info("Finish create ad call_center items")

    async def download_ad_mass_recruitment_data(self) -> None:
        log.info("Start create ad mass_recruitment items")
        items = await self.__bitrix_client.fetch_ad_mass_recruitment_models()
        for i in range(0, len(items), self.__chunk_size):
            log.info("Write chunk from %s to %s", i, i + self.__chunk_size)
            await self.__bitrix_repository.create_many_ad_mass_recruitment(
                items=items[i : i + self.__chunk_size]
            )
        log.info("Finish create ad mass_recruitment items")

    async def download_mass_selection(self) -> None:
        log.info("Start create mass selection items")
        items = await self.__bitrix_client.fetch_mass_selection_models()
        for i in range(0, len(items), self.__chunk_size):
            log.info("Write chunk from %s to %s", i, i + self.__chunk_size)
            await self.__bitrix_repository.create_many_mass_selection(
                items=items[i : i + self.__chunk_size]
            )
        log.info("Finish create mass selection items")
