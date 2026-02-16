from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.orm.attributes import set_committed_value
from src.models.infrastructure import InfrastructureItem
from src.schemas.infrastructure import (
    InfrastructureItemCreate,
    InfrastructureItemUpdate,
)
from src.security import decrypt_data, encrypt_data


class InfrastructureService:
    SENSITIVE_KEYS = {"password", "secret", "token", "key", "root_password"}

    def __init__(self, db: AsyncSession):
        self.db = db

    def _process_specs_encryption(self, specs: Dict[str, Any], encrypt: bool = True) -> Dict[str, Any]:
        """Helper to encrypt or decrypt sensitive values in the specs dictionary."""
        if not specs:
            return {}
        processed = specs.copy()
        for k, v in processed.items():
            if any(s in k.lower() for s in self.SENSITIVE_KEYS) and isinstance(v, str):
                processed[k] = encrypt_data(v) if encrypt else decrypt_data(v)
        return processed

    def _build_tree(self, flat_items: List[InfrastructureItem]) -> List[InfrastructureItem]:
        """Reconstructs the hierarchical tree structure from a flat list of items."""
        id_map = {item.id: item for item in flat_items}
        roots = []

        # Initialize children list manually without triggering lazy loading
        for item in flat_items:
            # This is the FIX: set_committed_value prevents SQLAlchemy from 
            # trying to fetch the 'old' value of children from the DB.
            set_committed_value(item, "children", [])

        for item in flat_items:
            parent_id = item.parent_id
            if parent_id is None or parent_id not in id_map:
                roots.append(item)
            else:
                parent = id_map[parent_id]
                # Since 'children' is now a plain list (thanks to set_committed_value),
                # we can append to it without DB interaction.
                parent.children.append(item)
        
        return roots

    async def get_item_with_descendants(self, item_id: int, decrypt_secrets: bool = False) -> Optional[InfrastructureItem]:
        """Fetches a single item and all its descendants using a Recursive CTE."""
        # 1. Recursive CTE definition
        hierarchy = select(InfrastructureItem).where(InfrastructureItem.id == item_id).cte(name="hierarchy", recursive=True)

        parent = aliased(hierarchy, name="parent")
        child = aliased(InfrastructureItem, name="child")

        hierarchy = hierarchy.union_all(
            select(child).where(child.parent_id == parent.c.id)
        )

        # 2. Select items joining with the CTE
        stmt = select(InfrastructureItem).join(hierarchy, InfrastructureItem.id == hierarchy.c.id)
        result = await self.db.execute(stmt)
        flat_items = result.scalars().all()

        if not flat_items:
            return None

        # 3. Rebuild tree structure
        tree_nodes = self._build_tree(flat_items)
        
        # Find the requested root node
        target_item = next((i for i in tree_nodes if i.id == item_id), None)
        
        if target_item and decrypt_secrets:
             target_item.specs = self._process_specs_encryption(target_item.specs, encrypt=False)

        return target_item

    async def get_root_items(self, skip: int = 0, limit: int = 100) -> List[InfrastructureItem]:
        """Fetches root items and builds their full subtrees."""
        # 1. Fetch root IDs with pagination
        roots_stmt = (
            select(InfrastructureItem.id)
            .where(InfrastructureItem.parent_id.is_(None))
            .offset(skip)
            .limit(limit)
        )
        roots_result = await self.db.execute(roots_stmt)
        root_ids = roots_result.scalars().all()

        if not root_ids:
            return []

        # 2. Recursive CTE for all identified roots
        hierarchy = select(InfrastructureItem).where(InfrastructureItem.id.in_(root_ids)).cte(name="hierarchy", recursive=True)
        
        parent = aliased(hierarchy, name="parent")
        child = aliased(InfrastructureItem, name="child")
        
        hierarchy = hierarchy.union_all(
            select(child).where(child.parent_id == parent.c.id)
        )
        
        stmt = select(InfrastructureItem).join(hierarchy, InfrastructureItem.id == hierarchy.c.id)
        result = await self.db.execute(stmt)
        flat_items = result.scalars().all()
        
        return self._build_tree(flat_items)

    async def create_item(self, item_dto: InfrastructureItemCreate) -> InfrastructureItem:
        encrypted_specs = self._process_specs_encryption(item_dto.specs, encrypt=True)
        
        db_item = InfrastructureItem(
            name=item_dto.name,
            type=item_dto.type,
            ip_address=item_dto.ip_address,
            dns_name=item_dto.dns_name,
            specs=encrypted_specs,
            parent_id=item_dto.parent_id,
        )
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        
        # Return complete tree structure
        return await self.get_item_with_descendants(db_item.id)

    async def update_item(self, item_id: int, update_dto: InfrastructureItemUpdate) -> Optional[InfrastructureItem]:
        # Use simpler query for update to avoid CTE overhead if checking existence
        stmt = select(InfrastructureItem).where(InfrastructureItem.id == item_id)
        result = await self.db.execute(stmt)
        item = result.scalar_one_or_none()

        if not item:
            return None

        update_data = update_dto.model_dump(exclude_unset=True)

        if "specs" in update_data and update_data["specs"]:
            update_data["specs"] = self._process_specs_encryption(update_data["specs"], encrypt=True)

        for key, value in update_data.items():
            setattr(item, key, value)

        await self.db.commit()
        
        return await self.get_item_with_descendants(item.id)

    async def delete_item(self, item_id: int) -> bool:
        stmt = select(InfrastructureItem).where(InfrastructureItem.id == item_id)
        result = await self.db.execute(stmt)
        item = result.scalar_one_or_none()
        
        if not item:
            return False
            
        await self.db.delete(item)
        await self.db.commit()
        return True