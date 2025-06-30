from dataclasses import dataclass
from environs import Env
from typing import List

@dataclass
class LogConfig:
    level: str
    format: str

@dataclass
class SchedulerConfig:
    cron_spec: str

@dataclass
class Config:
    base_url: str
    username: str
    password: str
    domain_id: int
    output_dir: str
    time_filter_enabled: bool
    time_filter_start: int
    log: LogConfig
    scheduler: SchedulerConfig
    debug: bool
    pool_size: int

class Parser:
    def __init__(self, auto_env_var_prefix: str = "APP_"):
        self.env = Env()
        self.env.read_env()
        self.auto_env_var_prefix = auto_env_var_prefix

    def parse_args(self, args: List[str]) -> None:
        pass 

    def sanitize_env(self) -> None:
        pass  #

    @property
    def config(self) -> Config:
        return Config(
            base_url=self.env.str(f"{self.auto_env_var_prefix}BASE_URL", "https://lk-al.cprt.su/api/"),
            username=self.env.str(f"{self.auto_env_var_prefix}USERNAME", "admin@callcenter-al.cprt.su"),
            password=self.env.str(f"{self.auto_env_var_prefix}PASSWORD", "RNEvCAkt"),
            domain_id=self.env.int(f"{self.auto_env_var_prefix}DOMAIN_ID", 2),
            output_dir=self.env.str(f"{self.auto_env_var_prefix}OUTPUT_DIR", "data"),
            time_filter_enabled=self.env.bool(f"{self.auto_env_var_prefix}TIME_FILTER_ENABLED", True),
            time_filter_start=self.env.int(f"{self.auto_env_var_prefix}TIME_FILTER_START", 1704067200),  # 1 января 2024
            log=LogConfig(
                level=self.env.str(f"{self.auto_env_var_prefix}LOG_LEVEL", "INFO"),
                format=self.env.str(f"{self.auto_env_var_prefix}LOG_FORMAT", "%(asctime)s %(levelname)s %(message)s")
            ),
            scheduler=SchedulerConfig(
                cron_spec=self.env.str(f"{self.auto_env_var_prefix}CRON_SPEC", "*/5 * * * *")  # Каждые 5 минут
            ),
            debug=self.env.bool(f"{self.auto_env_var_prefix}DEBUG", False),
            pool_size=self.env.int(f"{self.auto_env_var_prefix}POOL_SIZE", 10)
        )