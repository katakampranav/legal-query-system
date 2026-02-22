"""Health check endpoint."""

import logging

from fastapi import APIRouter

from src.app.config import api_settings
from src.models import HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse with service status
    """
    try:
        # Try to verify Pinecone
        from src.services.retriever import verify_pinecone

        pinecone_ok = False
        try:
            await verify_pinecone()
            pinecone_ok = True
        except Exception:
            pass

        return HealthResponse(
            status="healthy" if pinecone_ok else "degraded",
            version=api_settings.version,
            services={
                "pinecone": "ok" if pinecone_ok else "unavailable",
                "llm": "ok",
            },
        )

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="unhealthy",
            version=api_settings.version,
            services={
                "pinecone": "unavailable",
                "llm": "unavailable",
            },
        )
