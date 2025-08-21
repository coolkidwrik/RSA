import time
from typing import List, Optional, Tuple

from models.crypto_models import CryptoOperation, MessageBlock, PrimePair, RSAKeyPair


class RSACrypto:
    """RSA cryptographic operations"""

    def __init__(self):
        self.current_keypair: Optional[RSAKeyPair] = None

    def generate_keypair(self, prime_pair: PrimePair) -> RSAKeyPair:
        """Generate RSA key pair from prime pair"""
        n = prime_pair.n
        phi_n = prime_pair.phi_n

        # Choose public exponent e
        e = 65537  # Common choice
        while self._gcd(e, phi_n) != 1:
            e += 2

        # Calculate private exponent d
        d = self._mod_inverse(e, phi_n)

        keypair = RSAKeyPair(n=n, e=e, d=d, p=prime_pair.p, q=prime_pair.q, phi_n=phi_n)

        # Validate the key pair
        if not keypair.validate_key_pair():
            raise ValueError("Generated key pair failed validation")

        self.current_keypair = keypair
        return keypair

    def encrypt_message(self, message: str, n: int, e: int) -> CryptoOperation:
        """Encrypt a message using RSA public key"""
        start_time = time.time()

        try:
            # Convert message to blocks
            blocks_data = self._text_to_blocks(message, n)
            message_blocks = []

            for i, block_value in enumerate(blocks_data):
                encrypted_value = pow(block_value, e, n)

                block = MessageBlock(
                    block_number=i + 1, original_value=block_value, encrypted_value=encrypted_value
                )
                message_blocks.append(block)

            operation_time = time.time() - start_time

            return CryptoOperation(
                success=True,
                message=f"Successfully encrypted {len(message_blocks)} blocks",
                blocks=message_blocks,
                operation_time=operation_time,
            )

        except Exception as e:
            operation_time = time.time() - start_time
            return CryptoOperation(
                success=False,
                message="Encryption failed",
                blocks=[],
                operation_time=operation_time,
                error_message=str(e),
            )

    def decrypt_message(self, encrypted_blocks: List[int], n: int, d: int) -> CryptoOperation:
        """Decrypt a message using RSA private key"""
        start_time = time.time()

        try:
            decrypted_blocks = []

            for i, encrypted_value in enumerate(encrypted_blocks):
                decrypted_value = pow(encrypted_value, d, n)

                block = MessageBlock(
                    block_number=i + 1,
                    original_value=decrypted_value,
                    encrypted_value=encrypted_value,
                )
                decrypted_blocks.append(block)

            # Convert blocks back to text
            block_values = [block.original_value for block in decrypted_blocks]
            decrypted_text = self._blocks_to_text(block_values)

            operation_time = time.time() - start_time

            return CryptoOperation(
                success=True,
                message=decrypted_text,
                blocks=decrypted_blocks,
                operation_time=operation_time,
            )

        except Exception as e:
            operation_time = time.time() - start_time
            return CryptoOperation(
                success=False,
                message="Decryption failed",
                blocks=[],
                operation_time=operation_time,
                error_message=str(e),
            )

    def _text_to_blocks(self, text: str, n: int) -> List[int]:
        """Convert text to integer blocks smaller than n"""
        n_bits = n.bit_length()
        block_size = max(1, (n_bits - 1) // 8)  # Safe block size in bytes

        blocks = []
        text_bytes = text.encode("utf-8")

        for i in range(0, len(text_bytes), block_size):
            chunk = text_bytes[i : i + block_size]
            block_value = int.from_bytes(chunk, byteorder="big")

            if block_value >= n:
                raise ValueError(f"Block too large for key size: {block_value} >= {n}")

            blocks.append(block_value)

        return blocks

    def _blocks_to_text(self, blocks: List[int]) -> str:
        """Convert integer blocks back to text"""
        result_bytes = b""

        for block in blocks:
            if block == 0:
                continue

            byte_length = (block.bit_length() + 7) // 8
            block_bytes = block.to_bytes(byte_length, byteorder="big")
            result_bytes += block_bytes

        return result_bytes.decode("utf-8")

    @staticmethod
    def _gcd(a: int, b: int) -> int:
        """Greatest Common Divisor using Euclidean algorithm"""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def _extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """Extended Euclidean Algorithm"""
        if a == 0:
            return b, 0, 1

        gcd, x1, y1 = RSACrypto._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1

        return gcd, x, y

    @staticmethod
    def _mod_inverse(a: int, m: int) -> int:
        """Modular multiplicative inverse using Extended Euclidean Algorithm"""
        gcd, x, _ = RSACrypto._extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m
