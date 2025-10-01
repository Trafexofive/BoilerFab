"""
Items API routes for {{PROJECT_NAME}}
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..database.session import get_db
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()


@router.post("/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Create new item
    """
    db_item = Item(
        title=item.title,
        description=item.description,
        owner_id=current_user["id"]
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[ItemResponse])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve items for current user
    """
    items = db.query(Item).filter(Item.owner_id == current_user["id"]).offset(skip).limit(limit).all()
    return items


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Get item by ID
    """
    item = db.query(Item).filter(Item.id == item_id, Item.owner_id == current_user["id"]).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item