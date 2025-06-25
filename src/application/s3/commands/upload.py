import logging

from collections.abc import AsyncGenerator
from dataclasses import dataclass

from src.application.common.interfaces import S3Client
from src.infrastructure.mediator import Request, RequestHandler


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class UploadFile(Request[None]):
    bucket_name: str
    file_name: str
    stream: AsyncGenerator[bytes, None]


@dataclass(frozen=True)
class UploadFileHandler(RequestHandler[UploadFile, None]):
    s3_client: S3Client

    async def __call__(self, cmd: UploadFile) -> None:
        await self.s3_client.upload(bucket_name=cmd.bucket_name, key=cmd.file_name, data_stream=cmd.stream)
