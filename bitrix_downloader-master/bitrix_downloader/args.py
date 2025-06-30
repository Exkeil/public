import argclass
from aiomisc_log import LogFormat, LogLevel


class LogGroup(argclass.Group):
    level: LogLevel = argclass.EnumArgument(
        LogLevel, "--log-level", default=LogLevel.info
    )
    format: LogFormat = argclass.EnumArgument(
        LogFormat, "--log-format", default=LogFormat.color
    )


class DatabaseGroup(argclass.Group):
    user: str = argclass.Argument("--database-user", type=str, required=True)
    password: str = argclass.Secret("--database-password", type=str, required=True)
    host: str = argclass.Argument("--database-host", type=str, required=True)
    port: int = argclass.Argument("--database-port", type=int, required=True)
    name: str = argclass.Argument("--database-name", type=str, required=True)

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class BitrixGroup(argclass.Group):
    webhook: str = argclass.Argument("--bitrix-webhook", type=str, required=True)
    sng_entity_id: int = argclass.Argument(
        "--bitrix-sng-entity-id", type=int, required=True
    )
    world_entity_id: int = argclass.Argument(
        "--bitrix-world-entity-id", type=int, required=True
    )
    call_center_entity_id: int = argclass.Argument(
        "--bitrix-call-center-entity-id", type=int, required=True
    )
    mass_recruitment_entity_id: int = argclass.Argument(
        "--bitrix-mass-recruitment-entity-id", type=int, required=True
    )
    chunk_size: int = argclass.Argument("--bitrix-chunk-size", type=int, required=True)


class SchedulerGroup(argclass.Group):
    cron_spec: str = argclass.Argument(
        "--cron-spec",
        type=str,
        default="0 * * * *",
        help="Cron spec for scheduler",
    )


class Parser(argclass.Parser):
    log = LogGroup(title="Logging options")
    database = DatabaseGroup(title="Database options")
    bitrix = BitrixGroup(title="Bitrix options")
    scheduler = SchedulerGroup(title="Scheduler options")

    debug: bool = argclass.Argument(
        "-D",
        "--debug",
        default=False,
        type=lambda x: x.lower() == "true",
    )
    pool_size: int = argclass.Argument(
        "-s", "--pool-size", type=int, default=4, help="Thread pool size"
    )
