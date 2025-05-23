import functools

from collections.abc import Sequence
from typing import Protocol

from src.infrastructure.mediator.interface.handlers import CallableHandler
from src.infrastructure.mediator.interface.handlers.request import R_contra, Res_co


class Middleware(Protocol[R_contra, Res_co]):
    async def __call__(
        self,
        handler: CallableHandler,
        request: R_contra,
    ) -> Res_co:
        return await handler(request)


def wrap_middleware(
    middlewares: Sequence[Middleware[R_contra, Res_co]],
    handler: CallableHandler,
) -> CallableHandler:
    for middleware in reversed(middlewares):
        handler = functools.partial(middleware, handler)

    return handler
