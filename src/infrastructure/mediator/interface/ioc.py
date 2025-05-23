from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol, TypeVar

from . import Request
from .handlers import HandlerType, RequestHandler


R = TypeVar("R", bound=Request[Any])
RRes = TypeVar("RRes")


class Ioc(Protocol):
    def provide(self, handler: HandlerType[R, RRes]) -> AbstractAsyncContextManager[RequestHandler[R, RRes]]:
        raise NotImplementedError
