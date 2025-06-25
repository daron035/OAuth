from collections.abc import Callable, Coroutine
from functools import wraps
from inspect import iscoroutinefunction, isfunction
from typing import Any, ParamSpec, TypeVar, _ProtocolMeta

from sqlalchemy.exc import SQLAlchemyError

from src.application.common.exceptions import RepoError


Param = ParamSpec("Param")
ReturnT = TypeVar("ReturnT")
Func = Callable[Param, ReturnT]


def exception_mapper(
    func: Callable[Param, Coroutine[Any, Any, ReturnT]],
) -> Callable[Param, Coroutine[Any, Any, ReturnT]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnT:
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as err:
            raise RepoError from err

    return wrapped


def no_exception_mapper(func: Any) -> Any:
    func.__no_exception_mapper__ = True
    return func


class ExceptionMappingMeta(_ProtocolMeta):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]):
        for attr_name, attr_value in namespace.items():
            if attr_name.startswith("_"):
                continue

            if not (isfunction(attr_value) and iscoroutinefunction(attr_value)):
                continue

            if getattr(attr_value, "__no_exception_mapper__", False):
                continue

            namespace[attr_name] = exception_mapper(attr_value)

        return super().__new__(cls, name, bases, namespace)
