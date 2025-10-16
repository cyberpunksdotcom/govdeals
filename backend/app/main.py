"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import listings


def create_app() -> FastAPI:
    """Application factory for uvicorn."""

    app = FastAPI(title="GovDeals Opportunity Tracker", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["system"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(listings.router)
    return app


app = create_app()
