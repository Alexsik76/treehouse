import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database import get_db
from src.models.infrastructure import InfrastructureItem
from src.schemas.infrastructure import (
    InfrastructureItemCreate,
    InfrastructureItemResponse,
    InfrastructureItemUpdate,
)
from src.security import decrypt_data, encrypt_data

router = APIRouter(prefix="/infrastructure", tags=["infrastructure"])
logger = logging.getLogger(__name__)

# List of sensitive keys to automatically encrypt/decrypt
SENSITIVE_KEYS = ["password", "secret", "token", "key", "root_password"]


def process_specs_encryption(specs: dict, encrypt: bool = True) -> dict:
    """
    Helper to traverse specs dict and encrypt/decrypt values for keys containing sensitive words.
    """
    processed = specs.copy()
    for k, v in processed.items():
        if any(s in k.lower() for s in SENSITIVE_KEYS) and isinstance(v, str):
            processed[k] = encrypt_data(v) if encrypt else decrypt_data(v)
    return processed


@router.post("/", response_model=InfrastructureItemResponse, status_code=status.HTTP_201_CREATED)
async def create_infrastructure_item(
    item: InfrastructureItemCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new infrastructure item. Sensitive fields in specs are encrypted automatically.
    """
    logger.info(f"Creating item: {item.name}")
    
    # Encrypt sensitive data in specs
    encrypted_specs = process_specs_encryption(item.specs, encrypt=True)
    
    db_item = InfrastructureItem(
        name=item.name,
        type=item.type,
        ip_address=item.ip_address,
        dns_name=item.dns_name,
        specs=encrypted_specs,
        parent_id=item.parent_id,
    )
    db.add(db_item)
    try:
        await db.commit()
        await db.refresh(db_item, attribute_names=["id"])
        
        # Reload item with deep relationship loading to ensure Pydantic serialization works
        # matches update_infrastructure_item pattern
        stmt = (
            select(InfrastructureItem)
            .where(InfrastructureItem.id == db_item.id)
            .options(
                selectinload(InfrastructureItem.children)
                .selectinload(InfrastructureItem.children)
                .selectinload(InfrastructureItem.children)
                .selectinload(InfrastructureItem.children)
                .selectinload(InfrastructureItem.children)
            )
        )
        result = await db.execute(stmt)
        db_item = result.scalar_one()
        
        return db_item
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not create item")


@router.get("/", response_model=List[InfrastructureItemResponse])
async def read_infrastructure_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all root infrastructure items (items without parents).
    Children are loaded via recursion in the response model.
    """
    logger.debug("Fetching root items")
    try:
        # Only fetch root items to build the tree
        # We need to explicitly load children of children (recursion depth 2)
        # For deeper trees, we might need a recursive CTE or max depth limit
        stmt = (
            select(InfrastructureItem)
            .where(InfrastructureItem.parent_id.is_(None))
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(InfrastructureItem.children)
                .selectinload(InfrastructureItem.children)
                .selectinload(InfrastructureItem.children)
                .selectinload(InfrastructureItem.children)
                .selectinload(InfrastructureItem.children)
            )
        )
        result = await db.execute(stmt)
        items = result.scalars().all()
        return items
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        # Return error as detail for debugging
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        logger.error(f"Error fetching items: {e}")
        # Return error as detail for debugging
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/{item_id}", response_model=InfrastructureItemResponse)
async def read_infrastructure_item(
    item_id: int, decrypt_secrets: bool = False, db: AsyncSession = Depends(get_db)
):
    """
    Get a specific item by ID.
    Query param `decrypt_secrets=true` will decrypt sensitive fields in specs.
    """
    stmt = (
        select(InfrastructureItem)
        .where(InfrastructureItem.id == item_id)
        .options(
            selectinload(InfrastructureItem.children)
            .selectinload(InfrastructureItem.children)
            .selectinload(InfrastructureItem.children)
            .selectinload(InfrastructureItem.children)
            .selectinload(InfrastructureItem.children)
        )
    )
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if decrypt_secrets:
        # We need to copy the object to avoid modifying the DB session instance state unexpectedly if we were to flush
        # But for response model serialization, we can create a temporary dict or modify a copy
        # Ideally, we should not mutate the ORM object. 
        # For simplicity in this demo, we modify the specs in the response object (not DB)
        decrypted_specs = process_specs_encryption(item.specs, encrypt=False)
        # We can't easily assign back to item.specs on the ORM object without tracking changes.
        # So we manually construct the response if needed, or let Pydantic handle it if we passed a dict.
        # A clean way is to return the item, but if decrypt is requested, we assume the user accepts the overhead.
        # Let's clone the item into a Pydantic model and modify it.
        item_response = InfrastructureItemResponse.model_validate(item)
        item_response.specs = decrypted_specs
        return item_response

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_infrastructure_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an item by ID.
    """
    logger.info(f"Deleting item {item_id}")
    stmt = select(InfrastructureItem).where(InfrastructureItem.id == item_id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
        
    await db.delete(item)
    await db.commit()
    return None

@router.put("/{item_id}", response_model=InfrastructureItemResponse)
async def update_infrastructure_item(
    item_id: int, item: InfrastructureItemUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update an infrastructure item.
    """
    stmt = select(InfrastructureItem).where(InfrastructureItem.id == item_id)
    result = await db.execute(stmt)
    db_item = result.scalar_one_or_none()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item.model_dump(exclude_unset=True)

    # Handle encryption for specs if present
    if "specs" in update_data and update_data["specs"]:
        update_data["specs"] = process_specs_encryption(update_data["specs"], encrypt=True)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    await db.commit()
    
    # Reload item with deep relationship loading to ensure Pydantic serialization works
    # This mirrors the logic in read_infrastructure_items to prevent MissingGreenlet errors
    stmt = (
        select(InfrastructureItem)
        .where(InfrastructureItem.id == item_id)
        .options(
            selectinload(InfrastructureItem.children)
            .selectinload(InfrastructureItem.children)
            .selectinload(InfrastructureItem.children)
            .selectinload(InfrastructureItem.children)
            .selectinload(InfrastructureItem.children)
        )
    )
    result = await db.execute(stmt)
    db_item = result.scalar_one()
    
    return db_item
