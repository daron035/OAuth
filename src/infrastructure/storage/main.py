from collections.abc import AsyncGenerator

from aiobotocore.session import get_session
from botocore.client import BaseClient

from .config import S3Config


async def build_s3_client(config: S3Config) -> AsyncGenerator[BaseClient, None]:
    session = get_session()

    async with session.create_client(
        "s3",
        region_name=config.region,
        endpoint_url=config.full_url,
        aws_access_key_id=config.access_key,
        aws_secret_access_key=config.secret_key,
    ) as s3_client:
        yield s3_client
