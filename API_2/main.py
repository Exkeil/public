import logging
import asyncio
from dependency_injector import containers, providers
from aiohttp import ClientSession
from dotenv import load_dotenv

from config import Parser, Config
from auth import AuthService
from services import APIService, CSVRepository, DownloaderService

load_dotenv()

log = logging.getLogger(__name__)

class MainProvider(providers.Provider):
    def __init__(self, parser: Parser):
        super().__init__()
        self.parser = parser

    @providers.Singleton
    def config(self) -> Config:
        return self.parser.config

    @providers.Factory
    async def client_session(self) -> ClientSession:
        async with ClientSession() as session:
            yield session

    @providers.Factory
    def auth_service(self, config: Config = providers.Dependency()) -> AuthService:
        return AuthService(config.base_url, config.username, config.password)

    @providers.Factory
    def api_service(self, config: Config = providers.Dependency()) -> APIService:
        return APIService(config.base_url, config.domain_id)

    @providers.Factory
    def csv_repository(self, config: Config = providers.Dependency()) -> CSVRepository:
        return CSVRepository(config.output_dir)

def make_async_container(parser: Parser) -> containers.DynamicContainer:
    container = containers.DynamicContainer()
    container.main_provider = MainProvider(parser)
    container.config = container.main_provider.config
    container.client_session = container.main_provider.client_session
    container.auth_service = container.main_provider.auth_service
    container.api_service = container.main_provider.api_service
    container.csv_repository = container.main_provider.csv_repository
    return container

class Entrypoint:
    def __init__(self, services, log_level, log_format, pool_size, debug):
        self.services = services
        self.log_level = log_level
        self.log_format = log_format
        self.pool_size = pool_size
        self.debug = debug

    def __enter__(self):
        logging.basicConfig(level=self.log_level, format=self.log_format)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        for service in self.services:
            self.loop.create_task(service.run())
        return self.loop

    def __exit__(self, exc_type, exc, tb):
        tasks = [t for t in asyncio.all_tasks(self.loop) if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()

def entrypoint(*services, log_level, log_format, pool_size, debug):
    return Entrypoint(services, log_level, log_format, pool_size, debug)

def main():
    parser = Parser()
    parser.parse_args([])
    parser.sanitize_env()
    container = make_async_container(parser)
    services = [DownloaderService(parser.config.scheduler.cron_spec, container)]
    with entrypoint(
        *services,
        log_level=parser.config.log.level,
        log_format=parser.config.log.format,
        pool_size=parser.config.pool_size,
        debug=parser.config.debug
    ) as loop:
        loop.run_forever()

if __name__ == "__main__":
    main()