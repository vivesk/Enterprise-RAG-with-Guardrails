from dataclasses import dataclass


@dataclass
class TextChunk:
    """One retrievable section of a source document."""

    text: str
    source: str
    chunk_id: str


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = 900,
    overlap: int = 120,
) -> list[TextChunk]:
    """Create overlapping character chunks.

    This simple strategy is intentional for an interview project.
    In production, compare token-aware, recursive, or semantic chunking.
    """
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > overlap >= 0")

    text = " ".join(text.split())
    chunks = []
    start = 0
    index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        value = text[start:end].strip()

        if value:
            chunks.append(
                TextChunk(
                    text=value,
                    source=source,
                    chunk_id=f"{source}::chunk-{index}",
                )
            )

        if end == len(text):
            break

        start = end - overlap
        index += 1

    return chunks
