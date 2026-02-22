"""Document ingestion endpoint."""

import logging

from fastapi import APIRouter

from src.app.handlers import handle_endpoint
from src.models import IngestRequest, IngestResponse
from src.services.ingestion import ingestion_service

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Ingestion"])


@router.post("/ingest", response_model=IngestResponse)
@handle_endpoint
async def ingest_documents(request: IngestRequest) -> IngestResponse:
    """Ingest legal documents into vector store.

    Args:
        request: IngestRequest with file path

    Returns:
        IngestResponse with ingestion status
    """
    logger.info(f"Ingestion request for: {request.file_path}")

    result = await ingestion_service.ingest_documents(
        pdf_path=request.file_path,
    )

    return IngestResponse(
        status=result["status"],
        chunks_processed=result["chunks_processed"],
        message=result["message"],
    )
