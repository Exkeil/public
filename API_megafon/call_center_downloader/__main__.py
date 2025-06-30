import logging
import os
from dotenv import load_dotenv

from aiomisc import Service, entrypoint
from aiomisc_log import basic_config
from dishka import make_async_container

from call_center_downloader.args import MainConfig as Parser
from call_center_downloader.di import MainProvider
from call_center_downloader.presentors.scheduler.service import DownloaderService

log = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()
    parser = Parser(auto_env_var_prefix="APP_")
    parser.parse_args()
    parser.sanitize_env()
    basic_config(level=parser.log_level, log_format=parser.log_format)
    container = make_async_container(MainProvider(parser=parser))
    services: list[Service] = [
        DownloaderService(cron_spec=parser.scheduler_cron_spec, container=container),
    ]
    with entrypoint(
            *services,
            log_level=parser.log_level,
            log_format=parser.log_format,
            pool_size=parser.pool_size,
            debug=parser.debug,
    ) as loop:
        log.info(
            "Запуск сервиса загрузки с расписанием %s",
            parser.scheduler_cron_spec,
        )
        loop.run_forever()


if __name__ == "__main__":
    main()