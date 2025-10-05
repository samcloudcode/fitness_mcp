#!/usr/bin/env python3
"""Check the overview of seeded data."""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

from src.memory.db import SessionLocal
from src.memory import crud

def get_user_id() -> str:
    user_id = os.getenv('FITNESS_USER_ID') or os.getenv('DEFAULT_USER_ID')
    if not user_id:
        raise ValueError("FITNESS_USER_ID (or DEFAULT_USER_ID) must be set in environment")
    return user_id

def check_overview():
    user_id = get_user_id()
    session = SessionLocal()

    try:
        overview = crud.get_overview(session, user_id)
        print(json.dumps(overview, indent=2))
    finally:
        session.close()

if __name__ == "__main__":
    check_overview()
