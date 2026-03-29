"""FredOS API — FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import Base, engine
from app.api.routes import router as api_router
from app.api.bridge_routes import bridge_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup (dev convenience — Alembic is canonical)."""
    import app.models  # noqa: F401  — register all models
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FredOS",
    description="Memory-first personal AI operating system — REST API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api")
app.include_router(bridge_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
