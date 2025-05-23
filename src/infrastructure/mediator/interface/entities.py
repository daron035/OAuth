from typing import Protocol, TypeVar


RRes_co = TypeVar("RRes_co", covariant=True)


class Request(Protocol[RRes_co]):
    pass


class Event(Request[None], Protocol):
    pass
