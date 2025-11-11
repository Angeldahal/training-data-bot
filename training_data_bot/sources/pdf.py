import asyncio
from pathlib import Path


from training_data_bot.core.exceptions import DocumentLoadError
from training_data_bot.core.models import DocumentType
from training_data_bot.sources.base import BaseLoader


class PDFLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.supported_formats = [DocumentType.PDF]

    async def load_single(self, source):
        source = Path(source)
        if not source.exists():
            raise DocumentLoadError(f"File not found: {source}")
        content = await self._extract_pdf_text(source)
        document = self.create_document(
            title=source.stem,
            content=content,
            source=source,
            doc_type=DocumentType.PDF,
            extraction_method="PDFLoader.pymupdf",
        )
        return document
    
    async def _extract_pdf_text(self, path):
        def _extract_text():
            try:
                import fitz
                doc = fitz.open(path)
                text_parts = []
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    text = page.get_text()
                    if text.strip():
                        text_parts.append(f"Page {page_num + 1}: \n{text}")
                doc.close()
                return "\n\n".join(text_parts)
            except ImportError:
                raise DocumentLoadError("PyMuPDF package required for PDF files. Install with: pip install PyMuPDF")
        return await asyncio.to_thread(_extract_text)
