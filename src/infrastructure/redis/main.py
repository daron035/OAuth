from collections.abc import AsyncIterator

from redis.asyncio import Redis, from_url

from .config import RedisConfig


async def init_redis_pool(config: RedisConfig) -> AsyncIterator[Redis]:
    session = from_url(f"redis://{config.host}", password=config.password, encoding="utf-8", decode_responses=True)
    yield session
    await session.close()
