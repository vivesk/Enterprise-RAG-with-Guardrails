from pathlib import Path
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException

from .ingestion import ingest_pdf
from .models import AskRequest, AskResponse
from .rag import RAGService

app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Interview-ready RAG + security demonstration.",
    version="1.0.0",
)

rag = RAGService()


@app.get("/health")
def health() -> dict:
    """Basic service health endpoint."""
    return {"status": "ok"}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)) -> dict:
    """Upload a PDF, extract it, chunk it, and store embeddings."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    content = await file.read()

    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / file.filename
        path.write_bytes(content)
        chunks = ingest_pdf(path)

    count = rag.store.add_chunks(chunks)
    return {"filename": file.filename, "chunks_indexed": count}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Answer a question using retrieved document evidence."""
    return AskResponse(**rag.answer(request.question))
