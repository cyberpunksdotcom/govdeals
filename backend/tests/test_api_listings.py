from __future__ import annotations

from datetime import datetime

from fastapi.testclient import TestClient


def test_listings_endpoint_returns_all_results(client: TestClient) -> None:
    response = client.get("/listings")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 3


def test_listings_endpoint_applies_filters(client: TestClient) -> None:
    response = client.get("/listings", params={"category": "Heavy Equipment", "min_bid": 18000})

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["listing_id"] == "5687420"


def test_listings_endpoint_validates_bid_range(client: TestClient) -> None:
    response = client.get("/listings", params={"min_bid": 1000, "max_bid": 500})

    assert response.status_code == 400
    assert response.json()["detail"] == "min_bid must be less than or equal to max_bid"


def test_listings_endpoint_supports_ending_filters(client: TestClient) -> None:
    params = {
        "ending_before": datetime.fromisoformat("2024-05-12T20:30:00").isoformat(),
        "ending_after": datetime.fromisoformat("2024-05-10T14:00:00").isoformat(),
    }

    response = client.get("/listings", params=params)

    assert response.status_code == 200
    payload = response.json()
    assert [item["listing_id"] for item in payload] == ["8745632"]
