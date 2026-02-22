"""Application configuration management with Pydantic Settings."""

from pydantic_settings import BaseSettings
from typing import List


class APISettings(BaseSettings):
    """API configuration settings."""

    # App metadata
    app_name: str = "Legal QA Server"
    version: str = "0.1.0"
    debug: bool = False

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # API configuration
    api_prefix: str = "/api/v1"

    # LLM Configuration (Groq)
    groq_api_key: str
    groq_model: str = "mixtral-8x7b-32768"
    llm_temperature: float = 0.0

    # Vector Database Configuration
    pinecone_api_key: str
    pinecone_index: str = "legal-docs"
    retrieval_k: int = 4

    # Embedding Model Configuration
    cohere_api_key: str
    embedding_model: str = "embed-english-v3.0"

    # Ingestion Configuration
    ingestion_batch_size: int = 32
    ingestion_chunk_size: int = 512

    # CORS Configuration
    cors_allow_origins: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://localhost:8002"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Logging
    log_level: str = "INFO"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False
        json_schema_extra = {
            "example": {
                "app_name": "Legal QA Server",
                "version": "0.1.0",
                "debug": False,
            }
        }


# Load settings
api_settings = APISettings()
