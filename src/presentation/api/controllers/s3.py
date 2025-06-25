from fastapi import APIRouter, Request

from src.application.s3.commands.upload import UploadFile
from src.infrastructure.di import mediator
from src.presentation.api.controllers.requests.parsers.s3 import parse_multipart_file


s3_router = APIRouter(
    tags=["s3"],
)


@s3_router.post("/upload")
async def upload(request: Request) -> dict:
    file = await parse_multipart_file(request)
    await mediator.send(UploadFile(bucket_name="test-bucket", file_name=file.filename, stream=file.stream))
    return {"status": "ok", "filename": file.filename}
