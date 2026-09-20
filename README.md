# Day 1 AI Engineer Interview Project

## Enterprise RAG Assistant + Evaluation + Prompt-Injection Defense

This project demonstrates document ingestion, chunking, embeddings, Chroma vector search, Ollama generation, citations, evaluation, FastAPI, Streamlit, tests, and Docker.

### Architecture

User/UI -> FastAPI -> RAG Service -> Vector Store -> Ollama
                         |
                         +-> Security Guardrail
                         |
                         +-> Sources/Citations

### Install

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

Install/run Ollama separately and pull a model:

```bash
ollama pull llama3.2:3b
```

### Run

API:

```bash
uvicorn app.main:app --reload
```

UI:

```bash
streamlit run app/streamlit_app.py
```

API docs: http://127.0.0.1:8000/docs

### Usage

1. Upload a PDF through the Streamlit UI.
2. Index it.
3. Ask questions.
4. Review the retrieved sources.
5. Run `python -m app.evaluate` after adding domain-specific golden questions.

### Interview talking points

**Why RAG?** It keeps enterprise knowledge outside the model, supports document updates without retraining, and enables source attribution.

**How do you reduce hallucinations?** Retrieve evidence, ground the prompt, require citations, support an explicit "I don't know", evaluate groundedness, and add human review for high-impact workflows.

**Why security beyond the system prompt?** Prompts are not authorization boundaries. Tool permissions, identity, data access, and audit controls belong in the application/security layer.

**Prototype-to-production changes:** Azure OpenAI or another managed endpoint, Azure AI Search, Blob Storage, Entra ID/RBAC, Key Vault, private networking, Application Insights, CI/CD, evaluation, rate limiting, audit logging, PII controls, and human-in-the-loop controls.
