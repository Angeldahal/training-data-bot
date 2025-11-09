from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from .core.logging import get_logger
from .models import Document, DocumentType


class BaseLoader(ABC):
    def __init__(self):
        self.logger = get_logger(f"loader.{self.__class__.__name__}")
        self.supported_formats: List[DocumentType] = []

    @abstractmethod
    async def load_single(self, source, **kwargs) -> Document:
        pass


class PDFLoader:
    pass


class WebLoader:
    pass


class DocumentLoader:
    pass


class UnifiedLoader(BaseLoader):
    def __init__(self):
        self.document_loader = DocumentLoader()
        self.pdf_loader = PDFLoader()
        self.web_loader = WebLoader()

        self.supported_formats = list(DocumentType)

    def _get_loader(self, source):
        if source.startswith(("http://", "https://")):
            return self.web_loader

        source = Path(source)
        if not source.exists():
            return None

        suffix = source.suffix.lower().lstrip(".")
        doctype = DocumentType(suffix)

        if doctype == DocumentType.PDF:
            return self.pdf_loader
        elif doctype in [DocumentType.TXT, DocumentType.DOCX, DocumentType.MD]:
            return self.document_loader

    def load_single(self):
        pass

    def load_directory(self):
        pass
