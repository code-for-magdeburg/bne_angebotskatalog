# Main FastAPI application
from fastapi import FastAPI
from .routers import institution_router, offers_router

app = FastAPI(title="Institution API")

app.include_router(institution_router, prefix="/api")
app.include_router(offers_router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}
