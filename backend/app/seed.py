"""Utility helpers for seeding the local SQLite database."""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from .repository import ListingRepository


def parse_args() -> ArgumentParser:
    parser = ArgumentParser(description="Seed the listings database from a fixture")
    parser.add_argument(
        "--database",
        type=Path,
        default=None,
        help="Path to the SQLite database file to (re)populate.",
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=None,
        help="Path to the JSON fixture containing listing data.",
    )
    return parser


def main() -> int:
    parser = parse_args()
    args = parser.parse_args()

    repository = ListingRepository(
        database_path=args.database,
        seed_path=args.fixture,
        auto_seed=False,
    )

    inserted = repository.reset_with_fixture()
    print(f"Seeded {inserted} listings into {repository.database_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
