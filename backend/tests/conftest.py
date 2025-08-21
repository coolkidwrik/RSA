import asyncio

import pytest
from fastapi.testclient import TestClient

from api.dependencies import app_state
from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_app_state():
    """Reset application state before each test."""
    app_state.clear_state()
    yield
    app_state.clear_state()


@pytest.fixture
def sample_primes():
    """Sample small primes for testing."""
    return {"p": 61, "q": 53, "n": 3233, "phi_n": 3120, "e": 17, "d": 2753}
