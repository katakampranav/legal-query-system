"""Application factory — builds and returns the FastAPI app."""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.config import api_settings
from src.endpoints import health_router, legal_qa_router, ingest_router


def _configure_logging() -> None:
    """Set up a readable log format for the server."""
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    date_fmt = "%H:%M:%S"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt, datefmt=date_fmt))

    root = logging.getLogger()
    root.setLevel(logging.DEBUG if api_settings.debug else logging.INFO)
    # Remove any existing handlers (prevents duplicate output with uvicorn)
    root.handlers.clear()
    root.addHandler(handler)

    # Keep uvicorn's own loggers at INFO so we still see request lines
    for uv_logger in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        logging.getLogger(uv_logger).setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    # --- Startup ---
    print(f"{api_settings.app_name} v{api_settings.version} starting...")
    print(f"LLM Model: {api_settings.groq_model}")
    print(f"Pinecone Index: {api_settings.pinecone_index}")
    print(f"Retrieval Args (k={api_settings.retrieval_k})")

    # Verify Pinecone connectivity on startup
    try:
        from src.services.retriever import verify_pinecone
        await verify_pinecone()
        print("Pinecone index accessible ✓")
    except Exception as e:
        print(f"WARNING: Pinecone not accessible — {e}")
        print("The server will start, but retrieval will fail until Pinecone is up.")

    yield  # App is running

    # --- Shutdown ---
    print("Shutting down...")


def init_app() -> FastAPI:
    """Application factory."""
    _configure_logging()
    app = FastAPI(
        title=api_settings.app_name,
        version=api_settings.version,
        debug=api_settings.debug,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.cors_allow_origins,
        allow_credentials=api_settings.cors_allow_credentials,
        allow_methods=api_settings.cors_allow_methods,
        allow_headers=api_settings.cors_allow_headers,
    )

    # Routers
    api_prefix = api_settings.api_prefix
    app.include_router(health_router, prefix=api_prefix)
    app.include_router(legal_qa_router, prefix=api_prefix)
    app.include_router(ingest_router, prefix=api_prefix)

    return app
