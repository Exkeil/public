from argclass import Argument, Parser

class MainConfig(Parser):
    debug: bool = Argument(default=False)
    pool_size: int = Argument(default=1)
    log_level: str = Argument(default="info", choices=["critical", "debug", "error", "info", "notset", "warning"])
    log_format: str = Argument(default="plain", choices=["color", "disabled", "journald", "json", "plain", "rich", "rich_tb", "stream", "syslog"])
    storage_output_dir: str = Argument(default="./data")
    scheduler_cron_spec: str = Argument(default="* * * * *")