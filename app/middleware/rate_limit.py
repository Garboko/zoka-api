from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/hour"],
    storage_uri="memory://" 
)

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Handler personnalisé pour les erreurs de rate limit"""
    logger.warning(
        f"Rate limit exceeded for {get_remote_address(request)} on {request.url.path}"
    )
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many requests. Please try again later.",
            "retry_after": exc.detail
        }
    )