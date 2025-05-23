from dataclasses import dataclass
from typing import Any

from redis.asyncio import Redis

from .exception_mapper import exception_mapper


@dataclass
class RedisService:
    client: Redis

    @exception_mapper
    async def ping(self) -> Any:
        return await self.client.ping()
