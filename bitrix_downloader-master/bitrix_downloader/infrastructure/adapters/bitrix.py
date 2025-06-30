import asyncio
import itertools
import logging
from collections.abc import Sequence
from http import HTTPMethod, HTTPStatus
from types import MappingProxyType
from typing import ClassVar

from aiohttp import ClientSession
from base_http_client import BaseHttpClient, ResponseHandlersType, TimeoutType
from base_http_client.handlers.msgspec import struct_parser
from yarl import URL

from bitrix_downloader.common.entities.bitrix import (
    AdCallCenterApplicantPage,
    AdCallCenterModel,
    AdMassRecruitmentApplicantPage,
    AdMassRecruitmentModel,
    AdSNGApplicantPage,
    AdSNGModel,
    AdWorldApplicantPage,
    AdWorldModel,
    BitrixMassSelectionModel,
    BitrixMassSelectionPage,
    BitrixSNGApplicantPage,
    BitrixSNGModel,
    BitrixWorldApplicantPage,
    BitrixWorldModel,
)

log = logging.getLogger(__name__)

BITRIX_PAGE_SIZE = 50


class BitrixClient(BaseHttpClient):
    __sng_entity_id: int
    __world_entity_id: int
    __call_center_entity_id: int
    __mass_recruitment_entity_id: int

    DEFAULT_TIMEOUT: ClassVar[TimeoutType] = 5

    APPLICANTS_SNG_LIST_HANDLERS: ResponseHandlersType = MappingProxyType(
        {HTTPStatus.OK: struct_parser(struct=BitrixSNGApplicantPage)}
    )

    APPLICANTS_WORLD_LIST_HANDLERS: ResponseHandlersType = MappingProxyType(
        {HTTPStatus.OK: struct_parser(struct=BitrixWorldApplicantPage)}
    )

    APPLICANTS_AD_SNG_LIST_HANDLERS: ResponseHandlersType = MappingProxyType(
        {HTTPStatus.OK: struct_parser(struct=AdSNGApplicantPage)}
    )

    APPLICANTS_AD_WORLD_LIST_HANDLERS: ResponseHandlersType = MappingProxyType(
        {HTTPStatus.OK: struct_parser(struct=AdWorldApplicantPage)}
    )

    APPLICANTS_AD_MASS_RECRUITMENT_LIST_HANDLERS: ResponseHandlersType = (
        MappingProxyType(
            {HTTPStatus.OK: struct_parser(struct=AdMassRecruitmentApplicantPage)}
        )
    )

    APPLICANTS_AD_CALL_CENTER_LIST_HANDLERS: ResponseHandlersType = MappingProxyType(
        {HTTPStatus.OK: struct_parser(struct=AdCallCenterApplicantPage)}
    )

    MASS_SELECTION_LIST_HANDLERS: ResponseHandlersType = MappingProxyType(
        {HTTPStatus.OK: struct_parser(struct=BitrixMassSelectionPage)}
    )

    def __init__(
        self,
        url: URL,
        session: ClientSession,
        client_name: str,
        sng_entity_id: int,
        world_entity_id: int,
        call_center_entity_id: int,
        mass_recruitment_entity_id: int,
        chunk_size: int,
    ) -> None:
        super().__init__(url=url, session=session, client_name=client_name)
        self.__chunk_size = chunk_size
        self.__sng_entity_id = sng_entity_id
        self.__world_entity_id = world_entity_id
        self.__call_center_entity_id = call_center_entity_id
        self.__mass_recruitment_entity_id = mass_recruitment_entity_id

    async def fetch_sng_models(self) -> Sequence[BitrixSNGModel]:
        workers_count = self.__chunk_size // BITRIX_PAGE_SIZE
        results = await asyncio.gather(
            *[
                self.__fetch_sng_worker_items(
                    start=BITRIX_PAGE_SIZE * i,
                    chunk_size=self.__chunk_size,
                )
                for i in range(workers_count)
            ]
        )
        return tuple(itertools.chain(*results))

    async def fetch_world_models(self) -> Sequence[BitrixWorldModel]:
        workers_count = self.__chunk_size // BITRIX_PAGE_SIZE
        results = await asyncio.gather(
            *[
                self.__fetch_world_worker_items(
                    start=BITRIX_PAGE_SIZE * i,
                    chunk_size=self.__chunk_size,
                )
                for i in range(workers_count)
            ]
        )
        return tuple(itertools.chain(*results))

    async def fetch_ad_sng_models(self) -> Sequence[AdSNGModel]:
        workers_count = self.__chunk_size // BITRIX_PAGE_SIZE
        results = await asyncio.gather(
            *[
                self.__fetch_ad_sng_worker_items(
                    start=BITRIX_PAGE_SIZE * i,
                    chunk_size=self.__chunk_size,
                )
                for i in range(workers_count)
            ]
        )
        return tuple(itertools.chain(*results))

    async def fetch_ad_world_models(self) -> Sequence[AdWorldModel]:
        workers_count = self.__chunk_size // BITRIX_PAGE_SIZE
        results = await asyncio.gather(
            *[
                self.__fetch_ad_world_worker_items(
                    start=BITRIX_PAGE_SIZE * i,
                    chunk_size=self.__chunk_size,
                )
                for i in range(workers_count)
            ]
        )
        return tuple(itertools.chain(*results))

    async def fetch_ad_mass_recruitment_models(
        self,
    ) -> Sequence[AdMassRecruitmentModel]:
        workers_count = self.__chunk_size // BITRIX_PAGE_SIZE
        results = await asyncio.gather(
            *[
                self.__fetch_ad_mass_recruitment_worker_items(
                    start=BITRIX_PAGE_SIZE * i,
                    chunk_size=self.__chunk_size,
                )
                for i in range(workers_count)
            ]
        )
        return tuple(itertools.chain(*results))

    async def fetch_ad_call_center_models(self) -> Sequence[AdCallCenterModel]:
        workers_count = self.__chunk_size // BITRIX_PAGE_SIZE
        results = await asyncio.gather(
            *[
                self.__fetch_ad_call_center_worker_items(
                    start=BITRIX_PAGE_SIZE * i,
                    chunk_size=self.__chunk_size,
                )
                for i in range(workers_count)
            ]
        )
        return tuple(itertools.chain(*results))

    async def fetch_mass_selection_models(self) -> Sequence[BitrixMassSelectionModel]:
        workers_count = self.__chunk_size // BITRIX_PAGE_SIZE
        results = await asyncio.gather(
            *[
                self.__fetch_mass_selection_worker_items(
                    start=BITRIX_PAGE_SIZE * i,
                    chunk_size=self.__chunk_size,
                )
                for i in range(workers_count)
            ]
        )
        return tuple(itertools.chain(*results))

    async def __fetch_sng_worker_items(
        self,
        *,
        start: int,
        chunk_size: int,
    ) -> Sequence[BitrixSNGModel]:
        items: list[BitrixSNGModel] = []
        offset = start
        while True:
            page = await self.__fetch_sng_page(start=offset)
            items.extend(page.result.items)
            if page.next is None or page.next <= offset:
                break
            offset += chunk_size
        return items

    async def __fetch_world_worker_items(
        self,
        *,
        start: int,
        chunk_size: int,
    ) -> Sequence[BitrixWorldModel]:
        items: list[BitrixWorldModel] = []
        offset = start
        while True:
            page = await self.__fetch_world_page(start=offset)
            items.extend(page.result.items)
            if page.next is None or page.next <= offset:
                break
            offset += chunk_size
        return items

    async def __fetch_mass_selection_worker_items(
        self,
        *,
        start: int,
        chunk_size: int,
    ) -> Sequence[BitrixMassSelectionModel]:
        items: list[BitrixMassSelectionModel] = []
        offset = start
        while True:
            page = await self.__fetch_mass_selection_page(start=offset)
            items.extend(page.result.items)
            if page.next is None or page.next <= offset:
                break
            offset += chunk_size
        return items

    async def __fetch_ad_sng_worker_items(
        self,
        *,
        start: int,
        chunk_size: int,
    ) -> Sequence[AdSNGModel]:
        items: list[AdSNGModel] = []
        offset = start
        while True:
            page = await self.__fetch_ad_sng_page(start=offset)
            items.extend(page.result.items)
            if page.next is None or page.next <= offset:
                break
            offset += chunk_size
        return items

    async def __fetch_ad_world_worker_items(
        self,
        *,
        start: int,
        chunk_size: int,
    ) -> Sequence[AdWorldModel]:
        items: list[AdWorldModel] = []
        offset = start
        while True:
            page = await self.__fetch_ad_world_page(start=offset)
            items.extend(page.result.items)
            if page.next is None or page.next <= offset:
                break
            offset += chunk_size
        return items

    async def __fetch_ad_mass_recruitment_worker_items(
        self,
        *,
        start: int,
        chunk_size: int,
    ) -> Sequence[AdMassRecruitmentModel]:
        items: list[AdMassRecruitmentModel] = []
        offset = start
        while True:
            page = await self.__fetch_ad_mass_recruitment_page(start=offset)
            items.extend(page.result.items)
            if page.next is None or page.next <= offset:
                break
            offset += chunk_size
        return items

    async def __fetch_ad_call_center_worker_items(
        self,
        *,
        start: int,
        chunk_size: int,
    ) -> Sequence[AdCallCenterModel]:
        items: list[AdCallCenterModel] = []
        offset = start
        while True:
            page = await self.__fetch_ad_call_center_page(start=offset)
            items.extend(page.result.items)
            if page.next is None or page.next <= offset:
                break
            offset += chunk_size
        return items

    async def __fetch_world_page(
        self,
        *,
        start: int = 0,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> BitrixWorldApplicantPage:
        return await self._make_req(
            method=HTTPMethod.POST,
            url=self._url / "crm.item.list",
            handlers=self.APPLICANTS_WORLD_LIST_HANDLERS,
            timeout=timeout,
            json={
                "entityTypeId": self.__world_entity_id,
                "select": [
                    "id",
                    "assignedById",
                    "createdTime",
                    "stageId",
                    "ufCrm20_1710308337539",
                    "ufCrm20_1710308353693",
                    "ufCrm20_1710308372853",
                    "ufCrm20_1710308497445",
                    "ufCrm20_1710309130539",
                    "ufCrm20_1710492855399",
                    "ufCrm20_1710493359806",
                    "ufCrm20_1710833955002",
                    "ufCrm20_1711029907",
                    "ufCrm20_1712566725",
                    "ufCrm20_1712923122",
                    "ufCrm20_1714739083",
                    "ufCrm20_1715346103",
                    "ufCrm20_1716798467",
                ],
                "start": start,
            },
        )

    async def __fetch_sng_page(
        self,
        *,
        start: int = 0,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> BitrixSNGApplicantPage:
        return await self._make_req(
            method=HTTPMethod.POST,
            url=self._url / "crm.item.list",
            handlers=self.APPLICANTS_SNG_LIST_HANDLERS,
            timeout=timeout,
            json={
                "entityTypeId": self.__sng_entity_id,
                "select": [
                    "id",
                    "assignedById",
                    "createdTime",
                    "stageId",
                    "ufCrm23_1710937794",
                    "ufCrm23_1710937991",
                    "ufCrm23_1710938033",
                    "ufCrm23_1710938474",
                    "ufCrm23_1710939449",
                    "ufCrm23_1710942062",
                    "ufCrm23_1710942433",
                    "ufCrm23_1710945931",
                    "ufCrm23_1710947671",
                    "ufCrm23_1716619640273",
                    "ufCrm23_1716622092407",
                    "ufCrm23_1716817266",
                    "ufCrm23_1716879053",
                ],
                "start": start,
            },
        )

    async def __fetch_ad_sng_page(
        self,
        *,
        start: int = 0,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> AdSNGApplicantPage:
        return await self._make_req(
            method=HTTPMethod.POST,
            url=self._url / "crm.item.list",
            handlers=self.APPLICANTS_AD_SNG_LIST_HANDLERS,
            timeout=timeout,
            json={
                "entityTypeId": self.__sng_entity_id,
                "select": [
                    "id",
                    "createdTime",
                    "stageId",
                    "ufCrm23_1716909298",
                    "ufCrm23_1710937794",
                    "ufCrm23_1710937991",
                ],
                "start": start,
            },
        )

    async def __fetch_ad_world_page(
        self,
        *,
        start: int = 0,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> AdWorldApplicantPage:
        return await self._make_req(
            method=HTTPMethod.POST,
            url=self._url / "crm.item.list",
            handlers=self.APPLICANTS_AD_WORLD_LIST_HANDLERS,
            timeout=timeout,
            json={
                "entityTypeId": self.__world_entity_id,
                "select": [
                    "id",
                    "createdTime",
                    "stageId",
                    "ufCrm20_1716909279",
                    "ufCrm20_1710308337539",
                    "ufCrm20_1710308353693",
                ],
                "start": start,
            },
        )

    async def __fetch_ad_mass_recruitment_page(
        self,
        *,
        start: int = 0,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> AdMassRecruitmentApplicantPage:
        return await self._make_req(
            method=HTTPMethod.POST,
            url=self._url / "crm.item.list",
            handlers=self.APPLICANTS_AD_MASS_RECRUITMENT_LIST_HANDLERS,
            timeout=timeout,
            json={
                "entityTypeId": self.__mass_recruitment_entity_id,
                "select": [
                    "id",
                    "createdTime",
                    "stageId",
                    "ufCrm5_1717078179",
                    "ufCrm5_1706947526",
                ],
                "start": start,
            },
        )

    async def __fetch_ad_call_center_page(
        self,
        *,
        start: int = 0,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> AdCallCenterApplicantPage:
        return await self._make_req(
            method=HTTPMethod.POST,
            url=self._url / "crm.item.list",
            handlers=self.APPLICANTS_AD_CALL_CENTER_LIST_HANDLERS,
            timeout=timeout,
            json={
                "entityTypeId": self.__call_center_entity_id,
                "select": [
                    "id",
                    "createdTime",
                    "stageId",
                    "sourceId",
                    "ufCrm15_1708599858537",
                    "ufCrm15_1709032200935",
                    "ufCrm15_1709032219283",
                    "ufCrm15_1709032128595",
                    "ufCrm15_1709032182621",
                    "ufCrm15_1709032153650",
                    "ufCrm15_1713513061",
                    "ufCrm15_1708584336136",
                    "ufCrm15_1708584391194",
                    "ufCrm15_1708584379794",
                    "ufCrm15_1708584366043",
                    "ufCrm15_1708584351136",
                ],
                "start": start,
            },
        )

    async def __fetch_mass_selection_page(
        self,
        *,
        start: int = 0,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> BitrixMassSelectionPage:
        return await self._make_req(
            method=HTTPMethod.POST,
            url=self._url / "crm.item.list",
            handlers=self.MASS_SELECTION_LIST_HANDLERS,
            timeout=timeout,
            json={
                "entityTypeId": self.__mass_recruitment_entity_id,
                "select": [
                    "id",
                    "stageId",
                    "ufCrm5_1706447447",
                    "ufCrm5_1710238329892",
                    "ufCrm5_1706947526",
                    "ufCrm5_1710237996027",
                    "ufCrm5_1710238078012",
                    "ufCrm5_1710239649116",
                    "ufCrm5_1706447172",
                    "ufCrm5_1706860136",
                ],
                "start": start,
            },
        )


class BitrxException(Exception):
    pass


class BitrixImportError(BitrxException):
    pass
