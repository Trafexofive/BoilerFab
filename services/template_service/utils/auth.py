"""
Authentication utilities for the FastAPI Template Service
"""
from fastapi import Request, HTTPException
from ..auth.api_key import api_key_manager


def verify_api_key(request: Request) -> bool:
    """Verify API key from header or query parameter"""
    # Check header first
    api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization')
    
    # If not in header, check query parameter
    if not api_key:
        api_key = request.query_params.get('api_key')
    
    # Handle Bearer token format
    if api_key and api_key.startswith('Bearer '):
        api_key = api_key[7:]
    
    if not api_key or not api_key_manager.validate_api_key(api_key):
        return False
    return True


def require_api_key(request: Request):
    """Decorator-like function to require API key"""
    if not verify_api_key(request):
        raise HTTPException(status_code=401, detail="Invalid API Key")