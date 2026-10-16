# Main FastAPI application
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import institution_router, offers_router
from .database import init_db

app = FastAPI(title="Institution API")

#@app.on_event("startup")
#async def startup_event():
#    await init_db()

app.include_router(institution_router, prefix="/api")
app.include_router(offers_router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Serve static files from public directory
app.mount("/public", StaticFiles(directory="public"), name="public")
