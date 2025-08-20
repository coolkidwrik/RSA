import random

class MillerRabinTester:
    """Implementation of the Miller-Rabin primality test"""
    
    @staticmethod
    def test(n: int, k: int = 10) -> bool:
        """
        Miller-Rabin primality test
        
        Args:
            n: Number to test for primality
            k: Number of rounds (higher = more accurate)
            
        Returns:
            True if n is probably prime, False if n is composite
        """
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 as d * 2^r
        r = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            r += 1
        
        # Perform k rounds of testing
        for _ in range(k):
            if not MillerRabinTester._single_test(n, d, r):
                return False
        
        return True
    
    @staticmethod
    def _single_test(n: int, d: int, r: int) -> bool:
        """Perform a single round of Miller-Rabin test"""
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            return True
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        
        return False
    
    @staticmethod
    def get_error_probability(rounds: int) -> float:
        """Calculate the error probability for given number of rounds"""
        return (0.25) ** rounds