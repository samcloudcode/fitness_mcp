from fastmcp import FastMCP
from typing import Optional, Any, Dict, List, Literal
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
    distributed_tracing=False,  # MCP server typically runs standalone
)

# Enable SQLAlchemy auto-instrumentation
logfire.install_auto_tracing(
    modules=['src.memory.crud', 'src.memory.db'],
    min_duration=0.01  # Track operations taking 10ms or more
)

# Instrument SQLAlchemy
logfire.instrument_sqlalchemy()

from src.memory import crud
from src.memory.db import SessionLocal, engine

mcp = FastMCP("Fitness Memory Server")

# Warm up the connection pool at startup
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        logfire.info(
            'database connection pool initialized',
            pool_size=engine.pool.size(),
            checked_out=engine.pool.checkedout(),
            overflow=engine.pool.overflow(),
            total=engine.pool.checkedin()
        )
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


@mcp.tool
def upsert_item(
    kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','metric','note'],
    key: str,
    content: str,
    priority: Optional[int] = None,
    status: Optional[str] = None,
    tags: Optional[str] = None,
    parent_key: Optional[str] = None,
    due_date: Optional[str] = None,  # ISO date YYYY-MM-DD
    attrs: Optional[Dict[str, Any]] = None,
) -> dict:
    """Upsert a durable item by kind+key.

    Args:
    - kind: one of goal, plan, plan-step, strategy, preference, knowledge, principle, current, workout, metric, note
    - key: slug `^[a-z0-9-]{1,64}$`
    - content: short free text payload
    - priority: 1 (highest) … 5 (lowest)
    - status: e.g., active|paused|achieved|archived
    - due_date: ISO date `YYYY-MM-DD`
    - attrs: small object for extras (e.g., {"distance_km":5})

    Example:
    upsert_item(kind='knowledge', key='knee-health-best-practices', content='Bullet points...')
    """
    user_id = _get_user_id()
    parsed_due: Optional[date] = None
    if due_date:
        try:
            parsed_due = date.fromisoformat(due_date)
        except Exception:
            parsed_due = None
    with get_session() as session:
        return crud.upsert_item(
            session,
            user_id,
            kind=kind,
            key=key,
            content=content,
            priority=priority,
            status=status,
            tags=tags,
            parent_key=parent_key,
            due_date=parsed_due,
            attrs=attrs,
        )


@mcp.tool
def get_item(kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','metric','note'], key: str) -> Optional[dict]:
    """Get a durable item by kind+key.

    Example:
    get_item(kind='plan', key='running-progression')
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.get_item(session, user_id, kind=kind, key=key)


@mcp.tool
def delete_item(kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','metric','note'], key: str) -> bool:
    """Delete a durable item by kind+key.

    Example:
    delete_item(kind='preference', key='supersets')
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.delete_item(session, user_id, kind=kind, key=key)


@mcp.tool
def list_items(
    kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','metric','note'],
    status: Optional[str] = None,
    tag_contains: Optional[str] = None,
    parent_key: Optional[str] = None,
    limit: int = 100
) -> list[dict]:
    """List durable items (up to limit).

    Example:
    list_items(kind='plan', status='active', limit=20)
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.list_items(session, user_id, kind=kind, status=status, tag_contains=tag_contains, parent_key=parent_key, limit=limit)


@mcp.tool
def log_event(
    kind: Literal['workout','metric','note'],
    content: str,
    occurred_at: Optional[str] = None,  # ISO datetime
    tags: Optional[str] = None,
    parent_key: Optional[str] = None,
    attrs: Optional[Dict[str, Any]] = None
) -> dict:
    """Log an event-like entry (no key).

    Args:
    - occurred_at: ISO 8601 `YYYY-MM-DDTHH:MM:SS[Z]`
    - attrs: small object (e.g., {"distance_km":5})

    Example:
    log_event(kind='workout', content='5k in 25m', occurred_at='2025-10-01T07:30:00Z')
    """
    user_id = _get_user_id()
    parsed_time: Optional[datetime] = None
    if occurred_at:
        try:
            parsed_time = datetime.fromisoformat(occurred_at)
        except Exception:
            parsed_time = None
    with get_session() as session:
        return crud.log_event(session, user_id, kind=kind, content=content, occurred_at=parsed_time, tags=tags, parent_key=parent_key, attrs=attrs)


@mcp.tool
def list_events(
    kind: Optional[Literal['workout','metric','note']] = None,
    start: Optional[str] = None,  # ISO datetime
    end: Optional[str] = None,    # ISO datetime
    tag_contains: Optional[str] = None,
    parent_key: Optional[str] = None,
    limit: int = 100
) -> list[dict]:
    """List recent events (up to limit).

    Example:
    list_events(kind='workout', start='2025-09-01T00:00:00Z', end='2025-10-01T00:00:00Z')
    """
    user_id = _get_user_id()
    start_dt = None
    end_dt = None
    try:
        if start:
            start_dt = datetime.fromisoformat(start)
        if end:
            end_dt = datetime.fromisoformat(end)
    except Exception:
        start_dt = start_dt
        end_dt = end_dt
    with get_session() as session:
        return crud.list_events(session, user_id, kind=kind, start=start_dt, end=end_dt, tag_contains=tag_contains, parent_key=parent_key, limit=limit)


@mcp.tool
def search_entries(query: str, kind: Optional[Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','metric','note']] = None, limit: int = 100) -> list[dict]:
    """Full-text search across entries.

    Example:
    search_entries(query='knee health', kind='knowledge')
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.search_entries(session, user_id, query=query, kind=kind, limit=limit)


@mcp.tool
def get_overview() -> dict:
    """Return an organized overview for the current user.

    Example:
    get_overview()
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.get_overview(session, user_id)


@mcp.tool
def describe_conventions() -> dict:
    """Describe allowed kinds, key conventions, date formats, and attr hints.

    Example:
    describe_conventions()
    """
    kinds = ['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','metric','note']
    return {
        'kinds': kinds,
        'key_regex': '^[a-z0-9-]{1,64}$',
        'date_formats': {
            'date': 'YYYY-MM-DD',
            'datetime': 'YYYY-MM-DDTHH:MM:SS[.ffffff][Z]'
        },
        'defaults': {
            'limit': 100,
            'priority_range': [1, 5],
        },
        'attrs_hints': {
            'workout': {'distance_km': 'number', 'duration_min': 'number', 'sets': 'array of {ex,reps,weight,rpe?}'},
            'current': {'numeric_value': 'number', 'unit': 'string'},
            'goal': {'target_text': 'string'},
        },
        'examples': {
            'upsert_item': {
                'kind': 'knowledge', 'key': 'knee-health-best-practices', 'content': 'Bullet points...'
            },
            'log_event': {
                'kind': 'workout', 'content': '5k in 25m', 'occurred_at': '2025-10-01T07:30:00Z'
            },
            'list_items': {
                'kind': 'plan', 'status': 'active', 'limit': 20
            }
        }
    }

def main():
    """Main entry point for the MCP server"""
    # Log startup and initialization
    with logfire.span('mcp server startup'):
        logfire.info('starting fitness memory mcp server', tools=['upsert_item','get_item','delete_item','list_items','log_event','list_events','search_entries','get_overview','describe_conventions'])
        logfire.info('logfire configured', environment=os.getenv('ENVIRONMENT', 'development'))
        logfire.info('database connection initialized')

    # Run the server (this blocks until shutdown)
    try:
        logfire.info('mcp server ready and listening')
        mcp.run()  # Defaults to stdio transport
    except Exception as err:
        logfire.exception('mcp server error during execution')
        raise

if __name__ == "__main__":
    main()
