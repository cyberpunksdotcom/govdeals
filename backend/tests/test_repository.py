from __future__ import annotations

from datetime import datetime

from backend.app.models import ListingFilters
from backend.app.repository import ListingRepository


def test_get_listings_sorted_by_end_time() -> None:
    repo = ListingRepository()

    listings = repo.get_listings()

    end_times = [listing.end_time for listing in listings]
    assert end_times == sorted(end_times)


def test_search_filter_matches_multiple_fields() -> None:
    repo = ListingRepository()

    listings = repo.get_listings(ListingFilters(search="server"))

    assert len(listings) == 1
    assert listings[0].title == "Dell PowerEdge R740 Server"


def test_category_filter_is_case_insensitive() -> None:
    repo = ListingRepository()

    listings = repo.get_listings(ListingFilters(category="vehicles"))

    assert len(listings) == 1
    assert listings[0].category == "Vehicles"


def test_bid_range_filter_limits_results() -> None:
    repo = ListingRepository()

    listings = repo.get_listings(ListingFilters(min_bid=5000, max_bid=20000))

    assert {listing.listing_id for listing in listings} == {"5687420"}


def test_ending_range_filters_apply() -> None:
    repo = ListingRepository()
    before = datetime.fromisoformat("2024-05-12T20:30:00")
    after = datetime.fromisoformat("2024-05-10T14:00:00")

    listings = repo.get_listings(ListingFilters(ending_before=before, ending_after=after))

    assert len(listings) == 1
    assert listings[0].listing_id == "8745632"
