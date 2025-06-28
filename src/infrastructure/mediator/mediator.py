import asyncio
import logging

from collections.abc import Sequence
from types import TracebackType
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

logger = logging.getLogger(__name__)

R = TypeVar("R", bound=Request[Any])
RRes = TypeVar("RRes")
E = TypeVar("E", bound=Event)


class MediatorImpl(Mediator):
    def __init__(self, *, ioc: Ioc, middlewares: list[Middleware], worker_count: int = 1, timeout: int = 20) -> None:
        self._request_handlers: dict[type[Request[Any]], HandlerType[Any, Any]] = {}
        self._event_listeners: list[EventListener] = []
        self._middlewares = middlewares
        self._ioc = ioc

        self._message_queue: asyncio.Queue[list[Event]] = asyncio.Queue()
        self._worker_tasks: list[asyncio.Task] = []
        self._worker_count: int = worker_count
        self._timeout: int = timeout

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
            await self._message_queue.put(events.copy())

        return response

    async def _event_worker(self, worker_id: int) -> None:
        logger.info("Event worker #%d started", worker_id)
        while True:
            events = await self._message_queue.get()
            try:
                await self._send_events(events)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("[worker #%d] Ошибка при обработке событий", worker_id)
                # await asyncio.sleep(1)
                # await self._message_queue.put(events)
            finally:
                self._message_queue.task_done()

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

    async def __aenter__(self) -> Mediator:
        loop = asyncio.get_event_loop()

        def _schedule_workers() -> None:
            for idx in range(self._worker_count):
                logger.info("Scheduling event worker #%d", idx)
                task = asyncio.create_task(self._event_worker(idx))
                self._worker_tasks.append(task)

        if loop.is_running():
            _schedule_workers()
        else:
            loop.call_soon(_schedule_workers)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._drain_queue()

        await self._shutdown_workers()

    async def _drain_queue(self) -> None:
        try:
            logger.info("Waiting up to 20s to drain the message queue…")
            async with asyncio.timeout(self._timeout):
                await self._message_queue.join()
            logger.info("Message queue drained successfully.")
        except TimeoutError:
            logger.warning("Timeout — cancelling all worker tasks.")
        except asyncio.CancelledError:
            raise

    async def _shutdown_workers(self) -> None:
        for task in self._worker_tasks:
            task.cancel()

        for task in self._worker_tasks:
            try:
                await task
            except asyncio.CancelledError:
                logger.info("Worker task %r cancelled.", task.get_name())
