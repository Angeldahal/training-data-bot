from abc import ABC, abstractmethod
import asyncio
import datetime
from pathlib import Path
from typing import List
from uuid import uuid4

from training_data_bot.core.logging import get_logger
from training_data_bot.core.models import Document, DocumentType


class BaseLoader(ABC):
    def __init__(self):
        self.logger = get_logger(f"loader.{self.__class__.__name__}")
        self.supported_formats: List[DocumentType] = []

    @abstractmethod
    async def load_single(self, source, **kwargs) -> Document:
        pass

    async def load_multiple(self, sources, max_workers=4):
        semaphore = asyncio.Semaphore(max_workers)
        async def load_with_semaphore(source):
            async with semaphore:
                return await self.load_single(source)
        tasks = [load_with_semaphore(source) for source in sources]
        results = await asyncio.gather(*tasks)
    
    def get_document_type(self, source):
        if source.startswith("http"):
            return DocumentType.URL
        source = Path(source)
        suffix = source.suffix.lower().lstrip(".")
        return DocumentType(suffix)

    def create_document(
            self,
            title,
            content,
            source,
            doc_type,
            **kwargs
    ):
        return Document(
            id=uuid4(),
            title=title,
            content=content,
            source=source,
            doc_type=doc_type,
            word_count=len(content.split()),
            created_at=datetime.utcnow(),
            **kwargs
        )
