# GovDeals Opportunity Tracker Frontend

The front-end is a lightweight static dashboard that consumes the FastAPI backend. It can be served via any static file host during early prototyping or embedded into a richer SPA later.

## Features

- Responsive card grid that highlights key listing attributes (bid, end time, location).
- Keyword, category, bid range, and closing-window filters that call the FastAPI endpoint when available and fall back to local filtering when offline.
- Graceful error state when the API is unavailable.
- Automatic fallback to bundled sample data when the backend is offline.
- “Clear filters” action to reset the dashboard quickly during research sessions.

## Local quickstart

1. Start the backend API (see `../backend/README.md`).
2. Serve the static files using your preferred tool. For example, with Python:

   ```bash
   cd frontend
   python -m http.server 5173
   ```

3. Visit `http://127.0.0.1:5173` in your browser. Ensure the API is reachable at `http://127.0.0.1:8000` or adjust `API_BASE_URL` at the top of `app.js`. If the API is down the page will display sample listings from `sample-data/listings.json`.

## Future enhancements

- Replace the static assets with a Vite or Next.js project for richer state management and routing.
- Integrate authentication-aware features (saved searches, watchlists) once the backend exposes them.
- Add charts for bidding trends and notifications for time-sensitive auctions.
- Connect to live scraper output once the backend repository is replaced with a persistent datastore.
