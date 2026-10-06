# Pydantic models for Institution and Offer
from typing import Optional, List, Union
from pydantic import BaseModel

class AddressCreate(BaseModel):
    address_recipient: str
    address_recipient_addition: Optional[str] = None
    address_street: str
    address_city: str
    address_zip_code: str
    address_accessible: bool

class InstitutionCreate(BaseModel):
    institution_type: str
    name: str
    description: str
    address_id: int
    logo_url: Optional[str] = None
    link_id: Optional[int] = None

class InstitutionOut(InstitutionCreate):
    id: int

    class Config:
        from_attributes = True

# Offer related models
class TimeframeCreate(BaseModel):
    duration_minutes: int
    recurrence: Optional[dict] = None
    note: Optional[str] = None

class CostCreate(BaseModel):
    cost_type: str
    amount: Optional[float] = None
    currency: Optional[str] = None
    unit: Optional[str] = None
    note: Optional[str] = None

class OfferCreate(BaseModel):
    institution_id: int
    offer_type: str
    name: str
    image_url: Optional[str] = None
    description: str
    location: List[str]
    location_address_id: Optional[int] = None
    timeframe: TimeframeCreate
    cost: CostCreate
    agents: List[int] = []
    links: List[int] = []
    topics: List[str] = []
    interdisciplinary_topics: List[str] = []
    target_groups: List[str]
    min_participants: int
    max_participants: int
    sdgs: List[int]

class OfferUpdate(BaseModel):
    institution_id: Optional[int] = None
    offer_type: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[List[str]] = None
    location_address_id: Optional[int] = None
    timeframe: Optional[TimeframeCreate] = None
    cost: Optional[CostCreate] = None
    agents: Optional[List[int]] = None
    links: Optional[List[int]] = None
    topics: Optional[List[str]] = None
    interdisciplinary_topics: Optional[List[str]] = None
    target_groups: Optional[List[str]] = None
    min_participants: Optional[int] = None
    max_participants: Optional[int] = None
    sdgs: Optional[List[int]] = None

class OfferOut(OfferCreate):
    id: int

    class Config:
        from_attributes = True
