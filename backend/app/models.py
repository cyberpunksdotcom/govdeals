"""Domain models for GovDeals listing records."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Listing:
    """Represents a single auction listing."""

    listing_id: str
    title: str
    category: str
    current_bid: float
    currency: str
    end_time: datetime
    location: str
    seller: str
    url: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None


@dataclass(slots=True)
class ListingFilters:
    """Filtering options applied when retrieving listings."""

    search: Optional[str] = None
    category: Optional[str] = None
    min_bid: Optional[float] = None
    max_bid: Optional[float] = None
    ending_before: Optional[datetime] = None
    ending_after: Optional[datetime] = None

    def normalized_search(self) -> Optional[str]:
        """Return a trimmed lowercase search string for comparisons."""

        if self.search is None:
            return None
        normalized = self.search.strip().lower()
        return normalized or None

    def normalized_category(self) -> Optional[str]:
        """Return a lowercase category string for comparisons."""

        return self.category.lower() if self.category else None
