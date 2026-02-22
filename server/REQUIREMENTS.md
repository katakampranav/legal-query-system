# Legal QA Server Requirements

This file contains the core dependencies for the Legal QA Server.
The project uses uv for dependency management.

## Core Dependencies

- fastapi>=0.129.0
- uvicorn[standard]>=0.41.0
- pydantic>=2.0.0
- pydantic-settings>=2.13.0
- python-dotenv>=1.0.0

## LLM & Graph

- langgraph>=0.2.14
- langchain-core>=0.2.39
- langchain>=0.2.14
- openai>=1.40.0

## Vector Database & Embeddings

- pinecone-client>=3.2.0
- cohere>=5.5.0

## Utilities

- httpx>=0.28.0
- tiktoken>=0.7.0
- tqdm>=4.66.0
- requests>=2.32.0
- numpy>=1.26.0
- pypdf>=4.2.0
- llama-index>=0.10.0

## Development Dependencies

- pytest>=7.0.0
- pytest-asyncio>=0.23.0
- black>=23.0.0
- ruff>=0.1.0
- mypy>=1.0.0

## Installation

### Using uv (Recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -e .
```

## Running the Server

### Development Mode

```bash
# Windows
run.bat

# Linux/macOS
bash run.sh
```

### Production Mode

```bash
uv run uvicorn src.app.api:app --host 0.0.0.0 --port 8002
```

## API Documentation

Once the server is running, access the API documentation at:

- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc
