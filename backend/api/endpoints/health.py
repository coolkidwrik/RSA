from datetime import datetime, UTC

from fastapi import APIRouter, Depends

from api.dependencies import AppState, get_app_state
from config.settings import settings
from core.utils import get_system_info
from models.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["Health Check"])


@router.get("/", response_model=HealthResponse)
async def health_check(state: AppState = Depends(get_app_state)):
    """
    Comprehensive health check endpoint.

    Returns system status, resource usage, and application state.
    """
    system_info = get_system_info()

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(UTC).isoformat(),
        primes_available=state.current_primes is not None,
        keys_generated=state.current_keypair is not None,
        system_info=system_info,
    )


@router.get("/ready")
async def readiness_check(state: AppState = Depends(get_app_state)):
    """
    Readiness probe for container orchestration.

    Returns 200 if the service is ready to accept requests.
    """
    return {
        "status": "ready",
        "timestamp": datetime.now(UTC).isoformat(),
        "components": {
            "prime_generator": "available",
            "rsa_crypto": "available",
            "current_state": {
                "primes": "available" if state.current_primes else "not_generated",
                "keys": "available" if state.current_keypair else "not_generated",
            },
        },
    }


@router.get("/live")
async def liveness_check():
    """
    Liveness probe for container orchestration.

    Returns 200 if the service is alive and responding.
    """
    return {
        "status": "alive",
        "timestamp": datetime.now(UTC).isoformat(),
        "version": settings.version,
    }
