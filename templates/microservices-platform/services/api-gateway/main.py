"""
{{PROJECT_NAME}} API Gateway
Main routing and orchestration service following your architecture patterns
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
from datetime import datetime

app = FastAPI(
    title="{{PROJECT_NAME}} API Gateway",
    description="Main API routing and orchestration service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
SERVICE_NAME = os.getenv("SERVICE_NAME", "{{PROJECT_NAME}}-api-gateway")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to {{PROJECT_NAME}} API Gateway!",
        "service": SERVICE_NAME,
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "auth": "/api/v1/auth",
            "users": "/api/v1/users"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    # Check downstream services
    services_status = {}
    
    try:
        async with httpx.AsyncClient() as client:
            # Check auth service
            auth_response = await client.get(f"{AUTH_SERVICE_URL}/health", timeout=5.0)
            services_status["auth-service"] = {
                "status": "healthy" if auth_response.status_code == 200 else "unhealthy",
                "response_time_ms": auth_response.elapsed.total_seconds() * 1000
            }
    except Exception as e:
        services_status["auth-service"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Determine overall health
    all_healthy = all(service.get("status") == "healthy" for service in services_status.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "service": SERVICE_NAME,
        "timestamp": datetime.utcnow().isoformat(),
        "services": services_status,
        "uptime": "running"  # You can implement actual uptime tracking
    }

# Auth proxy endpoints
@app.post("/api/v1/auth/login")
async def login_proxy(credentials: dict):
    """Proxy login requests to auth service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/auth/login",
                json=credentials,
                timeout=10.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Auth service unavailable: {str(e)}"
        )

@app.post("/api/v1/auth/register")
async def register_proxy(user_data: dict):
    """Proxy registration requests to auth service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/auth/register",
                json=user_data,
                timeout=10.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Auth service unavailable: {str(e)}"
        )

@app.get("/api/v1/users/me")
async def get_current_user_proxy():
    """Proxy user info requests to auth service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/v1/users/me",
                timeout=10.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Auth service unavailable: {str(e)}"
        )

# Example business logic endpoints
@app.get("/api/v1/status")
async def system_status():
    """System-wide status endpoint"""
    return {
        "platform": "{{PROJECT_NAME}}",
        "gateway": SERVICE_NAME,
        "timestamp": datetime.utcnow().isoformat(),
        "services_count": len([AUTH_SERVICE_URL]),  # Add more services as needed
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)