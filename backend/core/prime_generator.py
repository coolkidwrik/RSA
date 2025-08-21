import random
import time

from models.crypto_models import PrimePair

from .miller_rabin import MillerRabinTester


class PrimeGenerator:
    """Generator for large prime numbers using Miller-Rabin test"""

    def __init__(self, max_attempts: int = 10000):
        self.max_attempts = max_attempts
        self.miller_rabin = MillerRabinTester()

    def generate_prime_pair(self, bit_length: int, rounds: int = 10) -> PrimePair:
        """Generate a pair of distinct primes"""
        start_time = time.time()

        p = self._generate_single_prime(bit_length, rounds)

        # Ensure q is different from p
        q = self._generate_single_prime(bit_length, rounds)
        attempts = 0
        while q == p and attempts < 100:
            q = self._generate_single_prime(bit_length, rounds)
            attempts += 1

        if p == q:
            raise RuntimeError("Failed to generate distinct primes")

        generation_time = time.time() - start_time

        return PrimePair(
            p=p,
            q=q,
            bit_length=bit_length,
            generation_time=generation_time,
            miller_rabin_rounds=rounds,
        )

    def _generate_single_prime(self, bit_length: int, rounds: int) -> int:
        """Generate a single prime number"""
        min_val = 1 << (bit_length - 1)
        max_val = (1 << bit_length) - 1

        for attempt in range(self.max_attempts):
            candidate = random.randrange(min_val, max_val)

            # Ensure odd number
            if candidate % 2 == 0:
                candidate += 1

            # Skip obvious composites
            if self._quick_composite_check(candidate):
                continue

            if self.miller_rabin.test(candidate, rounds):
                return candidate

        raise RuntimeError(f"Failed to generate prime after {self.max_attempts} attempts")

    @staticmethod
    def _quick_composite_check(n: int) -> bool:
        """Quick check for small prime factors"""
        small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        return any(n % p == 0 for p in small_primes if p < n)
