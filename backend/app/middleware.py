import os
from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

ONLY_GET_REQUESTS = os.getenv("ONLY_GET_REQUESTS", "false").lower() == "true"


class GetOnlyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # If ONLY_GET_REQUESTS is enabled and the method is not GET, deny the request
        if ONLY_GET_REQUESTS and request.method != "GET":
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Only GET requests are allowed"
            )
        
        response = await call_next(request)
        return response