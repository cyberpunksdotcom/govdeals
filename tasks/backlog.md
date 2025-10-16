# Backlog

The backlog mirrors the authoritative task board (Jira/Linear) and tracks work status snapshots for transparency.

## Status Legend
- **TODO**: Not yet started.
- **IN PROGRESS**: Currently being worked on.
- **BLOCKED**: Impeded; see notes.
- **DONE**: Completed and verified.

## Discovery & Compliance
- **TODO** Conduct legal/policy review of GovDeals scraping allowances; document outcomes.
- **TODO** Gather stakeholder buying criteria and ranking KPIs.
- **TODO** Define data retention and privacy requirements.

## Foundations
- **TODO** Draft Terraform module structure for core infrastructure.
- **TODO** Design database schema ERD and migration strategy.
- **TODO** Set up local Docker Compose environment definition.
- **TODO** Configure CI/CD pipeline skeleton with lint/test stages.

## Scraper MVP
- **TODO** Implement resilient HTTP client wrapper with retry/backoff and logging.
- **TODO** Create modular scraper templates for priority categories.
- **TODO** Build ingestion pipeline writing to PostgreSQL with deduplication hashes.
- **TODO** Establish HTML fixture library and parser unit tests.

## Business Logic & Alerts
- **TODO** Design scoring rubric and watchlist configuration UI/JSON schema.
- **TODO** Implement notification services (email, Slack) with templated summaries.
- **TODO** Create change detection service for pricing/status updates.

## Interfaces & Hardening
- **DONE** Build read-only dashboard prototype backed by fixture data (frontend/index.html, app.js).
- **DONE** Add query-parameter filtering to the listings API with validation and tests.
- **TODO** Scaffold admin dashboard for listing review and annotation.
- **TODO** Define observability SLOs and alert thresholds.
- **TODO** Plan load/chaos testing scenarios and tooling.

## Launch & Iteration
- **TODO** Define production rollout checklist and on-call runbook.
- **TODO** Outline roadmap enhancements (ML pricing predictions, seller insights).
- **DONE** Wire advanced bid/end-time filters into the dashboard once backend adoption is confirmed.

