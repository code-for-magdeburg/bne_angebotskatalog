import os
from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

ONLY_GET_REQUESTS = os.getenv("ONLY_GET_REQUESTS", "false").lower() == "true"


class GetOnlyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # If ONLY_GET_REQUESTS is enabled and the method is not GET, deny the request
        if ONLY_GET_REQUESTS and request.method != "GET":
            return JSONResponse(
                status_code=405,
                content={"detail": "Only GET requests are allowed"}
            )
        
        response = await call_next(request)
        return response