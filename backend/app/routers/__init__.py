# Institution router
from fastapi import APIRouter

# Create router instance for institution endpoints
institution_router = APIRouter(prefix="/institutions", tags=["institutions"])

# Import endpoint functions
from . import institution
institution_router.include_router(institution.router)

# Create router instance for offers endpoints
offers_router = APIRouter(prefix="/offers", tags=["offers"])

# Import endpoint functions
from . import offers
offers_router.include_router(offers.router)
