"""Pydantic schemas exposed by the FastAPI service."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ListingSchema(BaseModel):
    """Serialises listing data for API responses."""

    listing_id: str = Field(..., description="Unique identifier for the listing")
    title: str
    category: str
    current_bid: float = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=3)
    end_time: datetime
    location: str
    seller: str
    url: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = Field(None, alias="thumbnailUrl")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "listing_id": "123456",
                "title": "2016 Ford F-150",
                "category": "Vehicles",
                "current_bid": 4500.0,
                "currency": "USD",
                "end_time": "2024-05-21T22:15:00Z",
                "location": "Atlanta, GA",
                "seller": "City of Atlanta",
                "url": "https://www.govdeals.com/index.cfm?fa=Main.Item&itemid=123&acctid=456",
                "description": "Well-maintained fleet vehicle with 85k miles.",
                "thumbnailUrl": "https://images.govdeals.com/thumbnail/123456.jpg",
            }
        }
