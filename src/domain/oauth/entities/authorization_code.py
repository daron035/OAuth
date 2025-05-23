from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from src.domain.common.entities import Entity
from src.domain.oauth.value_objects.pkce import PKCEPair
from src.domain.oauth.value_objects.state import State


@dataclass
class AuthorizationCode(Entity):
    """
    Сущность, представляющая код авторизации c привязкой к OAuth-сценарию.

    Поля:
      - code: уникальный код авторизации (генерируется автоматически)
      - client_id: идентификатор клиента, для которого выдан код
      - redirect_uri: URI, на который клиент будет перенаправлен после авторизации
      - state: ОБЯЗАТЕЛЬНО, если параметр state присутствовал в запросе авторизации клиента.
        Точное значение, полученное от клиента
      - code_challenge: PKCE code_challenge, связанный c данным кодом
      - code_challenge_method: метод преобразования (обычно "S256")
      scope
      - created_at: время создания кода
      - expires_in: срок действия кода (в секундах)
    """

    state: State
    pkce: PKCEPair
    client_id: str
    scope: str | None
    redirect_uri: str | None
    code: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_in: int = field(default=600)

    def is_expired(self) -> bool:
        """Проверяет, истёк ли срок действия кода авторизации."""
        return datetime.now(tz=UTC) > self.created_at + timedelta(seconds=self.expires_in)
