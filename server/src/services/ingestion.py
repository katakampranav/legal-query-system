"""Document ingestion service for legal documents."""

import logging
import re
import time
from pathlib import Path
from typing import List

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document
from llama_index.core.settings import Settings
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from pypdf import PdfReader

from src.app.config import api_settings

logger = logging.getLogger(__name__)


class ThrottledCohereEmbedding(CohereEmbedding):
    """Cohere embedding with rate limiting for API throttling."""

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings with rate limiting.

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings
        """
        embeddings = super()._get_text_embeddings(texts)
        time.sleep(2)  # Rate limiting
        return embeddings


class DocumentIngestionService:
    """Service for ingesting legal documents into Pinecone."""

    def __init__(self) -> None:
        """Initialize ingestion service."""
        self._setup_embeddings()
        self._setup_chunking()
        self._setup_pinecone()

    def _setup_embeddings(self) -> None:
        """Setup Cohere embeddings with rate limiting."""
        try:
            Settings.embed_model = ThrottledCohereEmbedding(
                api_key=api_settings.cohere_api_key,
                model_name=api_settings.embedding_model,
                embed_batch_size=5,
            )
            logger.info("Cohere embeddings configured")
        except Exception as e:
            logger.error(f"Failed to setup embeddings: {e}")
            raise

    def _setup_chunking(self) -> None:
        """Setup document chunking strategy optimized for legal documents."""
        try:
            Settings.node_parser = SentenceSplitter(
                chunk_size=api_settings.ingestion_chunk_size,
                chunk_overlap=200,  # Important: overlap for legal context
            )
            logger.info("Document chunking configured")
        except Exception as e:
            logger.error(f"Failed to setup chunking: {e}")
            raise

    def _setup_pinecone(self) -> None:
        """Setup Pinecone vector store."""
        try:
            self.pc = Pinecone(api_key=api_settings.pinecone_api_key)

            # Create index if not exists
            if api_settings.pinecone_index not in [
                i.name for i in self.pc.list_indexes()
            ]:
                logger.info(f"Creating Pinecone index: {api_settings.pinecone_index}")
                self.pc.create_index(
                    name=api_settings.pinecone_index,
                    dimension=1024,  # Cohere embedding dimension
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )

            self.pinecone_index = self.pc.Index(api_settings.pinecone_index)
            self.vector_store = PineconeVectorStore(
                pinecone_index=self.pinecone_index
            )
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )

            logger.info("Pinecone configured successfully")
        except Exception as e:
            logger.error(f"Failed to setup Pinecone: {e}")
            raise

    def _load_pdf_sections(self, pdf_path: str) -> List[Document]:
        """Load PDF and split into legal sections.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of Document objects with metadata
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF not found: {pdf_path}")

            reader = PdfReader(pdf_path)
            full_text = ""

            # Combine all pages
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += "\n" + text

            # Split using legal section pattern (e.g., "318. Cheating")
            pattern = r"\n\s*(\d{2,4})\.\s+([A-Za-z ,\-()]+)"
            splits = re.split(pattern, full_text)

            documents = []

            # Reassemble sections
            for i in range(1, len(splits), 3):
                if i + 2 < len(splits):
                    section_number = splits[i]
                    section_title = splits[i + 1]
                    section_text = splits[i + 2]

                    content = f"Section {section_number}: {section_title}\n{section_text}"

                    documents.append(
                        Document(
                            text=content,
                            metadata={
                                "section": section_number,
                                "offence": section_title.strip(),
                                "act": "BNS",
                            },
                        )
                    )

            logger.info(f"Loaded {len(documents)} legal sections from {pdf_path}")
            return documents

        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            raise

    async def ingest_documents(self, pdf_path: str) -> dict:
        """Ingest legal documents into vector store.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with ingestion status and results
        """
        try:
            logger.info(f"Starting document ingestion from {pdf_path}")

            # Load and parse documents
            documents = self._load_pdf_sections(pdf_path)

            if not documents:
                raise ValueError("No documents found in PDF")

            # Create index
            logger.info("Creating vector index...")
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=self.storage_context,
                show_progress=True,
            )

            logger.info(f"✅ Successfully ingested {len(documents)} documents")

            return {
                "status": "success",
                "chunks_processed": len(documents),
                "message": f"Successfully ingested {len(documents)} legal sections",
            }

        except Exception as e:
            logger.error(f"Document ingestion failed: {e}")
            raise


# Singleton instance
ingestion_service = DocumentIngestionService()
