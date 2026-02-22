"""Graph state definition for legal QA system."""

from typing import TypedDict


class QAGraphState(TypedDict):
    """State for the legal QA graph."""

    question: str
    """The original user question"""

    context: str
    """Retrieved legal context"""

    is_legal: bool
    """Whether the question is legal-related"""

    relevant: bool
    """Whether the context is relevant to the question"""

    rewritten_question: str
    """The rewritten question for better retrieval"""

    mode: str
    """Response mode: 'lawyer' or 'normal'"""

    answer: str
    """The final answer"""

    citations: list
    """List of citations from responses"""

    retrieval_attempts: int
    """Number of retrieval attempts made"""

    current_query: str
    """Current query being used for retrieval (original or rewritten)"""
