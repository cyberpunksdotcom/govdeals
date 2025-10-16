# GovDeals Opportunity Tracker - Expanded Project Plan

## Vision
Build an automated platform that collects, normalizes, and highlights attractive GovDeals auctions aligned with defined buying criteria. The system should be reliable, auditable, and flexible enough to adapt to policy or layout changes on GovDeals.

## Objectives
- Collect daily snapshots of listings that match configurable search criteria.
- Normalize and store auction metadata for historical comparison and analytics.
- Surface high-priority opportunities through automated scoring and alerts.
- Provide internal tooling for reviewing, annotating, and reporting on auctions.

## Architecture Overview
1. **Collector Orchestrator**
   - Scheduled runner (e.g., Prefect, Airflow, or cron-triggered container) initiates scrape jobs.
   - Manages job state, retries, metrics, and notifications of job failures.
2. **Scraper Workers**
   - Implement modular scrapers per search template or category.
   - Use `httpx` with retry/backoff; fall back to Playwright when dynamic content blocks static scraping.
   - Normalize outputs into a shared schema.
3. **Persistence Layer**
   - **Primary database**: PostgreSQL for normalized auction data, change tracking, and user annotations.
   - **Object storage**: S3-compatible bucket for images, attachments, and HTML snapshots.
   - **Cache/message bus**: Redis for rate-limit coordination, distributed locks, and task queues.
   - **Prototype note**: The FastAPI service now uses a SQLite file for persistence so engineers can iterate on filters, IDs, and downstream interfaces before the managed PostgreSQL instance is provisioned.
4. **Business Logic**
   - Rule engine scoring listings by fit (price thresholds, category, distance, end date urgency).
   - Change detection (hash diffs) to flag meaningful updates.
   - Historical analytics for price trends and seller reliability.
5. **Interfaces**
   - REST API for integration with dashboards or external tooling.
   - Web dashboard for analysts and buyers with responsive cards, filters, and watchlist controls.
   - Daily email/Slack digests summarizing top-ranked opportunities.
6. **Presentation Layer**
   - **Frontend**: Modular SPA (Next.js/Vite) backed by a component library for cards, tables, and analytics widgets. The prototype dashboard already exercises the API’s keyword, category, bid range, and closing-window filters while providing an offline-friendly fallback.
   - **Backend-for-frontend (BFF)**: FastAPI service aggregating listings, scoring results, and powering real-time interactions.
   - **Design system**: Shared tokens for typography, spacing, and color palette to keep the dashboard consistent across surfaces.
7. **Observability & Ops**
   - Centralized logging (ELK, OpenSearch, or CloudWatch) with structured event logs.
   - Metrics/alerts via Prometheus + Grafana, plus on-call runbooks.
   - Feature flags and configuration stored in a secure manager (HashiCorp Vault, AWS Secrets Manager).

## Infrastructure Strategy
### Environment Layout
- **Development**: Docker Compose stack for local services (PostgreSQL, Redis, MinIO, API, worker).
- **Staging**: Managed Kubernetes cluster (EKS/GKE) or ECS Fargate with IaC for reproducibility. Mirrors production scale with smaller quotas.
- **Production**: Managed cloud environment with autoscaling worker pools and durable storage.

### Core Components
| Component | Service Choice | Notes |
|-----------|----------------|-------|
| Job orchestration | Prefect Cloud or Airflow on managed Kubernetes | Prefect for rapid iteration; Airflow if more complex DAGs required. |
| Worker execution | Containerized Python services in ECS Fargate/Kubernetes | Allows horizontal scaling and rolling updates. |
| Database | AWS RDS PostgreSQL (multi-AZ) | Automated backups, point-in-time recovery. |
| Object storage | AWS S3 | Lifecycle policies for archival, versioned snapshots. |
| Cache/Queue | AWS ElastiCache Redis | Supports distributed locking and Celery/Prefect task queues. |
| Secrets | AWS Secrets Manager | Rotates credentials, integrates with IAM. |
| Monitoring | CloudWatch + Prometheus/Grafana | Combine managed metrics with custom dashboards. |
| CI/CD | GitHub Actions -> Terraform Cloud -> ArgoCD (if K8s) | Automated testing, infrastructure deployment, and application rollout. |

### Infrastructure as Code (IaC)
- Terraform modules define network, compute, and data stores.
- Separate workspaces for dev/staging/prod with shared modules.
- Use Terragrunt or Terraform Cloud for pipeline-driven deployments.

### Security & Compliance
- IAM roles with least privilege for each service component.
- Encrypt data at rest (RDS, S3) and in transit (TLS everywhere).
- Implement WAF/rate limiting in front of public APIs.
- Regular vulnerability scanning (Dependabot, Trivy) and patch cadence.

## Project Timeline (Approximate)
### Phase 0 – Discovery & Compliance (Week 1)
- Confirm legal allowances for scraping; document policies.
- Capture detailed requirements, buying criteria, and KPI definitions.
- Establish project repo structure, coding standards, and workflows.

### Phase 1 – Foundations (Weeks 2-4)
- Implement Terraform baseline (network, RDS, S3, Redis, ECS/K8s cluster).
- Build local development environment (Docker Compose).
- Scaffold Python scraper service and shared libraries (HTTP client, parser utilities).
- Set up CI/CD pipelines (linting, tests, container builds).

### Phase 2 – Scraper MVP (Weeks 5-7)
- Implement core search templates and pagination handling.
- Integrate Prefect/Airflow DAG for daily collection.
- Create PostgreSQL schema and migration workflow.
- Store raw and normalized records; implement deduplication logic.
- Begin unit tests with HTML fixtures; set up logging/metrics baseline.

### Phase 3 – Business Logic & Alerts (Weeks 8-10)
- Implement scoring engine and configurable watchlists.
- Build notification pipelines (email, Slack) with templating.
- Add historical change tracking and dashboards.

### Phase 4 – Interfaces & Hardening (Weeks 11-13)
- Develop admin UI/REST API for browsing listings and annotations.
- Conduct load testing, chaos testing, and failover drills.
- Finalize observability stack and alert thresholds.
- Security review, penetration testing, and compliance sign-off.

### Phase 4a – UX Polish & Enablement (Weeks 11-12, overlaps Phase 4)
- Build polished dashboard views (list, table, analytics) and responsive layouts.
- Implement onboarding checklist and contextual help modals.
- Record short walkthrough videos and capture screenshots for the user guide.

### Phase 5 – Launch & Iteration (Weeks 14+)
- Production rollout with staged ramp-up.
- Monitor KPIs, adjust scraping frequency, and onboard stakeholders.
- Backlog grooming for future enhancements (ML-based scoring, pricing predictions).

## Delivery Process
1. **Work Tracking**: Use Kanban board (e.g., Jira, Linear) synced with `tasks/backlog.md` for transparency.
2. **Ceremonies**: Weekly planning/review, daily async stand-ups via Slack updates.
3. **Definition of Done**: Code merged with tests, documentation updated, monitoring configured.
4. **Quality Gates**: Automated lint/test in CI, peer review, staging deployment verification.
5. **Risk Management**: Maintain risk register, escalate blockers within 24 hours, and log mitigation steps in `docs/progress_log.md`.

## Next Steps
- Approve architecture & timeline.
- Stand up Jira/Linear workspace and map backlog items from `tasks/backlog.md`.
- Begin Phase 0 activities with compliance and requirement discovery interviews.

