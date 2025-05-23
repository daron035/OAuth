from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, TypeVar

from ..entities import Request
from .base import Handler
from .event import EventListener


R_contra = TypeVar("R_contra", bound=Request[Any], contravariant=True)
Res_co = TypeVar("Res_co", covariant=True)


@dataclass(frozen=True)
class RequestHandler(Handler[R_contra, Res_co], ABC):
    _events: list[EventListener] = field(default_factory=list, init=False)

    @property
    def events(self) -> list:
        return self._events

    @abstractmethod
    async def __call__(self, request: R_contra) -> Res_co:
        raise NotImplementedError
