from dataclasses import dataclass, field

from src.infrastructure.log.config import LoggingConfig
from src.infrastructure.postgres.config import PostgresConfig
from src.infrastructure.redis.config import RedisConfig
from src.presentation.api.config import APIConfig


@dataclass
class Config:
    api: APIConfig = field(default_factory=APIConfig)
    postgres: PostgresConfig = field(default_factory=PostgresConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
