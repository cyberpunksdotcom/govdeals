from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    """Provide a FastAPI test client for API tests."""

    app = create_app()
    return TestClient(app)
