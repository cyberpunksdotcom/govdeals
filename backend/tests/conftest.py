from __future__ import annotations

import pytest
from pathlib import Path
from typing import Generator

from fastapi.testclient import TestClient

from backend.app.api.listings import get_repository
from backend.app.main import create_app
from backend.app.repository import ListingRepository


@pytest.fixture()
def repository(tmp_path: Path) -> ListingRepository:
    """Create a temporary repository backed by SQLite."""

    db_path = tmp_path / "listings.db"
    return ListingRepository(database_path=db_path)


@pytest.fixture()
def client(repository: ListingRepository) -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client for API tests."""

    app = create_app()
    app.dependency_overrides[get_repository] = lambda: repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
