from dataclasses import dataclass


@dataclass
class RedisConfig:
    host: str = "localhost"
    password: str | None = None
