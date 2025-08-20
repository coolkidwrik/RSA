from fastapi import APIRouter
from api.endpoints import primes, keys, crypto, health

# Create main API router
api_router = APIRouter(prefix="/api")

# Include all endpoint routers
api_router.include_router(primes.router)
api_router.include_router(keys.router)
api_router.include_router(crypto.router)
api_router.include_router(health.router)

# Root endpoint
@api_router.get("/")
async def api_root():
    """API root endpoint with basic information"""
    return {
        "message": "RSA Cryptography API",
        "version": "1.0.0",
        "endpoints": {
            "primes": "/api/primes/*",
            "keys": "/api/keys/*",
            "crypto": "/api/crypto/*",
            "health": "/api/health/*"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }