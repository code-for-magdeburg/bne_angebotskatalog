# Pydantic models for all database tables
from typing import Optional, List, Union
from pydantic import BaseModel

# Address models
class AddressBase(BaseModel):
    address_recipient: Optional[str] = None
    address_recipient_addition: Optional[str] = None
    address_street: str
    address_city: str
    address_zip_code: str
    address_accessible: bool

class AddressCreate(AddressBase):
    pass

class AddressOut(AddressBase):
    id: int

    class Config:
        from_attributes = True

# Link models
class LinkBase(BaseModel):
    link_type: str
    value: str

class LinkCreate(LinkBase):
    pass

class LinkOut(LinkBase):
    id: int

    class Config:
        from_attributes = True

# Institution models
class InstitutionBase(BaseModel):
    institution_type: str
    name: str
    description: str
    address_id: int
    logo_url: Optional[str] = None
    link_id: Optional[int] = None

class InstitutionCreate(InstitutionBase):
    pass

class InstitutionOut(InstitutionBase):
    id: int

    class Config:
        from_attributes = True

# Agent models
class AgentBase(BaseModel):
    institution_id: int
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: str
    link_id: Optional[int] = None

class AgentCreate(AgentBase):
    pass

class AgentOut(AgentBase):
    id: int

    class Config:
        from_attributes = True

# Offer related models
class TimeframeCreate(BaseModel):
    duration_minutes: int
    recurrence_interval: Optional[int] = None
    recurrence_unit: Optional[str] = None
    note: Optional[str] = None

class CostCreate(BaseModel):
    cost_type: str
    amount: Optional[float] = None
    currency: str = "EUR"
    unit: Optional[str] = None
    note: Optional[str] = None

class OfferBase(BaseModel):
    institution_id: int
    offer_type: str
    name: str
    agent_id: Optional[int] = None
    image_url: Optional[str] = None
    description: str
    address_id: Optional[int] = None
    timeframe_duration_minutes: int
    timeframe_recurrence_interval: Optional[int] = None
    timeframe_recurrence_unit: Optional[str] = None
    timeframe_note: Optional[str] = None
    cost_type: str
    cost_amount: Optional[float] = None
    cost_currency: str = "EUR"
    cost_unit: Optional[str] = None
    cost_note: Optional[str] = None
    min_participants: int
    max_participants: int
    link_id: Optional[int] = None

class OfferCreate(OfferBase):
    pass

class OfferUpdate(BaseModel):
    institution_id: Optional[int] = None
    offer_type: Optional[str] = None
    name: Optional[str] = None
    agent_id: Optional[int] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    address_id: Optional[int] = None
    timeframe_duration_minutes: Optional[int] = None
    timeframe_recurrence_interval: Optional[int] = None
    timeframe_recurrence_unit: Optional[str] = None
    timeframe_note: Optional[str] = None
    cost_type: Optional[str] = None
    cost_amount: Optional[float] = None
    cost_currency: Optional[str] = None
    cost_unit: Optional[str] = None
    cost_note: Optional[str] = None
    min_participants: Optional[int] = None
    max_participants: Optional[int] = None
    link_id: Optional[int] = None

class OfferOut(OfferBase):
    id: int

    class Config:
        from_attributes = True

# OfferLocation models
class OfferLocationBase(BaseModel):
    offer_id: int
    location: str

class OfferLocationCreate(OfferLocationBase):
    pass

class OfferLocationOut(OfferLocationBase):
    pass

    class Config:
        from_attributes = True

# OfferTargetGroup models
class OfferTargetGroupBase(BaseModel):
    offer_id: int
    target_group: str

class OfferTargetGroupCreate(OfferTargetGroupBase):
    pass

class OfferTargetGroupOut(OfferTargetGroupBase):
    pass

    class Config:
        from_attributes = True

# OfferSdg models
class OfferSdgBase(BaseModel):
    offer_id: int
    sdg: int

class OfferSdgCreate(OfferSdgBase):
    pass

class OfferSdgOut(OfferSdgBase):
    pass

    class Config:
        from_attributes = True
