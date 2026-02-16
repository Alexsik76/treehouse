import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.infrastructure import (
    InfrastructureItemCreate,
    InfrastructureItemResponse,
    InfrastructureItemUpdate,
)
from src.services.infrastructure import InfrastructureService

router = APIRouter(prefix="/infrastructure", tags=["infrastructure"])
logger = logging.getLogger(__name__)


def get_infrastructure_service(db: AsyncSession = Depends(get_db)) -> InfrastructureService:
    return InfrastructureService(db)


@router.post("/", response_model=InfrastructureItemResponse, status_code=status.HTTP_201_CREATED)
async def create_infrastructure_item(
    item: InfrastructureItemCreate,
    service: InfrastructureService = Depends(get_infrastructure_service),
):
    logger.info(f"Creating item: {item.name}")
    try:
        return await service.create_item(item)
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Could not create item")


@router.get("/", response_model=List[InfrastructureItemResponse])
async def read_infrastructure_items(
    skip: int = 0,
    limit: int = 100,
    service: InfrastructureService = Depends(get_infrastructure_service),
):
    logger.debug("Fetching root items")
    return await service.get_root_items(skip, limit)


@router.get("/{item_id}", response_model=InfrastructureItemResponse)
async def read_infrastructure_item(
    item_id: int,
    decrypt_secrets: bool = False,
    service: InfrastructureService = Depends(get_infrastructure_service),
):
    item = await service.get_item_with_descendants(item_id, decrypt_secrets)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=InfrastructureItemResponse)
async def update_infrastructure_item(
    item_id: int,
    item: InfrastructureItemUpdate,
    service: InfrastructureService = Depends(get_infrastructure_service),
):
    updated_item = await service.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_infrastructure_item(
    item_id: int,
    service: InfrastructureService = Depends(get_infrastructure_service),
):
    success = await service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None