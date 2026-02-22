"""Legal QA Runner — orchestrates the graph execution."""

import logging
from typing import Dict, Any

from src.graph.legal_qa_graph import legal_qa_graph
from src.state.graph_state import QAGraphState

logger = logging.getLogger(__name__)


async def run_legal_qa(
    question: str,
    mode: str = "normal",
    session_id: str = None,
) -> Dict[str, Any]:
    """Run the legal QA pipeline.

    Args:
        question: The legal question
        mode: Response mode ("lawyer" or "normal")
        session_id: Optional session ID for tracking

    Returns:
        Dictionary with answer and metadata
    """
    try:
        # Initialize state
        initial_state: QAGraphState = {
            "question": question,
            "context": "",
            "is_legal": False,
            "relevant": False,
            "rewritten_question": "",
            "mode": mode,
            "answer": "",
            "citations": [],
        }

        logger.info(f"Running legal QA for: {question[:50]}...")

        # Execute graph (use ainvoke for async nodes)
        result = await legal_qa_graph.ainvoke(initial_state)

        logger.info("Legal QA pipeline completed")

        return {
            "answer": result.get("answer", ""),
            "mode": mode,
            "session_id": session_id,
            "is_legal": result.get("is_legal", False),
            "context_used": len(result.get("context", "")) > 0,
        }

    except Exception as e:
        logger.error(f"Legal QA execution error: {e}")
        raise
