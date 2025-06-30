import argparse
import logging

import argclass
from alembic.config import CommandLine

from bitrix_downloader.args import DatabaseGroup
from bitrix_downloader.infrastructure.database.utils import make_alembic_config


class Parser(argclass.Parser):
    database = DatabaseGroup(title="Database options")


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    options = alembic.parser.parse_args()
    parser = Parser(auto_env_var_prefix="APP_").parse_args([])
    if "cmd" not in options:
        alembic.parser.error("Too few arguments")
        exit(128)
    else:
        config = make_alembic_config(options, pg_url=parser.database.url)
        alembic.run_cmd(config, options)
        exit()


if __name__ == "__main__":
    main()
