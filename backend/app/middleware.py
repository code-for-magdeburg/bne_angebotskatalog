import os
from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class GetOnlyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # If the method is not GET, deny the request
        if request.method != "GET":
            return JSONResponse(
                status_code=405,
                content={"detail": "Only GET requests are allowed"}
            )
        
        response = await call_next(request)
        return response