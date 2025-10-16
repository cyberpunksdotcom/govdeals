# GovDeals Opportunity Tracker Backend

This service exposes a REST API for aggregating and serving GovDeals auction listings. The prototype now persists data in a lightweight SQLite database so the dashboard experiences stable identifiers and consistent filtering while the scraping pipeline is developed.

## Features

- FastAPI application with typed schemas and automatic OpenAPI docs.
- CORS-enabled for local front-end development.
- Repository abstraction backed by SQLite so local runs survive restarts while still allowing the source to be swapped for scraper output or PostgreSQL later.
- Listings endpoint supports keyword, category, bid range, and closing window filters used by the dashboard.

## Local quickstart

1. **Create a virtual environment**:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   For local development and testing you can install the optional tooling bundle:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run the API**:

   ```bash
   uvicorn app.main:app --reload
   ```

   The service will start on `http://127.0.0.1:8000`. Interactive docs are available at `/docs`.

4. **(Optional) Re-seed the local database**:

   ```bash
   python -m app.seed
   ```

   The command wipes the SQLite file in `app/data/` and reloads the bundled fixture. Custom paths can be passed with `--database` and `--fixture`.

5. **Verify the demo data**:

   ```bash
   curl http://127.0.0.1:8000/listings
   ```

6. **Run the automated tests**:

   ```bash
   pytest
   ```

## Next steps

- Connect the repository seeding to the scraping pipeline output.
- Migrate from SQLite to PostgreSQL with SQLModel or SQLAlchemy once infrastructure is ready.
- Add authentication once user-specific watchlists are introduced.
