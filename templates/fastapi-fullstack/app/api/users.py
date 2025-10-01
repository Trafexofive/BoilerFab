"""
Users API routes for {{PROJECT_NAME}}
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..database.session import get_db
from ..models.user import User
from ..schemas.auth import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Get current user information
    """
    return current_user


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve users (admin only in real implementation)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users