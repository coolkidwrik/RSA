from fastapi import APIRouter, HTTPException, Depends
import asyncio

from models.schemas import PrimeGenerationRequest, PrimeGenerationResponse
from core.prime_generator import PrimeGenerator
from api.dependencies import get_prime_generator, get_app_state, AppState

router = APIRouter(prefix="/primes", tags=["Prime Generation"])

@router.post("/generate", response_model=PrimeGenerationResponse)
async def generate_primes(
    request: PrimeGenerationRequest,
    prime_generator: PrimeGenerator = Depends(get_prime_generator),
    state: AppState = Depends(get_app_state)
):
    """
    Generate a pair of large prime numbers using Miller-Rabin primality test.
    
    The generated primes are stored in the application state for subsequent
    key generation operations.
    """
    try:
        # Run prime generation in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        prime_pair = await loop.run_in_executor(
            None,
            prime_generator.generate_prime_pair,
            request.bit_length,
            request.miller_rabin_rounds
        )
        
        # Store primes in application state
        state.current_primes = prime_pair
        
        # Clear any existing keypair since we have new primes
        state.current_keypair = None
        
        return PrimeGenerationResponse(
            p=str(prime_pair.p),
            q=str(prime_pair.q),
            generation_time=prime_pair.generation_time,
            bit_length=prime_pair.bit_length,
            miller_rabin_rounds=prime_pair.miller_rabin_rounds
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prime generation failed: {str(e)}"
        )

@router.get("/current")
async def get_current_primes(state: AppState = Depends(get_app_state)):
    """Get currently stored prime pair information (without revealing the primes)"""
    if state.current_primes is None:
        return {"status": "no_primes", "message": "No primes generated"}
    
    return {
        "status": "primes_available",
        "bit_length": state.current_primes.bit_length,
        "generation_time": state.current_primes.generation_time,
        "miller_rabin_rounds": state.current_primes.miller_rabin_rounds,
        "p_bit_length": state.current_primes.p.bit_length(),
        "q_bit_length": state.current_primes.q.bit_length(),
    }

@router.delete("/clear")
async def clear_primes(state: AppState = Depends(get_app_state)):
    """Clear stored primes and associated keypairs"""
    state.clear_state()
    return {"message": "Primes and keypairs cleared"}