from collections.abc import AsyncGenerator
from dataclasses import dataclass

from fastapi import HTTPException, Request
from streaming_form_data import StreamingFormDataParser

from .s3_upload_target import S3UploadTarget


@dataclass
class MultipartFile:
    filename: str
    stream: AsyncGenerator[bytes, None]


async def parse_multipart_file(request: Request) -> MultipartFile:
    if "multipart/form-data" not in request.headers.get("Content-Type", ""):
        raise HTTPException(400, detail="Invalid Content-Type")

    upload_target = S3UploadTarget()
    parser = StreamingFormDataParser(headers=request.headers)
    parser.register("file", upload_target)

    async for data in request.stream():
        parser.data_received(data)
    upload_target.finish()

    filename = upload_target.multipart_filename
    if not filename:
        raise HTTPException(400, detail="Filename not provided")

    return MultipartFile(filename=filename, stream=upload_target.stream())
