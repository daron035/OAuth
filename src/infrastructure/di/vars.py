from contextvars import ContextVar
from typing import TypeVar

from dishka import AsyncContainer

from src.infrastructure.mediator import Mediator


T = TypeVar("T")


class ContextProxy[T]:
    def __init__(self, ctx_var: ContextVar[T]) -> None:
        self._ctx_var = ctx_var

    def __getattr__(self, name: str):
        real_obj = self._ctx_var.get()
        return getattr(real_obj, name)


container_var: ContextVar[AsyncContainer] = ContextVar("container_var")
mediator_var: ContextVar[Mediator] = ContextVar("mediator_var")

container = ContextProxy(container_var)
mediator = ContextProxy(mediator_var)
