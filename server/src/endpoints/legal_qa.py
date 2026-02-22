"""Legal QA endpoint."""

import logging

from fastapi import APIRouter

from src.app.handlers import handle_endpoint
from src.models import AskRequest, AskResponse
from src.runner.legal_qa_runner import run_legal_qa

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Legal QA"])


@router.post("/ask", response_model=AskResponse, status_code=200)
@handle_endpoint
async def ask_legal_question(request: AskRequest) -> AskResponse:
    """Ask a legal question and get an answer.

    Args:
        request: AskRequest with question and mode

    Returns:
        AskResponse with answer and metadata
    """
    logger.info(f"Legal question received: {request.question[:50]}...")

    result = await run_legal_qa(
        question=request.question,
        mode=request.mode,
        session_id=request.session_id,
    )

    return AskResponse(
        answer=result["answer"],
        mode=result["mode"],
        session_id=result["session_id"],
    )
