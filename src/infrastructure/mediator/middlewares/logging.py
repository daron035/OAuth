import logging

from typing import Any, Protocol, TypeVar

from ..interface import CallableHandler, Request
from .base import Middleware


RRes = TypeVar("RRes")
R = TypeVar("R", bound=Request[Any])


class Logger(Protocol):
    def log(self, level: int, msg: str, *args: Any, extra: dict[str, Any] | None = None) -> None:
        raise NotImplementedError


class LoggingMiddleware(Middleware):
    def __init__(
        self,
        logger: Logger | None = None,
        level: int | str = logging.DEBUG,
    ):
        self._logger: Logger = logger or logging.getLogger(__name__)
        self._level: int = logging.getLevelName(level) if isinstance(level, str) else level

    async def __call__(self, handle: CallableHandler[R, RRes], request: R) -> RRes:
        self._logger.log(
            self._level,
            "Handle %s request",
            type(request).__name__,
            extra={"request": request},
        )
        response = await handle(request)
        self._logger.log(
            self._level,
            "Request %s handled. Response: %s",
            type(request).__name__,
            response,
            extra={"request": request},
        )

        return response
