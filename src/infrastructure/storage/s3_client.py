from collections.abc import AsyncGenerator
from dataclasses import dataclass

from botocore.client import BaseClient
from botocore.exceptions import ClientError

from src.application.common.interfaces import S3Client


PART_SIZE = 5 * 1024 * 1024


@dataclass
class S3ClientImpl(S3Client):
    client: BaseClient

    async def upload(
        self,
        bucket_name: str,
        key: str,
        data_stream: AsyncGenerator[bytes, None],
    ) -> None:
        resp = await self.client.create_multipart_upload(Bucket=bucket_name, Key=key)
        upload_id = resp["UploadId"]
        part_number = 1
        parts_info: list[dict] = []
        buffer = bytearray()

        try:
            async for chunk in data_stream:
                buffer.extend(chunk)
                if len(buffer) >= PART_SIZE:
                    resp = await self.client.upload_part(
                        Bucket=bucket_name,
                        Key=key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=bytes(buffer),
                    )
                    parts_info.append({"PartNumber": part_number, "ETag": resp["ETag"]})
                    part_number += 1
                    buffer.clear()

            if buffer:
                resp = await self.client.upload_part(
                    Bucket=bucket_name,
                    Key=key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=bytes(buffer),
                )
                parts_info.append({"PartNumber": part_number, "ETag": resp["ETag"]})

            await self.client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts_info},
            )
        except ClientError:
            await self.client.abort_multipart_upload(
                Bucket=bucket_name,
                Key=key,
                UploadId=upload_id,
            )
            raise

    async def ensure_bucket(self, bucket_name: str) -> None:
        try:
            await self.client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code in ("NoSuchBucket", "404"):
                await self.client.create_bucket(Bucket=bucket_name)
            else:
                raise
