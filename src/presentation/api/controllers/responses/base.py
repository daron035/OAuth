from dataclasses import dataclass, field
from typing import Generic, TypeVar


ResultT = TypeVar("ResultT")
ErrorT = TypeVar("ErrorT")


@dataclass(frozen=True)
class Response:
    pass


@dataclass(frozen=True)
class OkResponse(Response, Generic[ResultT]):
    status: int = 200
    result: ResultT | None = None


@dataclass(frozen=True)
class ErrorData(Generic[ErrorT]):
    title: str = "Unknown error occurred"
    data: ErrorT | None = None


@dataclass(frozen=True)
class ErrorResponse(Response, Generic[ErrorT]):
    status: int = 500
    error: ErrorData[ErrorT] = field(default_factory=ErrorData)
