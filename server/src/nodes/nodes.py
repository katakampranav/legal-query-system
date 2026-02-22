"""Graph nodes for the legal QA system."""

import logging

from src.llm.llm_client import llm_client
from src.models.prompts import (
    LEGAL_GATEKEEPER_PROMPT,
    LAWYER_PROMPT,
    NORMAL_PROMPT
)
from src.services.retriever import retriever
from src.state.graph_state import QAGraphState

logger = logging.getLogger(__name__)


async def domain_node(state: QAGraphState) -> dict:
    """Classify if question is legal AND optimize query in one step.

    Args:
        state: Current graph state

    Returns:
        Updated state with is_legal flag and optimized query (if legal)
    """
    try:
        logger.info("=" * 60)
        logger.info("📋 ENTERING DOMAIN_CHECK NODE")
        logger.info("=" * 60)
        logger.info(f"Question: {state['question'][:100]}...")

        # Single LLM call: classify + optimize
        prompt = LEGAL_GATEKEEPER_PROMPT.format(question=state["question"])
        result = llm_client.generate(prompt)
        
        result_clean = result.upper().strip()

        if result_clean == "NON_LEGAL":
            logger.info(f"❌ Classification: NON_LEGAL")
            logger.info("✨ Exiting domain_check node\n")
            return {"is_legal": False}
        else:
            # Result is the optimized query
            logger.info(f"✅ Classification: LEGAL")
            logger.info(f"✅ Optimized query: {result.strip()}")
            logger.info("✨ Exiting domain_check node\n")
            return {
                "is_legal": True,
                "current_query": result.strip()
            }
    except Exception as e:
        logger.error(f"❌ Domain node error: {e}", exc_info=True)
        raise


async def non_legal_response_node(state: QAGraphState) -> dict:
    """Handle non-legal questions with a friendly rejection message.

    Args:
        state: Current graph state

    Returns:
        Updated state with appropriate message
    """
    try:
        logger.info("=" * 60)
        logger.info("⚠️  ENTERING NON_LEGAL_RESPONSE NODE")
        logger.info("=" * 60)
        logger.info(f"Question: {state['question'][:100]}...")

        answer = """## This is a Legal QA System

I'm specifically designed to answer questions about Indian criminal law. Your question doesn't appear to be related to legal matters.

### What I Can Help With:
- Criminal law violations and penalties
- Police procedures and rights
- Arrest, bail, and court proceedings
- Legal sections of the Indian Penal Code
- Constitutional rights related to criminal law

### What I Cannot Help With:
- General knowledge questions
- Non-legal advice
- Personal opinions
- Topics outside of law

If you have a legal question, please feel free to ask! I'm here to help."""

        logger.info("✅ Generated non-legal response")
        logger.info("✨ Exiting non_legal_response node\n")

        return {"answer": answer}
    except Exception as e:
        logger.error(f"❌ Non-legal response node error: {e}", exc_info=True)
        raise


async def retrieve_node(state: QAGraphState) -> dict:
    """Retrieve relevant legal context using current query.

    Args:
        state: Current graph state

    Returns:
        Updated state with context
    """
    try:
        logger.info("=" * 60)
        logger.info("🔍 ENTERING RETRIEVE NODE")
        logger.info("=" * 60)

        current_query = state.get("current_query", state["question"])

        logger.info(f"Retrieving with query: {current_query[:100]}...")

        context = await retriever.retrieve(current_query)
        
        logger.info(f"✅ Retrieved {len(context)} characters of legal context")
        logger.info(f"Context preview: {context[:150]}...")
        logger.info("✨ Exiting retrieve node\n")

        return {
            "context": context,
        }
    except Exception as e:
        logger.error(f"❌ Retrieve node error: {e}", exc_info=True)
        raise


async def lawyer_response_node(state: QAGraphState) -> dict:
    """Generate lawyer-mode response from retrieved context.

    Args:
        state: Current graph state

    Returns:
        Updated state with answer
    """
    try:
        logger.info("=" * 60)
        logger.info("⚖️  ENTERING LAWYER_RESPONSE NODE")
        logger.info("=" * 60)

        question = state["question"]
        context = state["context"]

        logger.info(f"Generating lawyer-mode response")
        logger.info(f"Question: {question[:80]}...")
        logger.info(f"Using context of {len(context)} chars")

        prompt = LAWYER_PROMPT.format(
            question=question,
            context=context,
        )
        answer = llm_client.generate(prompt)

        logger.info("✅ Generated lawyer-mode response successfully")
        logger.info(f"Response preview: {answer[:150]}...")
        logger.info("✨ Exiting lawyer_response node\n")

        return {"answer": answer}
    except Exception as e:
        logger.error(f"❌ Lawyer response node error: {e}", exc_info=True)
        raise


async def normal_response_node(state: QAGraphState) -> dict:
    """Generate normal-mode response from retrieved context.

    Args:
        state: Current graph state

    Returns:
        Updated state with answer
    """
    try:
        logger.info("=" * 60)
        logger.info("👤 ENTERING NORMAL_RESPONSE NODE")
        logger.info("=" * 60)

        question = state["question"]
        context = state["context"]

        logger.info(f"Generating normal-mode response")
        logger.info(f"Question: {question[:80]}...")
        logger.info(f"Using context of {len(context)} chars")

        prompt = NORMAL_PROMPT.format(
            question=question,
            context=context,
        )
        answer = llm_client.generate(prompt)

        logger.info("✅ Generated normal-mode response successfully")
        logger.info(f"Response preview: {answer[:150]}...")
        logger.info("✨ Exiting normal_response node\n")

        return {"answer": answer}
    except Exception as e:
        logger.error(f"❌ Normal response node error: {e}", exc_info=True)
        raise
