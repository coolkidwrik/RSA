from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator

from config.settings import settings


class PrimeGenerationRequest(BaseModel):
    bit_length: int = Field(
        default=512,
        ge=settings.min_prime_bit_length,
        le=settings.max_prime_bit_length,
        description="Bit length of primes to generate",
    )
    miller_rabin_rounds: int = Field(
        default=10,
        ge=settings.min_miller_rabin_rounds,
        le=settings.max_miller_rabin_rounds,
        description="Number of Miller-Rabin test rounds",
    )

    @validator("bit_length")
    def validate_bit_length(cls, v):
        if v % 8 != 0:
            raise ValueError("Bit length should be divisible by 8")
        return v


class PrimeGenerationResponse(BaseModel):
    p: str = Field(description="First generated prime")
    q: str = Field(description="Second generated prime")
    generation_time: float = Field(description="Time taken to generate primes in seconds")
    bit_length: int = Field(description="Actual bit length of generated primes")
    miller_rabin_rounds: int = Field(description="Number of Miller-Rabin rounds used")


class RSAParameters(BaseModel):
    n: str = Field(description="Modulus n = p * q")
    phi_n: str = Field(description="Euler's totient function φ(n)")
    e: str = Field(description="Public exponent")
    d: str = Field(description="Private exponent")


class PublicKey(BaseModel):
    n: str = Field(description="Modulus")
    e: str = Field(description="Public exponent")


class PrivateKey(BaseModel):
    n: str = Field(description="Modulus")
    d: str = Field(description="Private exponent")


class RSAKeysResponse(BaseModel):
    public_key: PublicKey
    private_key: PrivateKey
    parameters: RSAParameters


class EncryptionRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000, description="Message to encrypt")
    n: str = Field(description="RSA modulus")
    e: str = Field(description="RSA public exponent")

    @validator("n", "e")
    def validate_key_components(cls, v):
        try:
            int(v)
            return v
        except ValueError:
            raise ValueError("Key components must be valid integers")


class BlockInfo(BaseModel):
    block_number: int
    original_value: str
    encrypted_value: str
    original_hex: str
    encrypted_hex: str


class EncryptionResponse(BaseModel):
    encrypted_blocks: List[str]
    block_info: List[BlockInfo]
    total_blocks: int
    message_length: int


class DecryptionRequest(BaseModel):
    encrypted_blocks: List[str] = Field(min_items=1, description="List of encrypted blocks")
    n: str = Field(description="RSA modulus")
    d: str = Field(description="RSA private exponent")

    @validator("encrypted_blocks")
    def validate_encrypted_blocks(cls, v):
        for block in v:
            try:
                int(block)
            except ValueError:
                raise ValueError("All encrypted blocks must be valid integers")
        return v


class DecryptionResponse(BaseModel):
    decrypted_message: str
    success: bool
    block_count: int


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    primes_available: bool
    keys_generated: bool
    system_info: Dict[str, str]


class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: str
