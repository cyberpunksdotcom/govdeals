"""Data access utilities for listing data."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from .models import Listing, ListingFilters


class ListingRepository:
    """Simple repository reading listing data from a JSON fixture."""

    def __init__(self, data_path: Path | None = None) -> None:
        default_path = Path(__file__).parent / "sample_data" / "listings.json"
        self._data_path = data_path or default_path

    def get_listings(self, filters: ListingFilters | None = None) -> List[Listing]:
        """Return all listings sorted by soonest end time with optional filtering."""

        import json

        with self._data_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)

        records: Iterable[Listing] = (
            Listing(
                listing_id=item["listing_id"],
                title=item["title"],
                category=item["category"],
                current_bid=float(item["current_bid"]),
                currency=item.get("currency", "USD"),
                end_time=datetime.fromisoformat(item["end_time"]),
                location=item["location"],
                seller=item["seller"],
                url=item["url"],
                description=item.get("description"),
                thumbnail_url=item.get("thumbnail_url"),
            )
            for item in payload
        )

        if filters is None:
            return sorted(records, key=lambda listing: listing.end_time)

        normalized_search = filters.normalized_search()
        normalized_category = filters.normalized_category()

        def matches_filters(listing: Listing) -> bool:
            if normalized_search is not None:
                haystacks = filter(
                    None,
                    (
                        listing.title,
                        listing.description,
                        listing.location,
                    ),
                )
                if not any(normalized_search in value.lower() for value in haystacks):
                    return False

            if normalized_category is not None:
                if listing.category.lower() != normalized_category:
                    return False

            if filters.min_bid is not None and listing.current_bid < filters.min_bid:
                return False

            if filters.max_bid is not None and listing.current_bid > filters.max_bid:
                return False

            if filters.ending_before is not None and listing.end_time >= filters.ending_before:
                return False

            if filters.ending_after is not None and listing.end_time <= filters.ending_after:
                return False

            return True

        filtered_records = filter(matches_filters, records)
        return sorted(filtered_records, key=lambda listing: listing.end_time)
