from collections.abc import Awaitable, Callable
from typing import Any, Protocol, TypeVar

from ..entities import Request


R_contra = TypeVar("R_contra", bound=Request[Any], contravariant=True)
Res_co = TypeVar("Res_co", covariant=True)


class Handler(Protocol[R_contra, Res_co]):
    async def __call__(self, request: R_contra) -> Res_co:
        raise NotImplementedError


HandlerType = type[Handler[R_contra, Res_co]] | Handler[R_contra, Res_co]
CallableHandler = Callable[[R_contra], Awaitable[Res_co]]
