# GovDeals Opportunity Tracker Planning

This repository now contains both the planning artifacts and the first runnable prototype for an application that scrapes GovDeals daily and prioritizes promising auctions.

## Documentation
- [`docs/project_overview.md`](docs/project_overview.md): Comprehensive plan covering architecture, infrastructure, timeline, and delivery process.
- [`docs/progress_log.md`](docs/progress_log.md): Rolling log of milestones, decisions, and outstanding questions.
- [`docs/user_guide.md`](docs/user_guide.md): Walkthrough of the dashboard workflow for buyers and analysts.
- [`docs/quickstart.md`](docs/quickstart.md): End-to-end setup instructions for running the prototype locally.

## Task Management
- [`tasks/backlog.md`](tasks/backlog.md): Lightweight backlog synchronized with the primary task board (e.g., Jira/Linear).

## Prototype code
- [`backend/`](backend/): FastAPI service exposing listings and a health endpoint. Reads from a JSON fixture today to unblock front-end work and now supports query-parameter filtering backed by automated tests.
- [`frontend/`](frontend/): Static dashboard that consumes the API, featuring keyword, category, bid range, and closing-window filters with automatic fallback to bundled sample data.

Follow the [quickstart guide](docs/quickstart.md) to launch both services locally.

## Next Steps
1. Review and refine the project plan with stakeholders.
2. Populate the backlog with estimates and owners once requirements are confirmed.
3. Stand up the scraping pipeline and replace the fixture-based repository.
4. Connect the API to a persistent datastore and begin ingesting real GovDeals data for end-to-end validation.

