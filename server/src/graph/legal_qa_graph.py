"""Legal QA Graph — LangGraph pipeline for legal question answering."""

import logging

from langgraph.graph import StateGraph, END

from src.nodes.nodes import (
    domain_node,
    non_legal_response_node,
    retrieve_node,
    lawyer_response_node,
    normal_response_node,
)
from src.state.graph_state import QAGraphState

logger = logging.getLogger(__name__)


def build_graph():
    """Build and compile the legal QA state graph.

    Simplified Flow:
    1. domain_check → classify + optimize query (only 1 LLM call)
    2. domain_check → (conditional)
       - If NON_LEGAL: non_legal_response → END
       - If LEGAL: retrieve → response → END
    3. retrieve → fetch from Pinecone (1 retrieval)
    4. response → generate answer from context (1 LLM call)

    Total: 3 LLM calls max (domain + rewrite + response)
    vs. Previous: 7+ LLM calls (domain + relevance + rewrite + retry + relevance + rewrite + response)

    Returns:
        Compiled LangGraph for legal QA
    """
    builder = StateGraph(QAGraphState)

    # Add nodes
    builder.add_node("domain_check", domain_node)
    builder.add_node("non_legal_response", non_legal_response_node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("lawyer_response", lawyer_response_node)
    builder.add_node("normal_response", normal_response_node)

    # Set entry point
    builder.set_entry_point("domain_check")

    # Conditional edge after domain_check: check if it's a legal question
    def route_after_domain(state: QAGraphState) -> str:
        """Route based on whether question is legal-related.
        
        - If is_legal=True: proceed with retrieval
        - If is_legal=False: reject immediately
        """
        is_legal = state.get("is_legal", False)
        
        if is_legal:
            logger.info("\n✅ LEGAL QUESTION DETECTED - Proceeding to retrieval")
            logger.info(f"   Optimized query: {state.get('current_query', state['question'])[:80]}...\n")
            return "retrieve"
        else:
            logger.info("\n❌ NON-LEGAL QUESTION DETECTED - Rejecting\n")
            return "non_legal_response"

    builder.add_conditional_edges(
        "domain_check",
        route_after_domain,
        {
            "retrieve": "retrieve",
            "non_legal_response": "non_legal_response",
        },
    )

    # Edge: retrieve → response (mode-based routing)
    def route_to_response(state: QAGraphState) -> str:
        """Route to appropriate response node based on mode."""
        mode = state.get("mode", "normal")
        return "lawyer_response" if mode == "lawyer" else "normal_response"

    builder.add_conditional_edges(
        "retrieve",
        route_to_response,
        {
            "lawyer_response": "lawyer_response",
            "normal_response": "normal_response",
        },
    )

    # All response nodes end
    builder.add_edge("non_legal_response", END)
    builder.add_edge("lawyer_response", END)
    builder.add_edge("normal_response", END)

    compiled_graph = builder.compile()
    logger.info("\n" + "=" * 60)
    logger.info("✅ Legal QA graph compiled successfully")
    logger.info("=" * 60 + "\n")

    return compiled_graph


# Singleton instance
legal_qa_graph = build_graph()
