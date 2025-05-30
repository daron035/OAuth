from functools import lru_cache

from dishka import AsyncContainer, Provider, Scope, make_async_container

from src.application.authorization.commands.authorize import AuthorizeHandler
from src.infrastructure.config import Config
from src.infrastructure.config_loader import load_config
from src.infrastructure.postgres.config import PostgresConfig
from src.infrastructure.postgres.main import (
    build_sa_engine,
    build_sa_session,
    build_sa_session_factory,
)
from src.infrastructure.postgres.services.healthcheck import PgHealthCheck, PostgresHealthcheckService
from src.infrastructure.postgres.uow import SQLAlchemyUoW
from src.infrastructure.redis.config import RedisConfig
from src.infrastructure.redis.main import init_redis_pool
from src.infrastructure.redis.service import RedisService
from src.infrastructure.uow import build_uow


def config_provider(config: Config) -> Provider:
    provider = Provider()

    # Config
    provider.provide(lambda: config.postgres, scope=Scope.APP, provides=PostgresConfig)
    provider.provide(lambda: config.redis, scope=Scope.APP, provides=RedisConfig)

    # Postgres
    provider.provide(build_sa_engine, scope=Scope.APP)
    provider.provide(build_sa_session_factory, scope=Scope.APP)
    provider.provide(build_sa_session, scope=Scope.REQUEST)

    # UoW
    provider.provide(SQLAlchemyUoW, scope=Scope.REQUEST)
    provider.provide(build_uow, scope=Scope.REQUEST)

    # Repositories
    provider.provide(PostgresHealthcheckService, scope=Scope.REQUEST, provides=PgHealthCheck)

    # Redis
    provider.provide(init_redis_pool, scope=Scope.APP)
    provider.provide(RedisService, scope=Scope.APP)

    # Handlers
    provider.provide(AuthorizeHandler, scope=Scope.REQUEST)
    return provider


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(config_provider(load_config(Config)))
