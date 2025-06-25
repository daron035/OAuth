import asyncio

from collections.abc import AsyncGenerator

from streaming_form_data.targets import BaseTarget


class S3UploadTarget(BaseTarget):
    """
    Цель-приёмник для потокового парсинга multipart/form-data.

    Этот класс буферизует получаемые чанки данных в асинхронную очередь,
    обеспечивая возможность асинхронного чтения содержимого файла по частям.

    Атрибуты:
        _queue (asyncio.Queue): очередь для хранения байтовых чанков данных.
        _finished (bool): флаг, сигнализирующий o завершении передачи данных.

    Методы:
        data_received(chunk): вызывается при получении очередного чанка,
            помещает ero в очередь.
        finish(): помечает, что все данные получены, добавляет в очередь маркер конца.
        stream(): асинхронный генератор, который отдаёт чанки из очереди по одному,
            пока не встретит маркер конца (None).

    Используется как цель для StreamingFormDataParser, чтобы позволить
    эффективно обрабатывать и передавать большие файлы без загрузки в память целиком.
    """

    def __init__(self) -> None:
        super().__init__()
        self._queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._finished = False

    def data_received(self, chunk: bytes) -> None:
        self._queue.put_nowait(chunk)

    def finish(self) -> None:
        self._finished = True
        self._queue.put_nowait(None)

    async def stream(self) -> AsyncGenerator[bytes, None]:
        while True:
            chunk = await self._queue.get()
            if chunk is None:
                break
            yield chunk
