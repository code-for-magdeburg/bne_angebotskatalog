# Router for offers
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exc, and_
from typing import List, Optional

from ..models import OfferCreate, OfferOut, OfferUpdate
from ..database import get_async_session
from ..orm import Offer, OfferLocation, OfferTargetGroup, OfferSdg

ONLY_GET_REQUESTS = os.getenv("ONLY_GET_REQUESTS", "false").lower() == "true"

router = APIRouter()

if not ONLY_GET_REQUESTS:
    @router.post("/", response_model=OfferOut, status_code=status.HTTP_201_CREATED)
    async def create_offer(
        offer: OfferCreate,
        db: AsyncSession = Depends(get_async_session),
    ):
        try:
            # Create the main offer
            db_offer = Offer(
                institution_id=offer.institution_id,
                offer_type=offer.offer_type,
                name=offer.name,
                image_url=offer.image_url,
                description=offer.description,
                address_id=offer.location_address_id,
                timeframe_duration_minutes=offer.timeframe.duration_minutes,
                timeframe_recurrence_interval=offer.timeframe.recurrence.interval if offer.timeframe.recurrence else None,
                timeframe_recurrence_unit=offer.timeframe.recurrence.unit if offer.timeframe.recurrence else None,
                timeframe_note=offer.timeframe.note,
                cost_type=offer.cost.cost_type,
                cost_amount=offer.cost.amount if hasattr(offer.cost, 'amount') else None,
                cost_currency=offer.cost.currency if hasattr(offer.cost, 'currency') else None,
                cost_unit=offer.cost.unit if hasattr(offer.cost, 'unit') else None,
                cost_note=offer.cost.note if hasattr(offer.cost, 'note') else None,
                min_participants=offer.min_participants,
                max_participants=offer.max_participants,
            )
            db.add(db_offer)
            await db.commit()
            await db.refresh(db_offer)
            
            # Create offer locations
            for location in offer.location:
                db_location = OfferLocation(
                    offer_id=db_offer.id,
                    location=location
                )
                db.add(db_location)
            
            # Create offer target groups
            for target_group in offer.target_groups:
                db_target_group = OfferTargetGroup(
                    offer_id=db_offer.id,
                    target_group=target_group
                )
                db.add(db_target_group)
            
            # Create offer SDGs
            for sdg in offer.sdgs:
                db_sdg = OfferSdg(
                    offer_id=db_offer.id,
                    sdg=sdg
                )
                db.add(db_sdg)
            
            await db.commit()
            
            # Refresh to get all relationships
            await db.refresh(db_offer)
            return db_offer
        except exc.IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

@router.get("/{offer_id}", response_model=OfferOut)
async def get_offer(
    offer_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        result = await db.execute(select(Offer).where(Offer.id == offer_id))
        offer = result.scalar_one_or_none()
        
        if offer is None:
            raise HTTPException(
                status_code=404,
                detail="Offer not found"
            )
            
        return offer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/", response_model=List[OfferOut])
async def get_offers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        result = await db.execute(select(Offer).offset(skip).limit(limit))
        offers = result.scalars().all()
        return offers
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if not ONLY_GET_REQUESTS:
    @router.put("/{offer_id}", response_model=OfferOut)
    async def update_offer(
        offer_id: int,
        offer_update: OfferUpdate,
        db: AsyncSession = Depends(get_async_session),
    ):
        try:
            # Get the existing offer
            result = await db.execute(select(Offer).where(Offer.id == offer_id))
            db_offer = result.scalar_one_or_none()
            
            if db_offer is None:
                raise HTTPException(
                    status_code=404,
                    detail="Offer not found"
                )
            
            # Update offer fields
            update_data = offer_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                if key not in ["location", "target_groups", "sdgs"]:
                    setattr(db_offer, key, value)
            
            # Handle relationships if provided
            if offer_update.location is not None:
                # Delete existing locations
                await db.execute(OfferLocation.__table__.delete().where(OfferLocation.offer_id == offer_id))
                # Add new locations
                for location in offer_update.location:
                    db_location = OfferLocation(
                        offer_id=offer_id,
                        location=location
                    )
                    db.add(db_location)
            
            if offer_update.target_groups is not None:
                # Delete existing target groups
                await db.execute(OfferTargetGroup.__table__.delete().where(OfferTargetGroup.offer_id == offer_id))
                # Add new target groups
                for target_group in offer_update.target_groups:
                    db_target_group = OfferTargetGroup(
                        offer_id=offer_id,
                        target_group=target_group
                    )
                    db.add(db_target_group)
            
            if offer_update.sdgs is not None:
                # Delete existing SDGs
                await db.execute(OfferSdg.__table__.delete().where(OfferSdg.offer_id == offer_id))
                # Add new SDGs
                for sdg in offer_update.sdgs:
                    db_sdg = OfferSdg(
                        offer_id=offer_id,
                        sdg=sdg
                    )
                    db.add(db_sdg)
            
            await db.commit()
            await db.refresh(db_offer)
            return db_offer
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    @router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_offer(
        offer_id: int,
        db: AsyncSession = Depends(get_async_session),
    ):
        try:
            result = await db.execute(select(Offer).where(Offer.id == offer_id))
            offer = result.scalar_one_or_none()
            
            if offer is None:
                raise HTTPException(
                    status_code=404,
                    detail="Offer not found"
                )
            
            await db.delete(offer)
            await db.commit()
            return
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )