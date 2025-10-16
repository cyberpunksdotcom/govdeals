# GovDeals Opportunity Tracker Backend

This service exposes a REST API for aggregating and serving GovDeals auction listings. The initial prototype reads from a fixture so the front-end can be developed in parallel, but the structure accommodates future scraper and database integrations.

## Features

- FastAPI application with typed schemas and automatic OpenAPI docs.
- CORS-enabled for local front-end development.
- Repository abstraction to swap the JSON fixture with scraper or database sources later.
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

4. **Verify the demo data**:

   ```bash
   curl http://127.0.0.1:8000/listings
   ```

5. **Run the automated tests**:

   ```bash
   pytest
   ```

## Next steps

- Replace the JSON repository with calls to the scraping pipeline.
- Persist listings in PostgreSQL with a SQLModel or SQLAlchemy implementation.
- Add authentication once user-specific watchlists are introduced.
