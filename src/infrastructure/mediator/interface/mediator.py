from collections.abc import Sequence
from typing import Any, Protocol, TypeVar

from .entities import Event, Request
from .handlers import HandlerType
from .handlers.event import EventHandlerType


R = TypeVar("R", bound=Request[Any])
RRes = TypeVar("RRes")
E = TypeVar("E", bound=Event)


class Mediator(Protocol):
    def register_request_handler(self, request: type[R], handler: HandlerType[R, RRes]) -> None:
        raise NotImplementedError

    def register_event_handler(self, event: type[E], handler: EventHandlerType[E]) -> None:
        raise NotImplementedError

    async def send(self, request: Request[RRes]) -> RRes:
        raise NotImplementedError

    async def _send_events(self, events: Event | Sequence[Event]) -> None:
        raise NotImplementedError
