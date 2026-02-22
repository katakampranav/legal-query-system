"""Pinecone retriever service for legal document retrieval."""

import logging
from typing import List

import cohere
from pinecone import Pinecone

from src.app.config import api_settings

logger = logging.getLogger(__name__)


class RetrieverService:
    """Service for retrieving legal documents from Pinecone."""

    def __init__(self) -> None:
        """Initialize retriever with Cohere embeddings and Pinecone vector store."""
        self.co = cohere.Client(api_settings.cohere_api_key)
        self.pc = Pinecone(api_key=api_settings.pinecone_api_key)
        self.index = self.pc.Index(api_settings.pinecone_index)
        self.embedding_model = api_settings.embedding_model
        self.retrieval_k = api_settings.retrieval_k

    async def retrieve(self, query: str, k: int = None) -> str:
        """Retrieve relevant legal documents from Pinecone.

        Args:
            query: The query string
            k: Number of results to retrieve (uses default if not provided)

        Returns:
            Concatenated context from retrieved documents
        """
        try:
            k = k or self.retrieval_k

            # Embed the query using Cohere
            embedding_response = self.co.embed(
                texts=[query],
                model=self.embedding_model,
                input_type="search_query",
            )

            embedding = embedding_response.embeddings[0]

            # Query Pinecone
            results = self.index.query(
                vector=embedding,
                top_k=k,
                include_metadata=True,
            )

            # Extract contexts from results
            contexts = []
            for match in results.get("matches", []):
                if "metadata" in match and "_node_content" in match["metadata"]:
                    contexts.append(match["metadata"]["_node_content"])

            return "\n\n".join(contexts) if contexts else ""

        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            raise

    async def retrieve_with_scores(
        self, query: str, k: int = None
    ) -> List[tuple]:
        """Retrieve documents with relevance scores.

        Args:
            query: The query string
            k: Number of results to retrieve

        Returns:
            List of (content, score) tuples
        """
        try:
            k = k or self.retrieval_k

            # Embed the query
            embedding_response = self.co.embed(
                texts=[query],
                model=self.embedding_model,
                input_type="search_query",
            )

            embedding = embedding_response.embeddings[0]

            # Query Pinecone
            results = self.index.query(
                vector=embedding,
                top_k=k,
                include_metadata=True,
            )

            # Extract contexts with scores
            results_with_scores = []
            for match in results.get("matches", []):
                if "metadata" in match and "_node_content" in match["metadata"]:
                    content = match["metadata"]["_node_content"]
                    score = match.get("score", 0.0)
                    results_with_scores.append((content, score))

            return results_with_scores

        except Exception as e:
            logger.error(f"Retrieval with scores error: {e}")
            raise


async def verify_pinecone() -> bool:
    """Verify Pinecone connectivity.

    Returns:
        True if Pinecone is accessible
    """
    try:
        pc = Pinecone(api_key=api_settings.pinecone_api_key)
        index = pc.Index(api_settings.pinecone_index)
        # Try to get index description to verify connection
        index.describe_index_stats()
        return True
    except Exception as e:
        logger.error(f"Pinecone verification failed: {e}")
        raise


# Singleton instance
retriever = RetrieverService()
