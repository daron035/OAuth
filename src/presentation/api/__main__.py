import asyncio
import logging

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import Scope, make_async_container

from src.infrastructure.config import Config
from src.infrastructure.config_loader import load_config
from src.infrastructure.di import config_provider, container_var, mediator_var
from src.infrastructure.log.main import configure_logging
from src.infrastructure.mediator.main import build_mediator
from src.presentation.api.main import init_api, run_api


logger = logging.getLogger(__name__)


@asynccontextmanager
async def init_di(config: Config) -> AsyncIterator[None]:
    container = make_async_container(config_provider(config), start_scope=Scope.RUNTIME)

    async with container(scope=Scope.APP) as app_container:
        mediator = build_mediator(app_container)
        container_var.set(app_container)
        mediator_var.set(mediator)

        yield

        await app_container.close()


async def main() -> None:
    config = load_config(Config)
    configure_logging(config.logging)

    logger.info("Launch app", extra={"config": config})

    async with init_di(config):
        app = init_api()
        await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
