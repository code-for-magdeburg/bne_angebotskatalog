# Router for institution
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exc

from ..models import InstitutionCreate, InstitutionOut, InstitutionUpdate
from ..database import get_async_session
from ..orm import Institution


router = APIRouter()


@router.post("/", response_model=InstitutionOut, status_code=status.HTTP_201_CREATED)
async def create_institution(
    institution: InstitutionCreate,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        db_institution = Institution(
            institution_type=institution.institution_type,
            name=institution.name,
            description=institution.description,
            address_id=institution.address_id,
            logo_url=institution.logo_url,
            link_id=institution.link_id,
        )
        db.add(db_institution)
        await db.commit()
        await db.refresh(db_institution)
        return db_institution
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

@router.get("/{institution_id}", response_model=InstitutionOut)
async def get_institution(
    institution_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        result = await db.execute(select(Institution).where(Institution.id == institution_id))
        institution = result.scalar_one_or_none()
        
        if institution is None:
            raise HTTPException(
                status_code=404,
                detail="Institution not found"
            )
            
        return institution
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/", response_model=list[InstitutionOut])
async def get_institutions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        result = await db.execute(select(Institution).offset(skip).limit(limit))
        institutions = result.scalars().all()
        return institutions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.put("/{institution_id}", response_model=InstitutionOut)
async def update_institution(
    institution_id: int,
    institution_update: InstitutionUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        # Fetch the existing institution
        result = await db.execute(select(Institution).where(Institution.id == institution_id))
        db_institution = result.scalar_one_or_none()
        
        if db_institution is None:
            raise HTTPException(
                status_code=404,
                detail="Institution not found"
            )
        
        # Update the institution fields if provided
        if institution_update.institution_type is not None:
            db_institution.institution_type = institution_update.institution_type
        if institution_update.name is not None:
            db_institution.name = institution_update.name
        if institution_update.description is not None:
            db_institution.description = institution_update.description
        if institution_update.address_id is not None:
            db_institution.address_id = institution_update.address_id
        if institution_update.logo_url is not None:
            db_institution.logo_url = institution_update.logo_url
        if institution_update.link_id is not None:
            db_institution.link_id = institution_update.link_id
            
        await db.commit()
        await db.refresh(db_institution)
        return db_institution
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
