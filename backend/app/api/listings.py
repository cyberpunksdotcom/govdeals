"""Listing endpoints."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from ..models import ListingFilters
from ..repository import ListingRepository
from ..schemas import ListingSchema

router = APIRouter(prefix="/listings", tags=["listings"])


def get_repository() -> ListingRepository:
    """Dependency providing the listing repository."""

    return ListingRepository()


@router.get("", response_model=list[ListingSchema])
def list_listings(
    repo: ListingRepository = Depends(get_repository),
    search: str | None = Query(
        default=None,
        description="Full-text search across title, description, and location.",
        min_length=1,
    ),
    category: str | None = Query(
        default=None,
        description="Restrict listings to an exact category match.",
        min_length=1,
    ),
    min_bid: float | None = Query(
        default=None,
        ge=0,
        description="Return listings with a current bid greater than or equal to this value.",
    ),
    max_bid: float | None = Query(
        default=None,
        ge=0,
        description="Return listings with a current bid less than or equal to this value.",
    ),
    ending_before: datetime | None = Query(
        default=None,
        description="Return listings closing before this timestamp.",
    ),
    ending_after: datetime | None = Query(
        default=None,
        description="Return listings closing after this timestamp.",
    ),
) -> list[ListingSchema]:
    """Return all tracked listings for the dashboard."""

    if min_bid is not None and max_bid is not None and min_bid > max_bid:
        raise HTTPException(
            status_code=400,
            detail="min_bid must be less than or equal to max_bid",
        )

    filters = ListingFilters(
        search=search,
        category=category,
        min_bid=min_bid,
        max_bid=max_bid,
        ending_before=ending_before,
        ending_after=ending_after,
    )

    listings = repo.get_listings(filters=filters)
    return [ListingSchema.model_validate(listing) for listing in listings]
