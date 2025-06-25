from dataclasses import dataclass


@dataclass
class S3Config:
    host: str = "localhost"
    port: int = 9000
    region: str = "us-east-1"
    access_key: str = "minioadmin"
    secret_key: str = "minioadmin"

    @property
    def full_url(self) -> str:
        return f"http://{self.host}:{self.port}"
