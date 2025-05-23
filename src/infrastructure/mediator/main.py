from dishka import AsyncContainer

from src.application.authorization.commands.authorize import Authorize, AuthorizeHandler
from src.infrastructure.mediator.middlewares.logging import LoggingMiddleware

from . import Mediator, MediatorImpl
from .ioc import DishkaIoc


def build_mediator(container: AsyncContainer) -> Mediator:
    mediator = MediatorImpl(
        ioc=DishkaIoc(container),
        middlewares=[LoggingMiddleware()],
    )
    mediator.register_request_handler(Authorize, AuthorizeHandler)

    return mediator
