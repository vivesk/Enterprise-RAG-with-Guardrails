from pathlib import Path
from pypdf import PdfReader

from .chunking import TextChunk, chunk_text
from .config import settings


def extract_pdf_text(file_path: str | Path) -> str:
    """Extract text from all pages of a PDF."""
    reader = PdfReader(str(file_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def ingest_pdf(file_path: str | Path) -> list[TextChunk]:
    """Read a PDF and convert it into retrievable chunks."""
    path = Path(file_path)
    return chunk_text(
        extract_pdf_text(path),
        source=path.name,
        chunk_size=settings.chunk_size,
        overlap=settings.chunk_overlap,
    )
