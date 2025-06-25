import logging

from dataclasses import dataclass

from src.application.common.interfaces import UnitOfWork
from src.infrastructure.mediator import Request, RequestHandler
from src.infrastructure.postgres.services.healthcheck import PgHealthCheck


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Authorize(Request[dict[str, bool]]):
    username: str


@dataclass(frozen=True)
class AuthorizeHandler(RequestHandler[Authorize, dict[str, bool]]):
    pg_health: PgHealthCheck
    uow: UnitOfWork

    async def __call__(self, cmd: Authorize) -> dict[str, bool]:
        pg_res = await self.pg_health.check()
        await self.uow.commit()

        logger.info(cmd.username)

        self._events.append("Some Event")  # type: ignore[arg-type]

        return pg_res
