"""Error handlers and decorators for API endpoints."""

import logging
from functools import wraps
from typing import Callable, Any

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


def handle_endpoint(func: Callable) -> Callable:
    """Decorator to handle common endpoint operations."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return JSONResponse(
                status_code=400,
                content={"detail": str(e)},
            )
        except Exception as e:
            logger.error(f"Unhandled error: {e}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )

    return wrapper
