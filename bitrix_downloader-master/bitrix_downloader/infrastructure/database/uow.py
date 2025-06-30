import logging
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

log = logging.getLogger(__name__)


class SQLAlchemyUnitOfWork:
    session: AsyncSession
    __transaction: AsyncSessionTransaction | None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.__transaction: AsyncSessionTransaction | None = None

    async def __aenter__(self) -> Self:
        await self.create_transaction()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.__transaction:
            if exc_type:
                log.warning("Rolling back transaction due to exception")
                await self.rollback()
            else:
                await self.commit()

        await self.close_transaction()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def create_transaction(self) -> None:
        if not self.session.in_transaction() and self.session.is_active:
            self.__transaction = await self.session.begin()

    async def close_transaction(self) -> None:
        if self.session.is_active:
            await self.session.close()
