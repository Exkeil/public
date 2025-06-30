import os

import pytest

from bitrix_downloader.args import Parser


@pytest.fixture(scope="session")
def parser() -> Parser:
    return Parser().parse_args(
        [
            "--log-level=info",
            "--log-format=plain",
            f"--database-user={os.getenv("APP_DATABASE_USER")}",
            f"--database-password={os.getenv("APP_DATABASE_PASSWORD")}",
            f"--database-host={os.getenv("APP_DATABASE_HOST")}",
            "--database-port=5432",
            f"--database-name={os.getenv("APP_DATABASE_NAME")}",
            "--bitrix-webhook=webhook",
            "--bitrix-sng-entity-id=123",
            "--bitrix-world-entity-id=123",
            "--bitrix-call-center-entity-id=123",
            "--bitrix-mass-recruitment-entity-id=123",
            "--bitrix-chunk-size=100",
            "--cron-spec=0 * * * *",
            "--log-level=info",
            "--log-format=plain",
            "--debug=True",
            "--pool-size=4",
        ]
    )
