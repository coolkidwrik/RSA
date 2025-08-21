import pytest

from core.miller_rabin import MillerRabinTester


class TestMillerRabinTester:
    """Test cases for Miller-Rabin primality test"""

    def test_known_primes(self):
        """Test with known prime numbers"""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        tester = MillerRabinTester()

        for prime in primes:
            assert tester.test(prime, k=10), f"{prime} should be identified as prime"

    def test_known_composites(self):
        """Test with known composite numbers"""
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28]
        tester = MillerRabinTester()

        for composite in composites:
            assert not tester.test(
                composite, k=10
            ), f"{composite} should be identified as composite"

    def test_large_known_primes(self):
        """Test with larger known primes"""
        large_primes = [
            982451653,  # Known prime
            2147483647,  # Mersenne prime (2^31 - 1)
            1000000007,  # Common large prime used in programming
        ]
        tester = MillerRabinTester()

        for prime in large_primes:
            assert tester.test(prime, k=20), f"{prime} should be identified as prime"

    def test_edge_cases(self):
        """Test edge cases"""
        tester = MillerRabinTester()

        # Test small numbers
        assert not tester.test(0, k=10)
        assert not tester.test(1, k=10)
        assert tester.test(2, k=10)
        assert tester.test(3, k=10)
        assert not tester.test(4, k=10)

    def test_carmichael_numbers(self):
        """Test with Carmichael numbers (composite numbers that pass many primality tests)"""
        carmichael_numbers = [561, 1105, 1729, 2465, 2821]
        tester = MillerRabinTester()

        # Miller-Rabin should correctly identify these as composite
        for carmichael in carmichael_numbers:
            assert not tester.test(
                carmichael, k=20
            ), f"Carmichael number {carmichael} should be identified as composite"

    def test_error_probability_calculation(self):
        """Test error probability calculation"""
        tester = MillerRabinTester()

        assert tester.get_error_probability(1) == 0.25
        assert tester.get_error_probability(2) == 0.0625
        assert tester.get_error_probability(10) == (0.25) ** 10
