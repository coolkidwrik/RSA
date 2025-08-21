import pytest

from core.rsa_crypto import RSACrypto
from models.crypto_models import PrimePair


class TestRSACrypto:
    """Test cases for RSA cryptographic operations"""

    @pytest.fixture
    def sample_prime_pair(self):
        """Create a sample prime pair for testing"""
        return PrimePair(p=61, q=53, bit_length=8, generation_time=0.001, miller_rabin_rounds=10)

    @pytest.fixture
    def rsa_crypto(self, sample_prime_pair):
        """Create RSA crypto instance with sample keypair"""
        crypto = RSACrypto()
        keypair = crypto.generate_keypair(sample_prime_pair)
        return crypto, keypair

    def test_keypair_generation(self, sample_prime_pair):
        """Test RSA keypair generation"""
        crypto = RSACrypto()
        keypair = crypto.generate_keypair(sample_prime_pair)

        # Verify key components
        assert keypair.n == 61 * 53  # 3233
        assert keypair.phi_n == 60 * 52  # 3120
        assert keypair.p == 61
        assert keypair.q == 53

        # Verify public and private keys
        assert keypair.e > 1
        assert keypair.d > 1
        assert (keypair.e * keypair.d) % keypair.phi_n == 1

    def test_key_validation(self, rsa_crypto):
        """Test RSA key validation"""
        crypto, keypair = rsa_crypto

        # Keypair should be valid
        assert keypair.validate_key_pair(), "Generated keypair should be valid"

    def test_text_to_blocks_conversion(self, rsa_crypto):
        """Test text to blocks conversion"""
        crypto, keypair = rsa_crypto

        test_message = "Hello"
        blocks = crypto._text_to_blocks(test_message, keypair.n)

        # Should produce at least one block
        assert len(blocks) > 0, "Should produce at least one block"

        # All blocks should be smaller than n
        for block in blocks:
            assert block < keypair.n, f"Block {block} should be smaller than n={keypair.n}"

    def test_blocks_to_text_conversion(self, rsa_crypto):
        """Test blocks to text conversion"""
        crypto, keypair = rsa_crypto

        test_message = "Hello RSA!"

        # Convert to blocks and back
        blocks = crypto._text_to_blocks(test_message, keypair.n)
        recovered_message = crypto._blocks_to_text(blocks)

        assert recovered_message == test_message, "Message should be recovered exactly"

    def test_encryption_decryption_cycle(self, rsa_crypto):
        """Test complete encryption and decryption cycle"""
        crypto, keypair = rsa_crypto

        test_message = "Test message for RSA!"

        # Encrypt
        encryption_result = crypto.encrypt_message(test_message, keypair.n, keypair.e)
        assert encryption_result.success, "Encryption should succeed"
        assert len(encryption_result.blocks) > 0, "Should produce encrypted blocks"

        # Extract encrypted values
        encrypted_blocks = [block.encrypted_value for block in encryption_result.blocks]

        # Decrypt
        decryption_result = crypto.decrypt_message(encrypted_blocks, keypair.n, keypair.d)
        assert decryption_result.success, "Decryption should succeed"
        assert decryption_result.message == test_message, "Should recover original message"

    def test_empty_message(self, rsa_crypto):
        """Test handling of edge cases"""
        crypto, keypair = rsa_crypto

        # Test with single character
        result = crypto.encrypt_message("A", keypair.n, keypair.e)
        assert result.success, "Should handle single character"

        encrypted_blocks = [block.encrypted_value for block in result.blocks]
        decrypt_result = crypto.decrypt_message(encrypted_blocks, keypair.n, keypair.d)
        assert decrypt_result.message == "A", "Should recover single character"
