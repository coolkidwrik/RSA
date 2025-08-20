from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PrimePair:
    """Represents a pair of generated primes"""
    p: int
    q: int
    bit_length: int
    generation_time: float
    miller_rabin_rounds: int
    
    def __post_init__(self):
        if self.p == self.q:
            raise ValueError("Primes p and q must be different")
    
    @property
    def n(self) -> int:
        """Calculate modulus n = p * q"""
        return self.p * self.q
    
    @property
    def phi_n(self) -> int:
        """Calculate Euler's totient φ(n) = (p-1)(q-1)"""
        return (self.p - 1) * (self.q - 1)

@dataclass
class RSAKeyPair:
    """Represents a complete RSA key pair"""
    n: int  # Modulus
    e: int  # Public exponent
    d: int  # Private exponent
    p: int  # First prime
    q: int  # Second prime
    phi_n: int  # Euler's totient
    
    @property
    def public_key(self) -> tuple:
        """Return public key as (n, e)"""
        return (self.n, self.e)
    
    @property
    def private_key(self) -> tuple:
        """Return private key as (n, d)"""
        return (self.n, self.d)
    
    def validate_key_pair(self) -> bool:
        """Validate that the key pair is mathematically correct"""
        try:
            # Test with a small message
            test_msg = 42
            if test_msg >= self.n:
                test_msg = 2
            
            encrypted = pow(test_msg, self.e, self.n)
            decrypted = pow(encrypted, self.d, self.n)
            
            return decrypted == test_msg
        except:
            return False

@dataclass
class MessageBlock:
    """Represents a message block for encryption/decryption"""
    block_number: int
    original_value: int
    encrypted_value: Optional[int] = None
    
    @property
    def original_hex(self) -> str:
        return hex(self.original_value)
    
    @property
    def encrypted_hex(self) -> str:
        if self.encrypted_value is None:
            return "N/A"
        return hex(self.encrypted_value)

@dataclass
class CryptoOperation:
    """Represents the result of a cryptographic operation"""
    success: bool
    message: str
    blocks: List[MessageBlock]
    operation_time: float
    error_message: Optional[str] = None