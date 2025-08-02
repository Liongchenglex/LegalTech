"""
FastAPI main application module for LegalTech MVP.

This module sets up the FastAPI application with middleware, CORS,
and API routing for the legal technology platform.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import os
from typing import Dict, Any

from app.core.config import settings
from app.api import health, auth

# Create FastAPI application instance
app = FastAPI(
    title="LegalTech MVP API",
    description="A scalable Legal Technology platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Dict[str, Any]:
    """
    Root endpoint providing API information.
    
    Returns basic API metadata and status information.
    Useful for API discovery and health monitoring.
    
    Returns:
        Dict containing API metadata, version, and timestamp
    """
    return {
        "message": "LegalTech MVP API",
        "version": "1.0.0",
        "description": "A scalable Legal Technology platform",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs"
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring and load balancers.
    
    Provides system health status, environment info, and basic metrics.
    Used by CI/CD pipelines and monitoring systems.
    
    Returns:
        Dict containing health status, environment, and system info
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        "api_version": "1.0.0"
    }


@app.get("/api")
async def api_info() -> Dict[str, Any]:
    """
    API information endpoint.
    
    Provides detailed API information for frontend integration.
    Used by frontend to verify backend connectivity and version.
    
    Returns:
        Dict containing API details and available endpoints
    """
    return {
        "message": "LegalTech MVP API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "auth": "/api/auth",
        }
    }


# Include API routers
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Custom 404 handler for unmatched routes.
    
    Provides consistent error response format for missing endpoints.
    
    Args:
        request: The HTTP request object
        exc: The exception that was raised
        
    Returns:
        JSONResponse with 404 status and error details
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Route not found",
            "path": str(request.url.path),
            "method": request.method,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Global exception handler for internal server errors.
    
    Provides consistent error response format and logging.
    Hides sensitive error details in production.
    
    Args:
        request: The HTTP request object
        exc: The exception that was raised
        
    Returns:
        JSONResponse with 500 status and error details
    """
    error_detail = str(exc) if settings.ENVIRONMENT == "development" else "Internal server error"
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": error_detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )