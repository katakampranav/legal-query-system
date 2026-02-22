"""Initialize endpoints module."""

from src.endpoints.health import router as health_router
from src.endpoints.legal_qa import router as legal_qa_router
from src.endpoints.ingest import router as ingest_router

__all__ = ["health_router", "legal_qa_router", "ingest_router"]
