"""
Main application factory for the FastAPI Template Service
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .config.settings import settings
from .auth.api_key import api_key_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


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


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.service_name,
        description="A service for generating FastAPI project templates",
        version="1.0.0",
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(router)
    
    return app


# Create the main app instance
app = create_app()


# For backward compatibility
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "services.template_service.main:app",
        host=settings.service_host,
        port=settings.service_port,
        reload=settings.debug_mode
    )


