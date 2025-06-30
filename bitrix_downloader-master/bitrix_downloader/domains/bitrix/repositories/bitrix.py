import abc
from collections.abc import Sequence
from typing import Protocol

from bitrix_downloader.common.entities.bitrix import (
    AdCallCenterModel,
    AdMassRecruitmentModel,
    AdSNGModel,
    AdWorldModel,
    BitrixMassSelectionModel,
    BitrixSNGModel,
    BitrixWorldModel,
)


class IBitrixRepository(Protocol):
    @abc.abstractmethod
    async def create_many_sng(self, *, items: Sequence[BitrixSNGModel]) -> None: ...

    @abc.abstractmethod
    async def create_many_world(self, *, items: Sequence[BitrixWorldModel]) -> None: ...

    @abc.abstractmethod
    async def create_many_ad_sng(self, *, items: Sequence[AdSNGModel]) -> None: ...

    @abc.abstractmethod
    async def create_many_ad_world(self, *, items: Sequence[AdWorldModel]) -> None: ...

    @abc.abstractmethod
    async def create_many_ad_mass_recruitment(
        self, *, items: Sequence[AdMassRecruitmentModel]
    ) -> None: ...

    @abc.abstractmethod
    async def create_many_ad_call_center(
        self, *, items: Sequence[AdCallCenterModel]
    ) -> None: ...

    @abc.abstractmethod
    async def create_many_mass_selection(
        self, *, items: Sequence[BitrixMassSelectionModel]
    ) -> None: ...
