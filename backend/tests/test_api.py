import pytest
from fastapi.testclient import TestClient


class TestAPI:
    """Test cases for API endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_api_root_endpoint(self, client):
        """Test API root endpoint"""
        response = client.get("/api/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/api/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "primes_available" in data
        assert "keys_generated" in data

    def test_readiness_check(self, client):
        """Test readiness check endpoint"""
        response = client.get("/api/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    def test_liveness_check(self, client):
        """Test liveness check endpoint"""
        response = client.get("/api/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"

    def test_prime_generation_endpoint(self, client):
        """Test prime generation endpoint"""
        response = client.post(
            "/api/primes/generate", json={"bit_length": 256, "miller_rabin_rounds": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert "p" in data
        assert "q" in data
        assert "generation_time" in data
        assert data["bit_length"] == 256

    def test_key_generation_without_primes(self, client):
        """Test key generation without primes should fail"""
        response = client.post("/api/keys/generate")
        assert response.status_code == 400
        assert "No primes available" in response.json()["detail"]

    def test_complete_workflow(self, client):
        """Test complete RSA workflow"""
        # Step 1: Generate primes
        prime_response = client.post(
            "/api/primes/generate", json={"bit_length": 256, "miller_rabin_rounds": 5}
        )
        assert prime_response.status_code == 200

        # Step 2: Generate keys
        key_response = client.post("/api/keys/generate")
        assert key_response.status_code == 200
        key_data = key_response.json()

        # Step 3: Encrypt message
        encrypt_response = client.post(
            "/api/crypto/encrypt",
            json={
                "message": "Hello API!",
                "n": key_data["public_key"]["n"],
                "e": key_data["public_key"]["e"],
            },
        )
        assert encrypt_response.status_code == 200
        encrypt_data = encrypt_response.json()

        # Step 4: Decrypt message
        decrypt_response = client.post(
            "/api/crypto/decrypt",
            json={
                "encrypted_blocks": encrypt_data["encrypted_blocks"],
                "n": key_data["private_key"]["n"],
                "d": key_data["private_key"]["d"],
            },
        )
        assert decrypt_response.status_code == 200
        decrypt_data = decrypt_response.json()
        assert decrypt_data["decrypted_message"] == "Hello API!"
        assert decrypt_data["success"] is True

    def test_encryption_with_invalid_keys(self, client):
        """Test encryption with invalid keys"""
        response = client.post(
            "/api/crypto/encrypt", json={"message": "test", "n": "invalid", "e": "invalid"}
        )
        assert response.status_code == 400

    def test_current_primes_without_generation(self, client):
        """Test getting current primes when none are generated"""
        response = client.get("/api/primes/current")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "no_primes"

    def test_current_keys_without_generation(self, client):
        """Test getting current keys when none are generated"""
        response = client.get("/api/keys/current")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "no_keys"
