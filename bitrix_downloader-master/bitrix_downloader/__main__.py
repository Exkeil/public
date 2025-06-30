import logging

from aiomisc import Service, entrypoint
from aiomisc_log import basic_config
from dishka import make_async_container

from bitrix_downloader.args import Parser
from bitrix_downloader.di import MainProvider
from bitrix_downloader.presentors.scheduler.service import DownloaderService

log = logging.getLogger(__name__)


def main() -> None:
    parser = Parser(auto_env_var_prefix="APP_")
    parser.parse_args([])
    parser.sanitize_env()

    basic_config(level=parser.log.level, log_format=parser.log.format)

    container = make_async_container(MainProvider(parser=parser))
    services: list[Service] = [
        DownloaderService(cron_spec=parser.scheduler.cron_spec, container=container),
    ]
    with entrypoint(
        *services,
        log_level=parser.log.level,
        log_format=parser.log.format,
        pool_size=parser.pool_size,
        debug=parser.debug,
    ) as loop:
        log.info(
            "Start downloader service with %s scheduler",
            parser.scheduler.cron_spec,
        )
        loop.run_forever()


if __name__ == "__main__":
    main()
