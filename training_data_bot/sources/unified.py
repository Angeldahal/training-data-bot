from pathlib import Path

from training_data_bot.core.models import DocumentType
from .base import BaseLoader
from .documents import DocumentLoader
from .web import WebLoader
from .pdf import PDFLoader


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
