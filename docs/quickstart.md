# Quickstart

Follow this guide to spin up the GovDeals opportunity tracker prototype on your machine. The stack uses a FastAPI backend and a static front-end so you can validate flows before wiring in the full scraping pipeline.

## Prerequisites

- Python 3.11+
- Node.js 18+ (optional, only if you prefer a Node-based static server)

## 1. Clone the repository

```bash
git clone https://github.com/your-org/govdeals-tracker.git
cd govdeals-tracker
```

## 2. Start the backend API

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
# Optional but recommended for local testing
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

The API listens on `http://127.0.0.1:8000`. Visit `/docs` for interactive OpenAPI endpoints.

Once the server is running you can execute the automated checks:

```bash
pytest
```

## 3. Launch the front-end dashboard

Open a new terminal window:

```bash
cd frontend
python -m http.server 5173
```

Now browse to `http://127.0.0.1:5173`. You should see the dashboard populated with demo listings provided by the backend fixture. If the API is offline the UI automatically falls back to `frontend/sample-data/listings.json` and displays a notice.

## 4. Explore the workflow

- Use the keyword search to narrow results by title, description, or location. The same search is available via the API `search` query parameter.
- Combine category, minimum/maximum bid, and closing window controls to mirror server-side filters. The UI sends the active filters directly to the API and falls back to local filtering if the backend is offline.
- Click “View on GovDeals” to inspect the source listing in a new tab.

## 5. Next steps

- Swap the fixture repository (`backend/app/repository.py`) with the scraper pipeline output.
- Deploy both services behind a reverse proxy or container stack (Docker Compose is recommended for repeatability).
- Extend the front-end with authentication, saved filters, and alert configuration as the backend surface expands.
