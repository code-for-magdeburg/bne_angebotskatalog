# Main FastAPI application
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import institution_router, offers_router
from .database import init_db
from .middleware import GetOnlyMiddleware

app = FastAPI(title="Institution API")

# Check if only GET requests should be allowed
ONLY_GET_REQUESTS = os.getenv("ONLY_GET_REQUESTS", "false").lower() == "true"

if not ONLY_GET_REQUESTS:
    app.include_router(institution_router, prefix="/api")
    app.include_router(offers_router, prefix="/api")

# Add middleware to enforce GET-only requests when enabled
app.add_middleware(GetOnlyMiddleware)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Serve static files from public directory
app.mount("/public", StaticFiles(directory="public"), name="public")
