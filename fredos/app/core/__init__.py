"""FredOS core configuration."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application-wide settings.

    Values can be overridden by environment variables prefixed with ``FREDOS_``.
    """

    # ── Database ──────────────────────────────────────────────
    # Default: SQLite file inside the project directory.
    # Switch to PostgreSQL by setting FREDOS_DATABASE_URL.
    database_url: str = "sqlite:///fredos.db"

    # ── Filesystem artifact root ──────────────────────────────
    data_dir: Path = Path(__file__).resolve().parent.parent.parent / "fredos_data"

    # ── App metadata ──────────────────────────────────────────
    app_name: str = "FredOS"
    version: str = "0.1.0"
    debug: bool = False

    model_config = {"env_prefix": "FREDOS_"}


# Singleton – import ``settings`` anywhere.
settings = Settings()
