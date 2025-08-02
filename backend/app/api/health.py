"""
Health check API endpoints.

Provides system health monitoring endpoints for load balancers,
monitoring systems, and CI/CD pipelines.
"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any
import psutil
import os

router = APIRouter()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint.
    
    Returns simple health status for quick monitoring.
    Used by load balancers and uptime monitoring.
    
    Returns:
        Dict with basic health status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with system metrics.
    
    Provides comprehensive system information including:
    - Memory usage
    - CPU usage
    - Disk space
    - Process information
    
    Used for monitoring dashboards and debugging.
    
    Returns:
        Dict with detailed system health metrics
    """
    try:
        # Get system metrics
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu_percent = psutil.cpu_percent(interval=1)
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                },
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "process": {
                    "pid": os.getpid(),
                    "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
                }
            }
        }
    except Exception as e:
        return {
            "status": "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "error": f"Health check failed: {str(e)}"
        }