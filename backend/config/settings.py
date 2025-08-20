from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    title: str = "RSA Cryptography API"
    version: str = "1.0.0"
    description: str = "Educational RSA implementation with Miller-Rabin primality testing"
    
    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Security Limits
    max_prime_bit_length: int = 2048
    max_miller_rabin_rounds: int = 100
    min_prime_bit_length: int = 256
    min_miller_rabin_rounds: int = 1
    
    # Performance Settings
    prime_generation_timeout: int = 300  # seconds
    max_concurrent_operations: int = 10
    
    # Development
    debug: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
