import secrets

from dataclasses import dataclass, field

from src.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class State(ValueObject[str | None]):
    value: str | None = field(default_factory=lambda: secrets.token_urlsafe(64))
