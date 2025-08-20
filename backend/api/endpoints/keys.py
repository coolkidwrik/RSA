from fastapi import APIRouter, HTTPException, Depends
import asyncio

from models.schemas import RSAKeysResponse, PublicKey, PrivateKey, RSAParameters
from models.crypto_models import PrimePair
from core.rsa_crypto import RSACrypto
from api.dependencies import require_primes, get_rsa_crypto, get_app_state, AppState

router = APIRouter(prefix="/keys", tags=["Key Generation"])

@router.post("/generate", response_model=RSAKeysResponse)
async def generate_keys(
    prime_pair: PrimePair = Depends(require_primes),
    rsa_crypto: RSACrypto = Depends(get_rsa_crypto),
    state: AppState = Depends(get_app_state)
):
    """
    Generate RSA public and private key pair from previously generated primes.
    
    Requires primes to be generated first using the /primes/generate endpoint.
    """
    try:
        # Generate keypair in thread pool
        loop = asyncio.get_event_loop()
        keypair = await loop.run_in_executor(
            None,
            rsa_crypto.generate_keypair,
            prime_pair
        )
        
        # Store keypair in application state
        state.current_keypair = keypair
        
        return RSAKeysResponse(
            public_key=PublicKey(n=str(keypair.n), e=str(keypair.e)),
            private_key=PrivateKey(n=str(keypair.n), d=str(keypair.d)),
            parameters=RSAParameters(
                n=str(keypair.n),
                phi_n=str(keypair.phi_n),
                e=str(keypair.e),
                d=str(keypair.d)
            )
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Key generation failed: {str(e)}"
        )

@router.get("/current")
async def get_current_keys(state: AppState = Depends(get_app_state)):
    """Get information about currently stored keys (without revealing private key)"""
    if state.current_keypair is None:
        return {"status": "no_keys", "message": "No keys generated"}
    
    keypair = state.current_keypair
    return {
        "status": "keys_available",
        "public_key": {
            "n": str(keypair.n),
            "e": str(keypair.e)
        },
        "key_info": {
            "n_bit_length": keypair.n.bit_length(),
            "is_valid": keypair.validate_key_pair()
        }
    }

@router.post("/validate")
async def validate_keys(state: AppState = Depends(get_app_state)):
    """Validate the current RSA keypair"""
    if state.current_keypair is None:
        raise HTTPException(status_code=400, detail="No keys available to validate")
    
    is_valid = state.current_keypair.validate_key_pair()
    
    return {
        "is_valid": is_valid,
        "message": "Keys are valid" if is_valid else "Keys failed validation"
    }