"""Data models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class AskRequest(BaseModel):
    """Request model for asking legal questions."""

    question: str = Field(..., description="The legal question to ask", min_length=5)
    mode: Literal["lawyer", "normal"] = Field(
        default="normal",
        description="Response mode: lawyer (technical) or normal (simple)",
    )
    session_id: Optional[str] = Field(
        default=None, description="Optional session ID for tracking"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "question": "What happens if I don't pay my taxes?",
                "mode": "normal",
                "session_id": None,
            }
        }


class AskResponse(BaseModel):
    """Response model for legal questions."""

    answer: str = Field(..., description="The answer to the legal question")
    citations: Optional[List[str]] = Field(
        default=None, description="Optional list of citations"
    )
    mode: str = Field(..., description="Response mode used")
    session_id: Optional[str] = Field(default=None, description="Session ID if provided")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "answer": "Not paying taxes is a serious offense...",
                "citations": ["Section 276 of IPC", "Article 265 of Constitution"],
                "mode": "normal",
                "session_id": None,
            }
        }


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    services: dict = Field(..., description="Status of dependent services")


class IngestRequest(BaseModel):
    """Request model for document ingestion."""

    file_path: str = Field(..., description="Path to the file to ingest")
    document_type: Literal["pdf", "text"] = Field(
        default="pdf", description="Type of document"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "file_path": "/data/legal_docs/ipc.pdf",
                "document_type": "pdf",
            }
        }


class IngestResponse(BaseModel):
    """Response model for document ingestion."""

    status: str = Field(..., description="Ingestion status")
    chunks_processed: int = Field(..., description="Number of chunks processed")
    message: str = Field(..., description="Status message")
