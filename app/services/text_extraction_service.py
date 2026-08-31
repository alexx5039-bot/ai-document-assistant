from pathlib import Path
from docx import Document as DocxDocument

from fastapi import HTTPException, status
from pypdf import PdfReader

class TextExtractionService:

    async def extract(self, file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self._extract_pdf(file_path)

        if extension == ".docx":
            return self._extract_docx(file_path)

        if extension in {".txt", ".md"}:
            return self._extract_text(file_path)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {extension}",
        )
    def _extract_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text)

    def _extract_docx(self, file_path: str) -> str:
        document = DocxDocument(file_path)
        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

    def _extract_text(self, file_path: str) -> str:
        return Path(file_path).read_text(encoding="utf-8")