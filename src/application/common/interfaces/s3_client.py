from collections.abc import AsyncGenerator
from typing import Protocol


class S3Client(Protocol):
    async def upload(self, bucket_name: str, key: str, data_stream: AsyncGenerator[bytes, None]) -> None: ...

    async def ensure_bucket(self, bucket_name: str) -> None: ...
