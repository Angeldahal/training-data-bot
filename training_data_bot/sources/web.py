import httpx
from training_data_bot.core.exceptions import DocumentLoadError
from training_data_bot.core.models import DocumentType
from .base import BaseLoader


class WebLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.supported_formats = [DocumentType.URL]

    async def load_single(self, source):
        if not source.startswith(("https://", "http://")):
            raise DocumentLoadError("Invalid URL: {source}")
        content = await self._fetch_url_content(source)
        title = self._extract_title(source, content)
        document = self.create_document(
            title=title,
            content=content,
            source=source,
            doc_type=DocumentType.URL,
            extraction_method="WebLoader.httpx",
        )
        return document

    async def _fetch_url_content(self, url):
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").lower()
            if "text/html" in content_type:
                return self._extract_html_text(response.text)
            else:
                return response.text

    def _extract_html_text(self, html):
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            return " ".join(chunk for chunk in chunks if chunk)
        except ImportError:
            return html

    def _extract_title(self, url, content):
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(content, "html.parser")
            title_tag = soup.find("title")
            if title_tag and title_tag.text.strip():
                return title_tag.text.strip()
        except ImportError:
            pass
        from urllib.parse import urlparse

        parsed = urlparse(url)
        return parsed.netloc + parsed.path or url
