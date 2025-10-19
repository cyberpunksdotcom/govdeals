"""Data access utilities for listing data."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from .models import Listing, ListingFilters


SCHEMA_STATEMENT = """
CREATE TABLE IF NOT EXISTS listings (
    listing_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    current_bid REAL NOT NULL,
    currency TEXT NOT NULL,
    end_time TEXT NOT NULL,
    location TEXT NOT NULL,
    seller TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    thumbnail_url TEXT
);
"""


class ListingRepository:
    """Repository backed by a lightweight SQLite store."""

    def __init__(
        self,
        database_path: Path | None = None,
        *,
        seed_path: Path | None = None,
        auto_seed: bool = True,
    ) -> None:
        default_db = Path(__file__).parent / "data" / "listings.db"
        self._db_path = Path(database_path) if database_path is not None else default_db
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        default_seed = Path(__file__).parent / "sample_data" / "listings.json"
        self._seed_path = Path(seed_path) if seed_path is not None else default_seed
        self._auto_seed = auto_seed

        self._initialise_database()

    @property
    def database_path(self) -> Path:
        """Return the configured database path."""

        return self._db_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialise_database(self) -> None:
        with self._connect() as connection:
            connection.execute(SCHEMA_STATEMENT)
            if self._auto_seed:
                self._seed_if_required(connection)

    def _seed_if_required(self, connection: sqlite3.Connection) -> None:
        cursor = connection.execute("SELECT COUNT(*) FROM listings")
        count = cursor.fetchone()[0]
        if count == 0:
            self._seed_database(connection)

    def _seed_database(self, connection: sqlite3.Connection) -> int:
        if not self._seed_path.exists():
            return 0

        with self._seed_path.open("r", encoding="utf-8") as handle:
            payload: Iterable[dict[str, object]] = json.load(handle)

        records = [
            (
                item["listing_id"],
                item["title"],
                item["category"],
                float(item["current_bid"]),
                item.get("currency", "USD"),
                item["end_time"],
                item["location"],
                item["seller"],
                item["url"],
                item.get("description"),
                item.get("thumbnail_url"),
            )
            for item in payload
        ]

        connection.executemany(
            """
            INSERT OR REPLACE INTO listings (
                listing_id,
                title,
                category,
                current_bid,
                currency,
                end_time,
                location,
                seller,
                url,
                description,
                thumbnail_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            records,
        )
        connection.commit()
        return len(records)

    def reset_with_fixture(self) -> int:
        """Replace the database contents with the JSON fixture."""

        with self._connect() as connection:
            connection.execute("DELETE FROM listings")
            connection.commit()
            return self._seed_database(connection)

    def count_listings(self) -> int:
        """Return the total number of listings stored."""

        with self._connect() as connection:
            cursor = connection.execute("SELECT COUNT(*) FROM listings")
            return int(cursor.fetchone()[0])

    def get_listings(self, filters: ListingFilters | None = None) -> List[Listing]:
        """Return listings sorted by soonest end time with optional filtering."""

        query_parts = [
            "SELECT listing_id, title, category, current_bid, currency, end_time,",
            "       location, seller, url, description, thumbnail_url",
            "FROM listings",
            "WHERE 1=1",
        ]
        parameters: list[object] = []

        if filters is not None:
            normalized_search = filters.normalized_search()
            normalized_category = filters.normalized_category()

            if normalized_search is not None:
                query_parts.append(
                    "AND ("  # noqa: ISC003
                    "LOWER(title) LIKE ? OR "
                    "LOWER(COALESCE(description, '')) LIKE ? OR "
                    "LOWER(location) LIKE ?"
                    ")",
                )
                like = f"%{normalized_search}%"
                parameters.extend([like, like, like])

            if normalized_category is not None:
                query_parts.append("AND LOWER(category) = ?")
                parameters.append(normalized_category)

            if filters.min_bid is not None:
                query_parts.append("AND current_bid >= ?")
                parameters.append(filters.min_bid)

            if filters.max_bid is not None:
                query_parts.append("AND current_bid <= ?")
                parameters.append(filters.max_bid)

            if filters.ending_before is not None:
                query_parts.append("AND end_time < ?")
                parameters.append(filters.ending_before.isoformat())

            if filters.ending_after is not None:
                query_parts.append("AND end_time > ?")
                parameters.append(filters.ending_after.isoformat())

        query_parts.append("ORDER BY end_time ASC")
        query = "\n".join(query_parts)

        with self._connect() as connection:
            cursor = connection.execute(query, parameters)
            rows = cursor.fetchall()

        return [
            Listing(
                listing_id=row["listing_id"],
                title=row["title"],
                category=row["category"],
                current_bid=float(row["current_bid"]),
                currency=row["currency"],
                end_time=datetime.fromisoformat(row["end_time"]),
                location=row["location"],
                seller=row["seller"],
                url=row["url"],
                description=row["description"],
                thumbnail_url=row["thumbnail_url"],
            )
            for row in rows
        ]
