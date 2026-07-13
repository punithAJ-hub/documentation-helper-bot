# Documentation Helper Bot

A powerful AI-powered documentation assistant built with LangChain, LLMs, and vector databases. This bot crawls documentation sites, indexes content into Pinecone vector store, and provides intelligent answers using Retrieval-Augmented Generation (RAG).

## 🎯 Features

- **Intelligent Web Crawling**: Automatically crawls and extracts content from documentation sites using Tavily
- **Vector-Based Search**: Leverages Pinecone vector database for semantic search across indexed documentation
- **RAG Pipeline**: Implements Retrieval-Augmented Generation using OpenAI GPT-4o for accurate, context-aware answers
- **Async Processing**: Efficiently processes and indexes large batches of documents asynchronously
- **Source Attribution**: Automatically cites sources from retrieved documentation
- **LangChain Integration**: Built on LangChain framework for robust agent management

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- Pinecone API key and index
- Tavily API key (optional, for web crawling)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/punithAJ-hub/documentation-helper-bot.git
cd documentation-helper-bot
```

2. Install dependencies using `uv`:
```bash
uv pip install -e .
```

Or using pip:
```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
TAVILY_API_KEY=your_tavily_api_key
```

## 📖 Usage

### 1. Index Documentation (Data Ingestion)

Run the ingestion script to crawl and index documentation:

```bash
python ingestion.py
```

This script:
- Crawls the LangChain documentation site
- Extracts content with focus on AI agents
- Splits documents into manageable chunks
- Indexes chunks into Pinecone vector store in batches

### 2. Query the Bot

Use the core module to ask questions:

```python
from backend.core import run_llm

result = run_llm("What are deep agents?")
print("Answer:", result["answer"])
print("Context:", result["context"])
```

## 🏗️ Architecture

### Project Structure

```
documentation-helper-bot/
├── backend/
│   ├── __init__.py
│   └── core.py              # RAG pipeline and agent logic
├── ingestion.py             # Document crawling and indexing
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
└── README.md
```

### Key Components

#### `ingestion.py`
- **Purpose**: Web crawling and document ingestion
- **Key Functions**:
  - `index_documents_async()`: Asynchronously indexes documents to Pinecone in batches
  - `main()`: Orchestrates crawling and indexing workflow
- **Features**:
  - Uses Tavily for intelligent web crawling
  - Recursive text splitting with 1000-character chunks and 200-character overlap
  - Batch processing for efficient indexing

#### `backend/core.py`
- **Purpose**: RAG pipeline and LLM interaction
- **Key Functions**:
  - `retrieve_content()`: Tool for retrieving relevant documentation from vector store
  - `run_llm()`: Main function that runs the complete RAG pipeline
- **Features**:
  - Creates an agent with document retrieval tool
  - Uses GPT-4o as the language model
  - Enforces source attribution in responses

## 🔧 Dependencies

Key dependencies include:

- **langchain**: 0.4.2+ - Core framework for building LLM applications
- **langchain-openai**: 1.3.3+ - OpenAI integration
- **langchain-pinecone**: 0.2.13+ - Pinecone vector store integration
- **langchain-tavily**: 0.2.18+ - Web crawling and search tools
- **langchain-docling**: 2.0.0+ - Document parsing
- **tavily**: 1.1.0+ - Web search and crawling API
- **python**: 3.11+

## 🔐 Security

- API keys are stored in `.env` file (ensure it's in `.gitignore`)
- Uses environment variables for sensitive configuration
- Implements SSL certificate verification with certifi

## 💡 How It Works

1. **Crawling Phase**: Tavily crawls the target documentation site and extracts raw content
2. **Chunking Phase**: Documents are split into overlapping chunks for optimal retrieval
3. **Indexing Phase**: Chunks are embedded using OpenAI's `text-embedding-3-small` model and stored in Pinecone
4. **Query Phase**: When queried, the system:
   - Converts the query to embeddings
   - Retrieves relevant document chunks from Pinecone
   - Passes them to GPT-4o for context-aware response generation
   - Returns the answer with source attribution

## 🛠️ Configuration

### Text Splitter Settings
- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters

### Indexing Settings
- **Batch Size**: 500 documents per batch
- **Embedding Model**: `text-embedding-3-small`
- **Embedding Chunk Size**: 50

### LLM Settings
- **Model**: `gpt-4o`
- **Provider**: OpenAI

### Web Crawling Settings
- **Max Depth**: 5 levels
- **Max Breadth**: 20 pages per level
- **Max Pages**: 1000 pages

## 📝 Example

```python
from backend.core import run_llm

# Query the documentation bot
result = run_llm("How do I create an agent in LangChain?")

# Extract results
answer = result["answer"]
context = result["context"]

print("Question: How do I create an agent in LangChain?")
print("\nAnswer:")
print(answer)
print("\nSources used:")
for doc in context:
    print(f"- {doc.metadata.get('source', 'Unknown')}")
```

## 🚦 Error Handling

The ingestion pipeline includes error handling for:
- Failed batch insertions to vector store
- Connection issues with external APIs
- Document processing failures

## 🔄 Async Support

The project uses Python's `asyncio` for efficient parallel processing:
- Asynchronous document indexing
- Concurrent batch uploads to Pinecone
- Non-blocking API calls

## 📚 Learn More

- [LangChain Documentation](https://python.langchain.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Tavily API Documentation](https://tavily.com/)

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Created by [punithAJ-hub](https://github.com/punithAJ-hub)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report issues
- Submit pull requests
- Suggest improvements

## ⚠️ Notes

- The ingestion script currently indexes LangChain documentation. You can modify the URL and instructions to crawl different documentation sites.
- Ensure your Pinecone index is configured with the same dimensions as the embedding model (384 dimensions for `text-embedding-3-small`)
- API usage will incur costs with OpenAI, Pinecone, and Tavily services

---

**Status**: Active Development ✨
