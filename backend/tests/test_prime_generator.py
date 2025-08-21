import time

import pytest

from core.miller_rabin import MillerRabinTester
from core.prime_generator import PrimeGenerator


class TestPrimeGenerator:
    """Test cases for prime number generator"""

    def test_generate_small_primes(self):
        """Test generation of small primes"""
        generator = PrimeGenerator()
        tester = MillerRabinTester()

        # Generate small primes for faster testing
        prime_pair = generator.generate_prime_pair(bit_length=64, rounds=10)

        # Verify both are prime
        assert tester.test(prime_pair.p, k=20), "Generated p should be prime"
        assert tester.test(prime_pair.q, k=20), "Generated q should be prime"

        # Verify they are different
        assert prime_pair.p != prime_pair.q, "Generated primes should be different"

        # Verify bit length is approximately correct
        assert (
            prime_pair.p.bit_length() >= 63
        ), "Prime p should have approximately correct bit length"
        assert (
            prime_pair.q.bit_length() >= 63
        ), "Prime q should have approximately correct bit length"

    def test_prime_pair_properties(self):
        """Test properties of generated prime pair"""
        generator = PrimeGenerator()
        prime_pair = generator.generate_prime_pair(bit_length=128, rounds=10)

        # Test PrimePair methods
        n = prime_pair.n
        phi_n = prime_pair.phi_n

        assert n == prime_pair.p * prime_pair.q, "n should equal p * q"
        assert phi_n == (prime_pair.p - 1) * (prime_pair.q - 1), "φ(n) should equal (p-1)(q-1)"

        # Verify generation time is recorded
        assert prime_pair.generation_time > 0, "Generation time should be positive"

    def test_different_bit_lengths(self):
        """Test prime generation with different bit lengths"""
        generator = PrimeGenerator()
        bit_lengths = [64, 128, 256]

        for bit_length in bit_lengths:
            prime_pair = generator.generate_prime_pair(bit_length=bit_length, rounds=5)

            # Check that primes have approximately correct bit length
            assert prime_pair.p.bit_length() >= bit_length - 1
            assert prime_pair.q.bit_length() >= bit_length - 1
            assert prime_pair.p.bit_length() <= bit_length + 1
            assert prime_pair.q.bit_length() <= bit_length + 1
