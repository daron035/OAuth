from fastapi import APIRouter

from src.application.authorization.commands.authorize import Authorize
from src.infrastructure.di import container, mediator
from src.infrastructure.redis.service import RedisService


healthcheck_router = APIRouter(
    tags=["general"],
)


@healthcheck_router.get("/healthcheck")
async def healthcheck() -> dict[str, bool]:
    # container is mediator._container
    assert container._ctx_var.get() is mediator._ctx_var.get()._ioc._container  # type: ignore[arg-type] # noqa: SLF001

    # send command
    response = await mediator.send(Authorize("Joe Peach"))

    # using container directly
    redis: RedisService = await container.get(RedisService)
    await redis.ping()

    return response
