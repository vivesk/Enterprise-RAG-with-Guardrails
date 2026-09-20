"""Simple transparent baseline for RAG evaluation.

Replace the example dataset with real domain questions and expected
answers/keywords. A production evaluation should add retrieval precision,
groundedness, answer relevance, citation accuracy, latency, and cost.
"""

from .rag import RAGService


GOLDEN_DATASET = [
    {
        "question": "What is the main topic of the document?",
        "expected_keywords": [],
    },
]


def keyword_score(answer: str, expected_keywords: list[str]) -> float:
    """Calculate a simple lexical baseline score."""
    if not expected_keywords:
        return 1.0

    answer_lower = answer.lower()
    hits = sum(k.lower() in answer_lower for k in expected_keywords)
    return hits / len(expected_keywords)


def run_evaluation() -> None:
    service = RAGService()
    scores = []

    for item in GOLDEN_DATASET:
        result = service.answer(item["question"])
        score = (
            0.0
            if result["blocked"]
            else keyword_score(result["answer"], item["expected_keywords"])
        )
        scores.append(score)

        print("\nQUESTION:", item["question"])
        print("ANSWER:", result["answer"])
        print("SCORE:", round(score, 3))
        print("SOURCES:", len(result["sources"]))

    if scores:
        print("\nAverage baseline score:", round(sum(scores) / len(scores), 3))


if __name__ == "__main__":
    run_evaluation()
