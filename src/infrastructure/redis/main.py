from collections.abc import AsyncGenerator

from redis.asyncio import Redis, from_url

from .config import RedisConfig


async def init_redis_pool(config: RedisConfig) -> AsyncGenerator[Redis]:
    session = from_url(
        f"redis://{config.host}:{config.port}",
        password=config.password,
        encoding="utf-8",
        decode_responses=True,
    )
    yield session
    await session.close()
