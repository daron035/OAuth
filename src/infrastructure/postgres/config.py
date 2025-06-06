from dataclasses import dataclass


@dataclass
class PostgresConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "postgres"
    user: str = "admin"
    password: str = "admin"
    echo: bool = True

    @property
    def full_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
