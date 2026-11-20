"""
System API routes for health and model status
"""

import time
import logging
from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.core.model_manager import model_manager
from app.models.schemas import SystemStatusResponse, ModelsStatus, ModelComponentStatus

router = APIRouter()
logger = logging.getLogger("research_rover")


@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status(settings: Settings = Depends(get_settings)):
    """
    Real-time system health and model readiness check.
    Returns API connectivity state and actual model initialization states.
    Never triggers expensive model loads inside this endpoint.
    """
    models_info = model_manager.get_models_status()

    components = {}
    for key, comp in models_info.get("components", {}).items():
        components[key] = ModelComponentStatus(**comp)

    models_status = ModelsStatus(
        status=models_info.get("status", "not_loaded"),
        components=components
    )

    return SystemStatusResponse(
        status="healthy",
        api="online",
        version=settings.VERSION,
        timestamp=time.time(),
        models=models_status,
        services={
            "api": "running",
            "models": models_status.status
        }
    )
