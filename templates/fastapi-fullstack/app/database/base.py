"""
Base database imports for {{PROJECT_NAME}}
"""

from .session import Base

# Import all models here to make sure they are registered with SQLAlchemy
from ..models.user import User
from ..models.item import Item