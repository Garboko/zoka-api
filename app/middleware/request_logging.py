import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        request_info = {
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown")
        }
        
        try:
            response: Response = await call_next(request)
            
            process_time = time.time() - start_time
            
            logger.info(
                f"{request_info['method']} {request_info['path']} "
                f"- Status: {response.status_code} "
                f"- Time: {process_time:.3f}s "
                f"- Client: {request_info['client']}"
            )
            
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"{request_info['method']} {request_info['path']} "
                f"- Error: {str(e)} "
                f"- Time: {process_time:.3f}s "
                f"- Client: {request_info['client']}",
                exc_info=True
            )
            raise