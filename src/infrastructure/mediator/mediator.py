from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, TypeVar

from .interface import Request
from .interface.entities import Event
from .interface.exceptions import HandlerNotFoundError
from .interface.handlers import HandlerType
from .interface.handlers.event import EventHandlerType, EventListener
from .interface.ioc import Ioc
from .interface.mediator import Mediator
from .middlewares import Middleware, wrap_middleware


if TYPE_CHECKING:
    from src.infrastructure.mediator.interface.handlers import CallableHandler


R = TypeVar("R", bound=Request[Any])
RRes = TypeVar("RRes")
E = TypeVar("E", bound=Event)


class MediatorImpl(Mediator):
    def __init__(self, *, ioc: Ioc, middlewares: list[Middleware]) -> None:
        self._request_handlers: dict[type[Request[Any]], HandlerType[Any, Any]] = {}
        self._event_listeners: list[EventListener] = []
        self._middlewares = middlewares
        self._ioc = ioc

    def register_request_handler(self, request: type[R], handler: HandlerType[R, RRes]) -> None:
        self._request_handlers[request] = handler

    def register_event_handler(self, event: type[E], handler: EventHandlerType[E]) -> None:
        listener = EventListener(event, handler)
        self._event_listeners.append(listener)

    async def send(self, request: Request[RRes]) -> RRes:
        try:
            handler = self._request_handlers[type(request)]
        except KeyError as err:
            raise HandlerNotFoundError(
                f"Request handler for {type(request).__name__} request is not registered",
                request,
            ) from err

        async with self._ioc.provide(handler) as initialized_handler:
            wrapped: CallableHandler = wrap_middleware(self._middlewares, initialized_handler)
            response = await wrapped(request)
            events = initialized_handler.events

        if events:
            await self._send_events(events.copy())

        return response

    async def _send_events(self, events: Event | Sequence[Event]) -> None:
        if not isinstance(events, Sequence):
            events = [events]

        for event in events:
            for listener in self._event_listeners:
                if listener.is_listen(event):
                    async with self._ioc.provide(listener.handler) as initialized_handler:
                        wrapped_handler = wrap_middleware(self._middlewares, initialized_handler)
                        return await wrapped_handler(event)

        return None
