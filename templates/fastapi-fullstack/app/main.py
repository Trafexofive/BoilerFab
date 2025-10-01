"""
{{PROJECT_NAME}} - FastAPI Application
A production-ready FastAPI application with authentication and database integration
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging

from .api import auth, users, items
from .core.config import settings
from .core.security import get_current_user
from .database.session import engine
from .database.base import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="{{PROJECT_NAME}}",
    description="A production-ready FastAPI application with authentication, database integration, and comprehensive testing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to {{PROJECT_NAME}} API!",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "{{PROJECT_NAME}}",
        "database": "{{database_type}}",
        "auth": "{{auth_method}}"
    }


@app.get("/api/v1/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    """Example protected route requiring authentication"""
    return {
        "message": f"Hello {current_user['username']}, this is a protected route!",
        "user_id": current_user["id"]
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": "2024-01-01T00:00:00Z"  # In real app, use datetime.utcnow()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)