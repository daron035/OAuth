from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, TypeVar

from dishka import AsyncContainer

from ..interface import Request, RequestHandler
from ..interface.handlers import HandlerType
from ..interface.ioc import Ioc


R = TypeVar("R", bound=Request[Any])
RRes = TypeVar("RRes")


class DishkaIoc(Ioc):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    @asynccontextmanager
    async def provide(self, handler: HandlerType[R, RRes]) -> AsyncIterator[RequestHandler[R, RRes]]:
        async with self._container() as request_container:
            yield await request_container.get(handler)
