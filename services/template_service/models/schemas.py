"""
Data models for the FastAPI Template Service
"""
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime


class TemplateParameter(BaseModel):
    name: str
    type: str
    description: str
    default: Optional[Any] = None
    required: bool = True


class TemplateMetadata(BaseModel):
    name: str
    description: str
    version: str
    author: Optional[str] = None
    license: Optional[str] = None
    tags: List[str] = []
    parameters: List[TemplateParameter] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TemplateInfo(BaseModel):
    name: str
    description: str
    version: str
    author: Optional[str] = None
    tags: List[str] = []
    parameter_count: int = 0


class TemplateRegistrationRequest(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    author: Optional[str] = None
    license: Optional[str] = None
    tags: List[str] = []
    parameters: List[TemplateParameter] = []


class GenerateRequest(BaseModel):
    template_name: str
    project_name: str
    parameters: Dict[str, Any] = {}