from collections.abc import AsyncGenerator, AsyncIterator

from aiohttp import ClientSession
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from yarl import URL

from bitrix_downloader.args import Parser
from bitrix_downloader.domains.bitrix.repositories.bitrix import IBitrixRepository
from bitrix_downloader.domains.bitrix.services.bitrix import BitrixService
from bitrix_downloader.infrastructure.adapters.bitrix import BitrixClient
from bitrix_downloader.infrastructure.database.gateway import DatabaseGateway
from bitrix_downloader.infrastructure.database.uow import SQLAlchemyUnitOfWork
from bitrix_downloader.infrastructure.database.utils import (
    create_engine,
    create_session_factory,
)


class MainProvider(Provider):
    __parser: Parser

    def __init__(self, parser: Parser) -> None:
        super().__init__()
        self.__parser = parser

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        engine = create_engine(
            url=self.__parser.database.url,
            debug=self.__parser.debug,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_factory(engine=engine)

    @provide(scope=Scope.APP)
    async def bitrix_client(self) -> AsyncGenerator[BitrixClient, None]:
        async with ClientSession() as session:
            yield BitrixClient(
                session=session,
                url=URL(self.__parser.bitrix.webhook),
                client_name="bitrix",
                sng_entity_id=self.__parser.bitrix.sng_entity_id,
                world_entity_id=self.__parser.bitrix.world_entity_id,
                call_center_entity_id=self.__parser.bitrix.call_center_entity_id,
                mass_recruitment_entity_id=self.__parser.bitrix.mass_recruitment_entity_id,
                chunk_size=self.__parser.bitrix.chunk_size,
            )

    @provide(scope=Scope.REQUEST)
    def uow(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(session=session_factory())

    @provide(scope=Scope.REQUEST)
    async def database_gateway(
        self,
        uow: SQLAlchemyUnitOfWork,
    ) -> AsyncIterator[DatabaseGateway]:
        async with DatabaseGateway(uow=uow) as gateway:
            yield gateway

    @provide(scope=Scope.REQUEST)
    def bitrix_repository(self, gateway: DatabaseGateway) -> IBitrixRepository:
        return gateway.bitrix()

    @provide(scope=Scope.REQUEST)
    def bitrix_service(
        self,
        bitrix_repository: IBitrixRepository,
        bitrix_client: BitrixClient,
    ) -> BitrixService:
        return BitrixService(
            bitrix_repository=bitrix_repository,
            bitrix_client=bitrix_client,
            sng_entity_id=self.__parser.bitrix.sng_entity_id,
            world_entity_id=self.__parser.bitrix.world_entity_id,
            call_center_entity_id=self.__parser.bitrix.call_center_entity_id,
            mass_recruitment_entity_id=self.__parser.bitrix.mass_recruitment_entity_id,
            chunk_size=self.__parser.bitrix.chunk_size,
        )
