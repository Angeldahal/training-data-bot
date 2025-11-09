import asyncio
import csv
import json

from training_data_bot.core.exceptions import DocumentLoadError
from training_data_bot.core.models import DocumentType
from .base import BaseLoader

class DocumentLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.supported_formats = [
            DocumentType.TXT,
            DocumentType.MD,
            DocumentType.JSON,
            DocumentType.CSV,
            DocumentType.HTML,
            DocumentType.DOCX,
        ]

    async def load_single(self, source, encoding='utf-8'):
        doc_type = self.get_document_type(source)
        if doc_type == DocumentType.TXT:
            content = await self._load_text(source, encoding)
        elif doc_type == DocumentType.MD:
            content = await self._load_markdown(source, encoding)
        elif doc_type == DocumentType.HTML:
            content = await self._load_html(source, encoding)
        elif doc_type == DocumentType.CSV:
            content = await self._load_csv(source, encoding)
        elif doc_type == DocumentType.JSON:
            content = await self._load_json(source, encoding)
        elif doc_type == DocumentType.DOCX:
            content = await self._load_docx(source)
    
    async def _load_text(self, path, encoding):
        return await asyncio.to_thread(path.read_text, encoding=encoding)

    async def _load_md(self, path, encoding):
        return await asyncio.to_thread(path.read_text, encoding=encoding)
    
    async def _load_html(self, path, encoding):
        try:
            from bs4 import BeautifulSoup
            with open(path, "r", encoding=encoding) as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            return " ".join(chunk for chunk in chunks if chunk)
        except ImportError:
            return path.read_text(encoding=encoding)

    async def _load_json(self, path, encoding):
        with open(path, "r", encoding=encoding) as f:
            data = json.load(f)
        if isinstance(data, dict):
            lines = [f"{key}: {value}" for key, value in data.items()]
            return '\n'.join(lines)
        elif isinstance(data, list):
            lines = [f"Item {i+1}: {item}" for i, item in enumerate(data)]
            return "\n".join(lines)
    
    async def _load_csv(self, path, encoding):
        lines = []
        with open(path, 'r', encoding=encoding, newline='') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers:
                lines.append("Headers: " + ", ".join(headers))
                lines.append("")
            for row_num, row in enumerate(reader, 1):
                if headers and len(row) == len(headers):
                    row_data = [f'{header}: {value}' for header, value in zip(headers, row)]
                    lines.append(f'Row: {row_num}: {' | '.join(row_data)}')
        return "\n".join(lines)

    async def _load_docx(self, path, encoding):
        try:
            from docx import Document
            doc = Document(path)
            text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(text_parts)
        except ImportError:
            raise DocumentLoadError("python-docx package required for DOCX files")
