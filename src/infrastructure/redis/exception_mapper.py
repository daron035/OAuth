from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from redis.exceptions import RedisError

from src.application.common.exceptions import RedisUnavailableError


Param = ParamSpec("Param")
ReturnType = TypeVar("ReturnType")


def exception_mapper(
    func: Callable[Param, Coroutine[Any, Any, ReturnType]],
) -> Callable[Param, Coroutine[Any, Any, ReturnType]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnType:
        try:
            return await func(*args, **kwargs)
        except RedisError as err:
            raise RedisUnavailableError from err

    return wrapped
