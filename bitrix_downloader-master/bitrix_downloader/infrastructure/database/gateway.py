from types import TracebackType
from typing import Self

from bitrix_downloader.infrastructure.database.repositories.bitrix import (
    BitrixRepository,
)
from bitrix_downloader.infrastructure.database.uow import SQLAlchemyUnitOfWork


class DatabaseGateway:
    __uow: SQLAlchemyUnitOfWork

    def __init__(self, uow: SQLAlchemyUnitOfWork) -> None:
        self.__uow = uow

    async def __aenter__(self) -> Self:
        await self.__uow.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.__uow.__aexit__(exc_type, exc_val, exc_tb)

    def bitrix(self) -> BitrixRepository:
        return BitrixRepository(session=self.__uow.session)
