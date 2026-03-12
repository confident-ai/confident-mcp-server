import logging
import sys
import os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("confident-mcp")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        method = request.method
        url = request.url.path
        
        logger.info(f"Incoming {method} - {url} from {client_ip}")
        
        response = await call_next(request)
        
        logger.info(f"Completed {method} {url} - Status: {response.status_code}")
        return response