from typing import Optional

from fastapi import Depends, HTTPException

from core.prime_generator import PrimeGenerator
from core.rsa_crypto import RSACrypto
from models.crypto_models import PrimePair, RSAKeyPair


# Global state management (in production, use Redis or database)
class AppState:
    def __init__(self):
        self.current_primes: Optional[PrimePair] = None
        self.current_keypair: Optional[RSAKeyPair] = None
        self.prime_generator = PrimeGenerator()
        self.rsa_crypto = RSACrypto()

    def clear_state(self):
        self.current_primes = None
        self.current_keypair = None


app_state = AppState()


def get_prime_generator() -> PrimeGenerator:
    """Dependency to get prime generator instance"""
    return app_state.prime_generator


def get_rsa_crypto() -> RSACrypto:
    """Dependency to get RSA crypto instance"""
    return app_state.rsa_crypto


def get_app_state() -> AppState:
    """Dependency to get application state"""
    return app_state


def require_primes(state: AppState = Depends(get_app_state)) -> PrimePair:
    """Dependency that requires primes to be generated"""
    if state.current_primes is None:
        raise HTTPException(
            status_code=400,
            detail="No primes available. Generate primes first using /api/generate-primes",
        )
    return state.current_primes


def require_keypair(state: AppState = Depends(get_app_state)) -> RSAKeyPair:
    """Dependency that requires RSA keypair to be generated"""
    if state.current_keypair is None:
        raise HTTPException(
            status_code=400,
            detail="No RSA keypair available. Generate keys first using /api/generate-keys",
        )
    return state.current_keypair
