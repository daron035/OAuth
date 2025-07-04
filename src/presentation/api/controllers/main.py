from fastapi import FastAPI

from .default import default_router
from .exceptions import setup_exception_handlers
from .healthcheck import healthcheck_router
from .s3 import s3_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(healthcheck_router)
    app.include_router(s3_router)
    setup_exception_handlers(app)
