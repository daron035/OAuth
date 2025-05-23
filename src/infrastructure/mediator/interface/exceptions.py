from typing import Any

from .entities import Request


class MediatorError(Exception):
    pass


class HandlerNotFoundError(MediatorError, TypeError):
    request: Request[Any]

    def __init__(self, text: str, request: Request[Any]):
        super().__init__(text)
        self.request = request
