from app.chunking import chunk_text


def test_chunking_creates_chunks():
    chunks = chunk_text(
        "A" * 2000,
        source="test.txt",
        chunk_size=500,
        overlap=50,
    )
    assert len(chunks) > 1
    assert chunks[0].source == "test.txt"
