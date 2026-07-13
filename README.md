# Documentation Helper Bot

A lightweight documentation assistant built with LangChain, LLMs, and a vector database. This project crawls documentation sites, indexes content into a Pinecone vector store, and exposes a simple Streamlit UI and programmatic RAG (Retrieval-Augmented Generation) pipeline for querying the indexed docs.


## 🎯 What changed (this update)

This README has been updated to reflect the current repository layout and the latest commits: added a Streamlit app (main.py), clarified how the ingestion and RAG pipeline work, and listed concrete commands to run the project locally.


## 🚀 Features

- Intelligent web crawling using Tavily
- Vector-based semantic search with Pinecone
- Retrieval-Augmented Generation (RAG) using OpenAI LLMs (gpt-4o)
- Asynchronous ingestion pipeline for large-scale indexing
- Streamlit UI for interactive querying
- Source attribution for retrieved documents

## Demo

https://github.com/user-attachments/assets/8150b9bc-e8fe-4401-bf59-96524b7ba964




## 📁 Repository layout

```
documentation-helper-bot/
├── .agents/                # optional agent configs
├── .claude/                # optional Claude tool configs
├── .gitignore
├── .python-version
├── backend/
│   └── core.py             # RAG pipeline and LLM interaction
├── ingestion.py            # Document crawling and indexing (async)
├── main.py                 # Streamlit UI for querying the bot
├── pyproject.toml          # Project config and dependencies
├── uv.lock                 # dependency lock file
└── README.md
```


## 🧰 Prerequisites

- Python 3.11+
- OpenAI API key
- Pinecone API key and index
- (Optional) Tavily API key if you want to use the built-in crawler


## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/punithAJ-hub/documentation-helper-bot.git
cd documentation-helper-bot
```

2. Install dependencies. The repository includes a `pyproject.toml` and `uv.lock`.

Using pip:

```bash
pip install -r requirements.txt
```

Or using your preferred tool configured for `pyproject.toml` (e.g., `uv` / `poetry` / `pipx`).


## 🔐 Environment variables

Create a `.env` file in the project root with the following variables (examples):

```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=your_index_name
TAVILY_API_KEY=...            # optional for web crawling
```

Make sure `.env` is added to `.gitignore` so keys are not committed.


## 📥 Ingest (crawl + index)

The ingestion pipeline lives in `ingestion.py`. It performs the following:

- Uses Tavily to crawl a documentation site (the example uses https://python.langchain.com/)
- Wraps raw pages in langchain Document objects
- Splits documents into overlapping chunks (1000 characters with 200 overlap)
- Embeds chunks with OpenAI `text-embedding-3-small`
- Uploads batches asynchronously to a Pinecone index

Run the ingest script:

```bash
python ingestion.py
```

Key implementation notes from the code:
- Text splitter: RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
- Embedding model: text-embedding-3-small (embedding chunk_size=50)
- Indexing is done in async batches (batch_size default 500 in the call)


## 🗣️ Querying (RAG)

There are two ways to query:

1) Programmatically via `backend/core.py`:

```python
from backend.core import run_llm
result = run_llm("What are deep agents?")
print(result["answer"])  # generated answer
print(result["context"]) # list of retrieved documents (with metadata)
```

Implementation notes from `backend/core.py`:
- Uses OpenAI embeddings and PineconeVectorStore configured with `PINECONE_INDEX_NAME` from the environment
- Chat model: `gpt-4o` via `init_chat_model(model="gpt-4o", model_provider="openai")`
- A simple tool `retrieve_content(query: str)` is registered to fetch k=4 documents from the vector store and return serialized content and the document list
- `run_llm` creates an agent with the tool and system prompt, invokes it, extracts the assistant answer and any tool-returned documents as context

2) Interactive Streamlit UI in `main.py`:

```bash
streamlit run main.py
```

The Streamlit app provides a chat-style interface. When you ask a question it calls `run_llm`, displays the generated answer, and shows the sources used in an expander.


## ⚙️ Configuration

- Text splitter: chunk_size = 1000, overlap = 200
- Embedding model: text-embedding-3-small (embedding chunk size = 50)
- LLM: gpt-4o (OpenAI)
- Indexing batch size: 500 (configurable when calling `index_documents_async`)
- Web crawling settings (Tavily): max_depth=5, max_breadth=20, max_pages=1000


## 📦 Dependencies

Key dependencies are listed in `pyproject.toml`. Highlights:

- langchain-community
- langchain-openai
- langchain-pinecone
- langchain-tavily
- langchain-docling
- langchain-text-splitters
- tavily
- streamlit
- certifi
- dotenv

Refer to `pyproject.toml` for exact versions.


## 🚨 Notes & Troubleshooting

- Ensure your Pinecone index has the same embedding dimensionality as the model (`text-embedding-3-small` currently uses 384 dims) — configure the index accordingly before ingesting.
- API calls to OpenAI, Pinecone, and Tavily may incur charges.
- The ingestion pipeline performs async batch uploads; network or API errors may cause batch failures — check logs printed by `ingestion.py`.
- If you run into import issues, confirm your Python environment uses Python 3.11+ and that dependencies are installed.


## 📝 License

This project is open source and available under the MIT License.


## 👤 Author

Created by [punithAJ-hub](https://github.com/punithAJ-hub)


## 🤝 Contributing

Contributions welcome — open issues or submit pull requests. Please include tests or a short description of the change.


---

**Status**: Active Development ✨
