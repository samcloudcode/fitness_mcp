"""
Simplified Fitness MCP Server - 6 Core Tools

Following Claude Code's philosophy: minimal tool surface, maximum flexibility.
Everything goes in content as natural text. Only 2 status values (active/archived).
"""

from fastmcp import FastMCP
from typing import Optional, Any, Dict, List
from contextlib import contextmanager
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
from sqlalchemy import text
from datetime import datetime, date
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

# Configure Logfire before other imports
import logfire
from logfire import ConsoleOptions

# Configure Logfire for the MCP server
logfire.configure(
    send_to_logfire=os.getenv('LOGFIRE_SEND_TO_LOGFIRE', 'false').lower() == 'true',
    environment=os.getenv('ENVIRONMENT', 'development'),
    console=ConsoleOptions(min_log_level='info'),
    min_level='info',
    distributed_tracing=False,
)

# Enable SQLAlchemy auto-instrumentation
logfire.install_auto_tracing(
    modules=['src.memory.crud', 'src.memory.db'],
    min_duration=0.01
)

# Instrument SQLAlchemy
logfire.instrument_sqlalchemy()

from src.memory import crud
from src.memory.db import SessionLocal, engine

mcp = FastMCP("Fitness Memory Server (Simplified)")

# Warm up the connection pool at startup
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        logfire.info('database connection pool initialized')
except Exception as e:
    logfire.error('failed to initialize database pool', error=str(e))
    raise

@contextmanager
def get_session():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def _get_user_id() -> str:
    user_id = os.getenv('FITNESS_USER_ID') or os.getenv('DEFAULT_USER_ID')
    if not user_id:
        raise ValueError("FITNESS_USER_ID (or DEFAULT_USER_ID) must be set in environment")
    return user_id


# ====================
# 6 CORE TOOLS
# ====================

@mcp.tool
def upsert(
    kind: str,
    key: str,
    content: str,
    status: Optional[str] = None,
) -> dict:
    """Create or update an item with identity (has a key).

    Use for durable data: goals, plans, knowledge, preferences, etc.
    Same key = update existing item. Everything goes in content as natural text.

    Args:
        kind: Type of item (goal, plan, knowledge, preference, etc.)
        key: Unique identifier within kind (e.g., 'bench-225', 'knee-health')
        content: Main content/description - PUT EVERYTHING HERE as natural text
        status: 'active' (default) or 'archived'

    Examples:
        # Goal
        upsert(
            kind='goal',
            key='bench-225',
            content='Bench 225lbs x5 by March. Started at 185 in Sept.'
        )

        # Knowledge with tags in content
        upsert(
            kind='knowledge',
            key='knee-health',
            content='Knee tracking: keep knees over toes, avoid narrow stance. Tags: injury-prevention, squat-form'
        )

        # Plan with dates in content
        upsert(
            kind='plan',
            key='squat-8wk',
            content='Linear squat progression: 275→315lbs (+5/wk). 8 weeks starting Jan 1. Week 3 of 8. Deload week 4.'
        )
    """
    user_id = _get_user_id()

    with get_session() as session:
        return crud.upsert_item(
            session,
            user_id,
            kind=kind,
            key=key,
            content=content,
            status=status,
        )


@mcp.tool
def log(
    kind: str,
    content: str,
    occurred_at: Optional[str] = None,
    event_id: Optional[str] = None,
) -> dict:
    """Log a timestamped event (no key, creates new entry) OR update existing event by ID.

    Use for events: workouts, metrics, notes. Always creates new unless event_id provided.

    Args:
        kind: Type of event (workout, metric, note)
        content: Description of the event - PUT EVERYTHING HERE as natural text
        occurred_at: ISO 8601 timestamp (defaults to now)
        event_id: If provided, updates existing event instead of creating new

    Examples:
        # Log workout - everything in content
        log(
            kind='workout',
            content='Lower (52min): Squats 5x5 @ 225lbs RPE 7, RDL 3x8 @ 185lbs RPE 6',
            occurred_at='2025-01-15T10:00:00Z'
        )

        # Update existing event
        log(
            event_id='abc123...',
            content='Lower (52min): Squats 5x5 @ 230lbs RPE 7, RDL 3x8 @ 185lbs RPE 6'  # Corrected weight
        )

        # Metric
        log(
            kind='metric',
            content='Weight: 185lbs, 14% bodyfat'
        )
    """
    user_id = _get_user_id()

    parsed_time = None
    if occurred_at:
        try:
            parsed_time = datetime.fromisoformat(occurred_at)
        except Exception:
            parsed_time = None

    with get_session() as session:
        if event_id:
            # Update existing event
            return crud.update_event(
                session,
                user_id,
                event_id=event_id,
                content=content,
                occurred_at=parsed_time,
            )
        else:
            # Create new event
            return crud.log_event(
                session,
                user_id,
                kind=kind,
                content=content,
                occurred_at=parsed_time,
            )


@mcp.tool
def overview(truncate_length: int = 100) -> dict:
    """Get lightweight overview of all data with truncated content.

    Returns ALL active items but truncates verbose content for efficient scanning.
    Use 'get' tool to fetch full content for specific items.

    Args:
        truncate_length: Max chars before truncation (default 100)

    Returns:
        Organized dict with current_date, goals, plans, knowledge (truncated), etc.

    Workflow:
        1. Call overview() to scan what exists
        2. Use get() to fetch full details for relevant items
        3. Or use search() to find specific content
    """
    user_id = _get_user_id()
    with get_session() as session:
        result = crud.get_overview(session, user_id, truncate_length=truncate_length)
        today = date.today()
        result['current_date'] = today.isoformat()
        result['current_day'] = today.strftime('%A')
        return result


@mcp.tool
def get(
    items: Optional[List[Dict[str, str]]] = None,
    kind: Optional[str] = None,
    status: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 100,
) -> list[dict]:
    """Get full details for specific items or filtered list.

    Two modes:
    1. Fetch specific items by keys: get(items=[{'kind': 'goal', 'key': 'bench-225'}])
    2. Filter and list: get(kind='workout', start='2025-01-01', limit=10)

    Args:
        items: List of {'kind': ..., 'key': ...} to fetch specific items
        kind: Filter by kind (for list mode)
        status: Filter by status (for list mode)
        start: ISO date start filter (for events)
        end: ISO date end filter (for events)
        limit: Max results (default 100)

    Examples:
        # Get specific items seen in overview
        get(items=[
            {'kind': 'knowledge', 'key': 'knee-health'},
            {'kind': 'goal', 'key': 'bench-225'}
        ])

        # List recent workouts
        get(kind='workout', start='2025-01-01', limit=10)

        # Get all active goals
        get(kind='goal', status='active')
    """
    user_id = _get_user_id()

    with get_session() as session:
        if items:
            # Mode 1: Fetch specific items by keys
            keys = [(item['kind'], item['key']) for item in items]
            return crud.get_items_by_keys(session, user_id, keys=keys)
        else:
            # Mode 2: Filter and list
            if kind in ['workout', 'metric', 'note']:
                # Events - use list_events
                start_dt = datetime.fromisoformat(start) if start else None
                end_dt = datetime.fromisoformat(end) if end else None
                return crud.list_events(
                    session, user_id,
                    kind=kind,
                    start=start_dt,
                    end=end_dt,
                    limit=limit
                )
            elif kind:
                # Items - use list_items
                return crud.list_items(
                    session, user_id,
                    kind=kind,
                    status=status,
                    limit=limit
                )
            else:
                # No filters - return empty
                return []


@mcp.tool
def search(
    query: str,
    kind: Optional[str] = None,
    limit: int = 100
) -> list[dict]:
    """Search by content when you don't know the key.

    Uses PostgreSQL full-text search across key and content fields.

    Args:
        query: Search terms (e.g., 'knee pain', 'squat form')
        kind: Optional filter by kind
        limit: Max results (default 100)

    Examples:
        search('knee pain')
        search('progressive overload', kind='principle')
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.search_entries(session, user_id, query=query, kind=kind, limit=limit)


@mcp.tool
def archive(
    kind: Optional[str] = None,
    key: Optional[str] = None,
    event_id: Optional[str] = None,
    status: Optional[str] = 'active',
) -> dict:
    """Archive items or events (soft delete by setting status='archived').

    Modes:
    1. Archive specific item: archive(kind='goal', key='old-goal')
    2. Archive event: archive(event_id='abc123...')
    3. Bulk archive: archive(kind='preference', status='active')

    Args:
        kind: Kind of items to archive
        key: Specific item key to archive
        event_id: Specific event ID to archive
        status: Current status filter for bulk archive (default 'active')

    Returns:
        Dict with archived_count and details

    Examples:
        # Archive specific goal
        archive(kind='goal', key='2024-goal')

        # Archive all active preferences
        archive(kind='preference')

        # Archive specific workout event
        archive(event_id='abc-123-def')
    """
    user_id = _get_user_id()

    with get_session() as session:
        if event_id:
            # Delete specific event (events don't support archiving currently)
            success = crud.delete_event(session, user_id, event_id=event_id)
            return {
                'archived_count': 1 if success else 0,
                'event_id': event_id
            }
        elif kind and key:
            # Archive specific item
            crud.upsert_item(
                session, user_id,
                kind=kind,
                key=key,
                content='',  # Will be ignored in update
                status='archived'
            )
            return {
                'archived_count': 1,
                'kind': kind,
                'key': key
            }
        elif kind:
            # Bulk archive
            items = crud.list_items(
                session, user_id,
                kind=kind,
                status=status,
                limit=1000
            )

            archived_keys = []
            for item in items:
                if item.get('key'):
                    crud.upsert_item(
                        session, user_id,
                        kind=kind,
                        key=item['key'],
                        content=item['content'],
                        status='archived'
                    )
                    archived_keys.append(item['key'])

            return {
                'archived_count': len(archived_keys),
                'archived_keys': archived_keys,
                'kind': kind
            }
        else:
            return {'archived_count': 0, 'error': 'Must specify kind+key, event_id, or kind for bulk'}


# ====================
# RUN SERVER
# ====================

def main():
    """Entry point for the server"""
    import asyncio
    asyncio.run(mcp.run())

if __name__ == "__main__":
    main()