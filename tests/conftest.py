"""Pytest fixtures for Fitness MCP."""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path
from typing import Callable, Iterator, Tuple

import pytest
from dotenv import load_dotenv
from sqlalchemy import delete
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SRC_PATH))

load_dotenv()

from src.memory.db import SessionLocal, Entry


@pytest.fixture(scope="session", autouse=True)
def load_environment() -> None:
    """Load .env once and force local-testing defaults."""
    load_dotenv()
    os.environ.setdefault("LOGFIRE_SEND_TO_LOGFIRE", "false")
    os.environ.setdefault("ENVIRONMENT", "testing")
    os.environ.setdefault("LOGFIRE_IGNORE_NO_CONFIG", "1")


@pytest.fixture
def session_and_user() -> Iterator[Tuple[Session, str]]:
    """Provide a DB session and unique user id, cleaning up afterwards."""
    user_id = f"test-user-{uuid.uuid4()}"
    with SessionLocal() as session:
        try:
            yield session, user_id
        finally:
            with SessionLocal() as cleanup:
                cleanup.execute(delete(Entry).where(Entry.user_id == user_id))
                cleanup.commit()


@pytest.fixture(scope="session")
def cleanup_entries() -> Callable[[str], None]:
    """Return a helper that deletes all entries for a user id."""

    def _cleanup(user_id: str) -> None:
        with SessionLocal() as session:
            session.execute(delete(Entry).where(Entry.user_id == user_id))
            session.commit()

    return _cleanup
