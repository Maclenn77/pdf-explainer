---
title: GnosisPages
emoji: 📚
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
pinned: false
---

# GnosisPages

GnosisPages is a RAG + LLM chatbot for querying private document collections. Upload PDF files, build a semantic knowledge base, and ask questions in natural language — no keyword matching required.

**[▶ Try the live demo](https://huggingface.co/spaces/maclenn77/pdf-explainer)** · **[Watch a walkthrough](https://youtu.be/OEQTusJGHFQ)**

---

## Use Case: CV Discovery for Recruiters

Managing large volumes of CVs is difficult. Recruiters often don't know the exact technologies or skill names to search for, and keyword-based search misses semantically equivalent terms (e.g. "machine learning" vs "aprendizaje automático", or experience in a framework analogous to the one required).

GnosisPages solves this with semantic retrieval: a recruiter can ask "Who has experience with distributed systems and has worked in startups?" and the system finds relevant profiles even when the exact phrasing doesn't match.

Candidate data is sensitive (contact details, personal history). GnosisPages keeps it private by design: documents live in a local or private vector database, and the LLM never trains on them — it only reads the retrieved context at inference time.

The demo ships with a pre-loaded collection of synthetic CVs generated with Claude Sonnet 4.6 and vectorized with OpenAI's `text-embedding-3-small`.

---

## Data flow

```
PDF documents
      │
      ▼
  Text extraction (PyMuPDF)
      │
      ▼
  Chunking (LangChain TextSplitter)
      │
      ▼
  Embedding (text-embedding-3-small · OpenAI)
      │
      ▼
  Vector storage (ChromaDB)
      │
      ▼
  User query (natural language)
      │
      ├─► Embed query ──► Semantic search (ChromaDB cosine similarity)
      │                         │
      │                   Top-k chunks
      │                         │
      └─────────────────► Prompt construction
                                │
                          GPT-4o-Mini (LangChain)
                                │
                          Answer → Streamlit UI
```


## Architecture

<img width="2000" height="1292" alt="image" src="https://github.com/user-attachments/assets/17f5f557-0334-47b7-9f62-a7f27f5522c7" />

### Components

| Layer | Technology | Role |
|---|---|---|
| UI | Streamlit 1.58 | Web interface and file upload |
| Orchestration | LangChain 0.3 | RAG chain, prompt management |
| Vector store | ChromaDB 1.5 | Semantic storage and retrieval |
| Embeddings | `text-embedding-3-small` (OpenAI) | Document and query vectorization |
| LLM | GPT-4o-Mini (OpenAI) | Answer generation |
| PDF parsing | PyMuPDF 1.24 | Text extraction from PDF files |

`text-embedding-3-small` replaces ChromaDB's default (`all-MiniLM-L6-v2`) for better semantic quality, especially across mixed-language content.

### Why GPT-4o-Mini

- Fast response times for conversational QA over retrieved context
- Lower cost per token than GPT-4o or GPT-4 Turbo
- Native LangChain integration
- Stable OpenAI API with no additional infrastructure

### Why RAG

The knowledge base is private, dynamic, and cannot be baked into model weights. RAG provides on-demand access to documents the LLM was never trained on, without exposing them to external services beyond the query moment.

---

## Features

- **Upload PDFs** up to 200 MB (programmatically created or OCR-processed)
- **Semantic search** across your document collection — finds relevant content even without exact keyword matches
- **Conversational interface** — ask follow-up questions in the same session
- **Pre-loaded dataset** — the demo includes synthetic CVs so you can try it immediately without uploading anything
- **Private by design** — documents stay in your vector store; the LLM only sees retrieved chunks

---

## Demo Usage

The live demo on HuggingFace requires only an OpenAI API Key.

**Example questions to try with the pre-loaded CV dataset:**

```
Who has experience with Python and machine learning?
Find candidates who have worked in startups or early-stage companies.
Who has the most experience in technical leadership roles?
Is there anyone with a background in both data engineering and backend development?
Which candidates mention experience with cloud infrastructure?
```

---

## Local Setup

**Requirements:** Python 3.11, OpenAI API Key

```bash
# 1. Clone
git clone https://github.com/maclenn77/pdf-explainer.git
cd pdf-explainer

# 2. Create environment file
touch .env
```

Add your key to `.env`:

```
OPENAI_API_KEY=your_key_here
```

```bash
# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run GnosisPages.py
```

---

## Deployment

The repo includes three GitHub Actions workflows that run on every PR and deploy automatically on merge to `main`:

| Workflow | What it does |
|---|---|
| Check file size | Blocks merges with files above HuggingFace's size limit |
| Check lints | Runs `pylint` on the codebase |
| Deploy to HuggingFace | Pushes the latest `main` to the HuggingFace Space |

To deploy your own fork, add these secrets in your repository settings:

- `HF_TOKEN` — your HuggingFace access token
- `HF_USERNAME` — your HuggingFace username

---

## Project Structure

```
pdf-explainer/
├── GnosisPages.py          # App entry point
├── gnosis/
│   ├── chroma_client.py    # ChromaDB wrapper
│   ├── settings.py         # Collection bootstrap (loads pre-built DB)
│   ├── gui_messages.py     # UI copy
│   └── components/
│       ├── sidebar.py      # File upload and DB controls
│       └── main.py         # Chat interface and RAG chain
├── pages/                  # Additional Streamlit pages
├── requirements.txt
├── Dockerfile
└── .github/workflows/      # CI/CD
```

---

## License

MIT — see [LICENSE](LICENSE) for details.
