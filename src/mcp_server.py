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
    kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','workout-plan','metric','note','issue'],
    key: str,
    content: str,
    priority: Optional[int | str] = None,
    status: Optional[str] = None,
    tags: Optional[str] = None,
    parent_key: Optional[str] = None,
    due_date: Optional[str] = None,  # ISO date YYYY-MM-DD
    attrs: Optional[Dict[str, Any] | str] = None,
) -> dict:
    """Create or update a durable item by kind+key.

    Use this to store permanent data like goals, plans, preferences, or knowledge that needs to persist.
    Items with the same kind+key will be updated. For time-stamped events (workouts, metrics), use log_event instead.

    Args:
        kind: Category of item (goal, plan, plan-step, strategy, preference, knowledge, principle, current, workout, workout-plan, metric, note, issue)
        key: Unique slug identifier (lowercase alphanumeric with hyphens, max 64 chars, e.g., 'run-5k-goal')
        content: Main content/description (string)
        priority: Optional priority - accepts any string ("urgent", "high") or int (1, 2, 3). No validation applied.
        status: Optional status string (active, paused, achieved, archived, draft, planned)
        tags: Optional comma-separated tags string (e.g., 'running,cardio')
        parent_key: Optional reference to parent item (e.g., plan-step refers to a plan)
        due_date: Optional ISO date string YYYY-MM-DD (e.g., '2025-12-01')
        attrs: Optional dict for structured data. Accepts dict object or JSON string (will be parsed).
               Example: {"distance_km": 5, "exercises": [{"name": "Squat", "sets": 5}]}
               Also accepts: '{"distance_km": 5}' (will be parsed automatically)

    Returns:
        Complete item with id, user_id, kind, key, content, timestamps, and all fields

    Examples:
        # Basic item
        upsert_item(
            kind='goal',
            key='bench-225',
            content='Bench press 225lbs for 5 reps',
            priority=1,
            status='active'
        )

        # With attrs dict (note: dict object, not string!)
        upsert_item(
            kind='plan-step',
            key='week-1',
            content='Week 1: Build base',
            attrs={'distance_km': 20, 'num_runs': 4}
        )
    """
    user_id = _get_user_id()

    # Flexible priority: accept any string or int (no validation)
    # Users can use "urgent", "high", 1, 2, etc. - whatever works for them
    priority_value = priority

    # Flexible attrs: if string provided, try parsing as JSON
    attrs_value = attrs
    if attrs is not None and isinstance(attrs, str):
        try:
            attrs_value = json.loads(attrs)
            logfire.info('parsed attrs from JSON string', attrs_keys=list(attrs_value.keys()))
        except json.JSONDecodeError as e:
            logfire.warn('failed to parse attrs as JSON, using as-is', error=str(e))
            attrs_value = attrs

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
            priority=priority_value,
            status=status,
            tags=tags,
            parent_key=parent_key,
            due_date=parsed_due,
            attrs=attrs_value,
        )


@mcp.tool
def get_item(kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','workout-plan','metric','note','issue'], key: str) -> Optional[dict]:
    """Retrieve a specific durable item by kind+key.

    Use this to fetch the current state of a known item. Returns None if not found.
    For discovering items, use list_items or search_entries instead.

    Args:
        kind: Category of item
        key: Unique slug identifier

    Returns:
        Item dict with all fields, or None if not found

    Example:
        get_item(kind='plan', key='running-progression')
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.get_item(session, user_id, kind=kind, key=key)


@mcp.tool
def get_items_detail(items: List[Dict[str, str]]) -> list[dict]:
    """Fetch full content for multiple items seen in overview (which shows truncated content).

    Use this after get_overview() to retrieve full content for specific entries you need details on.
    Overview truncates verbose content to 100 chars - use this tool to get the complete text.

    Args:
        items: List of dicts with 'kind' and 'key' fields, e.g., [{"kind": "knowledge", "key": "knee-health"}, {"kind": "principle", "key": "progressive-overload"}]

    Returns:
        List of full item dicts with complete content, status, tags, attrs, timestamps

    Examples:
        # After seeing truncated knowledge in overview
        overview = get_overview()
        # overview['knowledge'][0] = {"key": "knee-health...", "content": "Knee Health Best Practices:..."}

        # Get full content
        details = get_items_detail([
            {"kind": "knowledge", "key": "knee-health-best-practices"},
            {"kind": "principle", "key": "progressive-overload"}
        ])
        # details[0]['content'] now has full text, not truncated

        # Or get details for all knowledge at once
        keys = [{"kind": "knowledge", "key": k["key"]} for k in overview.get("knowledge", [])]
        all_knowledge = get_items_detail(keys)
    """
    user_id = _get_user_id()

    # Convert list of dicts to list of tuples
    keys = [(item['kind'], item['key']) for item in items]

    with get_session() as session:
        return crud.get_items_by_keys(session, user_id, keys=keys)


@mcp.tool
def delete_item(kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','workout-plan','metric','note','issue'], key: str) -> bool:
    """Permanently delete a durable item by kind+key.

    Use this to remove items that are no longer needed. Consider using status='archived'
    in upsert_item instead to keep historical data. This operation cannot be undone.

    Args:
        kind: Category of item
        key: Unique slug identifier

    Returns:
        True if item was deleted, False if not found

    Example:
        delete_item(kind='preference', key='supersets')
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.delete_item(session, user_id, kind=kind, key=key)


@mcp.tool
def archive_items(
    kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','workout-plan','metric','note','issue'],
    status: Optional[str] = 'active',
    tag_contains: Optional[str] = None,
    parent_key: Optional[str] = None
) -> dict:
    """Archive multiple items at once (sets status='archived').

    This is safer than deleting - archived items are hidden from overview but preserved.
    Use this when user wants to "remove" or "delete all" items of a type.

    Args:
        kind: Category of items to archive
        status: Filter items by current status (default: 'active')
        tag_contains: Optional filter by tag substring
        parent_key: Optional filter by parent item

    Returns:
        Dict with count of archived items and list of keys archived

    Examples:
        # Archive all active preferences
        archive_items(kind='preference', status='active')

        # Archive specific tagged goals
        archive_items(kind='goal', tag_contains='2024')
    """
    user_id = _get_user_id()
    with get_session() as session:
        # Get items to archive
        items = crud.list_items(
            session, user_id,
            kind=kind,
            status=status,
            tag_contains=tag_contains,
            parent_key=parent_key,
            limit=1000
        )

        archived_keys = []
        for item in items:
            if item['key']:  # Only archive items with keys
                crud.upsert_item(
                    session, user_id,
                    kind=kind,
                    key=item['key'],
                    content=item['content'],
                    priority=item.get('priority'),
                    status='archived',
                    tags=item.get('tags'),
                    parent_key=item.get('parent_key'),
                    due_date=item.get('due_date'),
                    attrs=item.get('attrs', {})
                )
                archived_keys.append(item['key'])

        return {
            'archived_count': len(archived_keys),
            'archived_keys': archived_keys,
            'kind': kind
        }


@mcp.tool
def list_items(
    kind: Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','workout-plan','metric','note','issue'],
    status: Optional[str] = None,
    tag_contains: Optional[str] = None,
    parent_key: Optional[str] = None,
    limit: int = 100
) -> list[dict]:
    """List durable items with optional filtering (up to limit).

    Use this to browse items of a specific kind, optionally filtered by status, tags, or parent.
    Results are sorted by priority (ascending), then updated_at (descending).
    For text-based search, use search_entries instead.

    Args:
        kind: Category of items to list
        status: Optional filter by status (e.g., 'active', 'achieved')
        tag_contains: Optional filter by tag substring (case-insensitive)
        parent_key: Optional filter by parent item key
        limit: Maximum number of items to return (default 100)

    Returns:
        List of items, each containing id, kind, key, content, status, priority, tags,
        created_at, updated_at, due_date, and attrs

    Example:
        list_items(kind='plan', status='active', limit=20)
        list_items(kind='plan-step', parent_key='running-progression')
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
    """Log a time-stamped event (no key, creates new entry each time).

    Use this for recording events that happen at a specific time (workouts, measurements, notes).
    Unlike upsert_item, this always creates a new entry. Use for historical tracking and timelines.

    Args:
        kind: Event type (workout, metric, note)
        content: Description of the event (string)
        occurred_at: Optional ISO 8601 timestamp string (YYYY-MM-DDTHH:MM:SS[Z]). Defaults to current time if not provided.
        tags: Optional space-separated tags string (e.g., 'running cardio morning')
        parent_key: Optional reference to related item (e.g., workout linked to a plan)
        attrs: Optional dict object (NOT a JSON string!) for structured data.
               Example: {"distance_km": 5, "duration_min": 25, "avg_hr": 145}
               WRONG: '{"distance_km": 5}' - don't stringify!

    Returns:
        Created event with id, content, occurred_at, and all fields

    Examples:
        # Workout with comprehensive attrs
        log_event(
            kind='workout',
            content='Lower body: Squat 5x5@245 (RPE 8)',
            occurred_at='2025-10-05T18:30:00Z',
            tags='strength lower-body',
            attrs={
                'exercises': [
                    {'name': 'Squat', 'sets': 5, 'reps': 5, 'weight_lbs': 245, 'rpe': 8}
                ],
                'duration_min': 45
            }
        )

        # Simple metric
        log_event(
            kind='metric',
            content='Morning weigh-in',
            attrs={'weight_lbs': 180.5}
        )
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
    """List time-stamped events with optional filtering (up to limit).

    Use this to retrieve historical events (workouts, metrics, notes) within a time range.
    Results are sorted by occurred_at (descending), showing most recent first.

    Args:
        kind: Optional event type filter (workout, metric, note). If None, returns all event types.
        start: Optional ISO 8601 start timestamp (inclusive)
        end: Optional ISO 8601 end timestamp (inclusive)
        tag_contains: Optional filter by tag substring (case-insensitive)
        parent_key: Optional filter by parent item key
        limit: Maximum number of events to return (default 100)

    Returns:
        List of events, each containing id, ref (short id), kind, content, occurred_at,
        tags, and attrs

    Example:
        list_events(kind='workout', start='2025-09-01T00:00:00Z', end='2025-10-01T00:00:00Z')
        list_events(kind='metric', tag_contains='weight', limit=30)
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
def update_event(
    event_id: str,
    content: Optional[str] = None,
    occurred_at: Optional[str] = None,
    tags: Optional[str] = None,
    parent_key: Optional[str] = None,
    attrs: Optional[Dict[str, Any]] = None,
    replace_attrs: bool = False
) -> Optional[dict]:
    """Update an existing event by ID. Only provided fields will be updated.

    Use this to correct mistakes in logged workouts, add missing information, or update details.
    Events are identified by their UUID (the 'id' field returned from log_event or list_events).

    Args:
        event_id: UUID of the event to update (from event's 'id' field)
        content: Updated content text (optional)
        occurred_at: Updated ISO datetime (optional)
        tags: Updated tags (optional)
        parent_key: Updated parent reference (optional)
        attrs: Attributes to add/update (optional). By default, merges with existing attrs.
        replace_attrs: If True, replaces entire attrs object. If False (default), merges new attrs with existing.

    Returns:
        Updated event dict if found, None if event doesn't exist

    Example:
        # First, get the event ID from a recent workout
        events = list_events(kind='workout', limit=1)
        event_id = events[0]['id']

        # Update to add missing RPE data (MERGES with existing attrs by default)
        update_event(
            event_id=event_id,
            attrs={'rpe': 8, 'notes': 'Felt stronger today'}
        )
        # No need to spread existing attrs - merging is automatic!
    """
    user_id = _get_user_id()
    parsed_time = None
    if occurred_at:
        try:
            parsed_time = datetime.fromisoformat(occurred_at)
        except Exception:
            parsed_time = None
    with get_session() as session:
        return crud.update_event(
            session,
            user_id,
            event_id=event_id,
            content=content,
            occurred_at=parsed_time,
            tags=tags,
            parent_key=parent_key,
            attrs=attrs,
            replace_attrs=replace_attrs
        )


@mcp.tool
def delete_event(event_id: str) -> bool:
    """Delete an event by ID.

    Use this to remove incorrectly logged events or duplicate entries.
    Cannot be undone - use with caution.

    Args:
        event_id: UUID of the event to delete (from event's 'id' field)

    Returns:
        True if event was deleted, False if not found

    Example:
        # Delete a mistakenly logged workout
        events = list_events(kind='workout', limit=5)
        duplicate_id = events[2]['id']
        delete_event(event_id=duplicate_id)
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.delete_event(session, user_id, event_id=event_id)


@mcp.tool
def search_entries(query: str, kind: Optional[Literal['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','workout-plan','metric','note','issue']] = None, limit: int = 100) -> list[dict]:
    """Full-text search across all entries (items and events).

    Use this to find entries by content when you don't know the exact key or want to discover
    related information. Searches both key and content fields using PostgreSQL full-text search.
    Results are sorted by relevance and recency.

    Args:
        query: Search terms (e.g., 'knee health', 'running progression')
        kind: Optional filter by specific kind
        limit: Maximum number of results to return (default 100)

    Returns:
        List of matching entries (both items with keys and events), each containing
        all fields sorted by updated_at (descending)

    Example:
        search_entries(query='knee health', kind='knowledge')
        search_entries(query='running', limit=50)
    """
    user_id = _get_user_id()
    with get_session() as session:
        return crud.search_entries(session, user_id, query=query, kind=kind, limit=limit)


@mcp.tool
def report_issue(
    title: str,
    description: str,
    issue_type: Literal['bug', 'feature', 'enhancement'] = 'bug',
    severity: Literal['critical', 'high', 'medium', 'low'] = 'medium',
    context: Optional[str] = None,
    tags: Optional[str] = None
) -> dict:
    """Report a backend issue, bug, or feature request.

    Use this to report bugs, request features, or suggest enhancements to the fitness tracking system.
    Issues are stored separately from fitness data and won't clutter your overview or workout history.
    Developers will review and address reported issues.

    Args:
        title: Short title/summary (becomes the key as a slug)
        description: Detailed description of the issue or feature request
        issue_type: Type of issue (bug, feature, enhancement)
        severity: Severity level (critical, high, medium, low)
        context: Optional additional context (stack traces, reproduction steps, etc.)
        tags: Optional space-separated tags (e.g., 'database performance')

    Returns:
        Created issue with id, key, content, and metadata

    Examples:
        # Report a bug
        report_issue(
            title='Overview times out with large datasets',
            description='get_overview() times out when user has >500 workouts',
            issue_type='bug',
            severity='high',
            context='Error: psycopg.OperationalError: timeout expired'
        )

        # Request a feature
        report_issue(
            title='Add weekly summary tool',
            description='Tool to generate weekly workout summary with volume/intensity stats',
            issue_type='feature',
            severity='low',
            tags='analytics reporting'
        )
    """
    user_id = _get_user_id()

    # Convert title to slug key (lowercase, hyphens, no special chars)
    import re
    key = re.sub(r'[^a-z0-9-]', '', title.lower().replace(' ', '-'))[:64]

    # Combine description and context
    content = description
    if context:
        content += f"\n\nContext:\n{context}"

    with get_session() as session:
        return crud.upsert_item(
            session,
            user_id,
            kind='issue',
            key=key,
            content=content,
            priority={'critical': 1, 'high': 2, 'medium': 3, 'low': 4}.get(severity, 3),
            status='open',
            tags=f"{issue_type} {severity} {tags or ''}".strip(),
            attrs={
                'issue_type': issue_type,
                'severity': severity,
                'title': title
            }
        )


@mcp.tool
def list_issues(
    status: Optional[str] = 'open',
    issue_type: Optional[Literal['bug', 'feature', 'enhancement']] = None,
    severity: Optional[Literal['critical', 'high', 'medium', 'low']] = None,
    limit: int = 100
) -> list[dict]:
    """List backend issues with optional filtering (developer use only).

    Retrieve issues for review and tracking. Issues are excluded from fitness
    overview and general searches.

    Args:
        status: Filter by status (open, in-progress, resolved, wontfix) - default: open
        issue_type: Optional filter by type (bug, feature, enhancement)
        severity: Optional filter by severity (critical, high, medium, low)
        limit: Maximum number of issues to return (default 100)

    Returns:
        List of issues with all fields, sorted by priority then updated_at

    Examples:
        # Get open bugs
        list_issues(status='open', issue_type='bug')

        # Get critical issues
        list_issues(severity='critical')

        # Get all issues regardless of status
        list_issues(status=None, limit=200)
    """
    user_id = _get_user_id()

    with get_session() as session:
        issues = crud.list_items(
            session, user_id,
            kind='issue',
            status=status,
            limit=limit
        )

        # Filter by issue_type or severity if specified
        if issue_type:
            issues = [i for i in issues if i.get('attrs', {}).get('issue_type') == issue_type]
        if severity:
            issues = [i for i in issues if i.get('attrs', {}).get('severity') == severity]

        return issues


@mcp.tool
def get_started() -> dict:
    """Get a quick start guide with common workflows and examples.

    Use this when first learning the server or to remind yourself of common patterns.
    Returns example commands and recommended workflows for typical use cases.

    Returns:
        Guide containing:
        - quick_start: Step-by-step first commands to try
        - common_workflows: Typical patterns for different use cases
        - tool_guide: When to use each tool
        - see_also: References to other helpful tools

    Example:
        get_started()
    """
    return {
        "quick_start": {
            "1_see_whats_stored": "get_overview() - Start here to see all your data",
            "2_add_a_goal": "upsert_item(kind='goal', key='run-5k', content='Run 5K under 25 minutes', status='active')",
            "3_log_workout": "log_event(kind='workout', content='3km easy run', occurred_at='2025-10-05T07:00:00Z', attrs={'distance_km': 3})",
            "4_search": "search_entries(query='running') - Find anything related to running"
        },
        "common_workflows": {
            "goal_tracking": "1. upsert_item(kind='goal') → 2. upsert_item(kind='plan') → 3. log_event(kind='workout') → 4. get_overview()",
            "knowledge_base": "1. upsert_item(kind='knowledge') → 2. search_entries(query='...') → 3. get_item(kind='knowledge', key='...')",
            "workout_logging": "1. log_event(kind='workout', attrs={...}) → 2. list_events(kind='workout', start='...', end='...') → 3. Analyze progress",
            "plan_with_steps": "1. upsert_item(kind='plan', key='plan-key') → 2. upsert_item(kind='plan-step', parent_key='plan-key', key='step-1') → 3. get_overview()"
        },
        "tool_guide": {
            "when_to_upsert_item": "For durable data that needs a memorable key (goals, plans, knowledge, preferences)",
            "when_to_log_event": "For timestamped occurrences that should create new entries each time (workouts, measurements)",
            "when_to_get_overview": "At start of conversation or to see the big picture",
            "when_to_search_entries": "When looking for content but don't know the exact key",
            "when_to_list_items": "When browsing items of a specific kind with filters",
            "when_to_list_events": "When reviewing historical events in a time range"
        },
        "see_also": {
            "conventions": "describe_conventions() - Learn about kinds, key formats, and attribute patterns",
            "overview": "get_overview() - See everything that's stored"
        }
    }


@mcp.tool
def get_overview(truncate_length: int = 100) -> dict:
    """Get a scannable overview of all user data with truncated content - start here!

    Returns all active items but with verbose content truncated for efficient scanning.
    Use get_items_detail() to fetch full content for specific items you need details on.

    Args:
        truncate_length: Max characters for verbose content before truncation (default 100).
                        Higher values = more context, lower values = faster scanning.

    IMPORTANT: Verbose kinds (knowledge, principles, preferences, plan-steps, workouts) show truncated
    content ending in "..." - this is intentional to reduce context size. Use get_items_detail() to
    get full text when needed.

    Returns:
        Organized structure (only non-empty sections shown):
        - current_date: ISO date string (YYYY-MM-DD)
        - current_day: Day of week (e.g., 'Monday')
        - strategies: {long_term: {...}, short_term: {...}} [TRUNCATED]
        - goals: {active: [...], achieved: [...]} [FULL CONTENT]
        - plans: {active: [...], steps: {plan-key: [...]}} [FULL for plans, TRUNCATED for steps]
        - current: [...]  (current state/metrics) [FULL CONTENT]
        - preferences: [...]  [TRUNCATED - use get_items_detail() for full text]
        - knowledge: [...]  [TRUNCATED - use get_items_detail() for full text]
        - principles: [...]  [TRUNCATED - use get_items_detail() for full text]
        - recent_workouts: [...]  (last 10) [TRUNCATED]
        - recent_metrics: [...]  (last 10) [FULL CONTENT]
        - recent_notes: [...]  (last 5) [TRUNCATED]

    Workflow:
        # 1. Get overview (lightweight, truncated)
        overview = get_overview()  # or get_overview(truncate_length=150) for more preview

        # 2. Scan keys and truncated content
        # knowledge[0] = {"key": "knee-health-best-practices", "content": "Knee Health Best Practices:\n\nALIGNMENT & TRACKING:\n- Knees track over toes (prevent valgus coll..."}

        # 3. Fetch full details for relevant items
        details = get_items_detail([
            {"kind": "knowledge", "key": "knee-health-best-practices"},
            {"kind": "principle", "key": "progressive-overload"}
        ])
        # Now details[0]['content'] has complete text

        # 4. Or use list_items/search_entries for targeted queries
        knee_knowledge = search_entries(query="knee pain", kind="knowledge", limit=3)
    """
    user_id = _get_user_id()
    with get_session() as session:
        result = crud.get_overview(session, user_id, truncate_length=truncate_length)
        today = date.today()
        result['current_date'] = today.isoformat()
        result['current_day'] = today.strftime('%A')
        return result


@mcp.tool
def get_current_date() -> dict:
    """Get the current date with day of week.

    Use this when you need the current date for creating timestamps, filtering events,
    or calculating time-based metrics. This is the canonical source of the current date.

    Returns:
        Dictionary with:
        - date: ISO date string (YYYY-MM-DD)
        - day: Day of week (e.g., 'Monday', 'Tuesday')

    Example:
        today = get_current_date()
        # Use in log_event
        log_event(kind='workout', content='Morning run', occurred_at=f"{today['date']}T07:00:00Z")
    """
    today = date.today()
    return {
        'date': today.isoformat(),
        'day': today.strftime('%A')
    }


@mcp.tool
def describe_conventions() -> dict:
    """Get metadata about allowed kinds, key formats, date formats, and attribute conventions.

    Use this to understand the schema, validation rules, and recommended patterns for this server.
    Helpful for understanding what values are valid for kinds, how to format keys, and what
    attributes are recommended for each kind.

    Returns:
        Dictionary containing:
        - kinds: List of all allowed kind values
        - key_regex: Pattern that keys must match
        - date_formats: Expected date and datetime formats
        - defaults: Default values (limit, priority range)
        - attrs_hints: Recommended attributes for each kind
        - examples: Example usage for main tools

    Example:
        describe_conventions()
    """
    kinds = ['goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout','workout-plan','metric','note']
    developer_kinds = ['issue']
    return {
        'kinds': kinds,
        'developer_kinds': developer_kinds,
        'key_regex': '^[a-z0-9-]{1,64}$',
        'date_formats': {
            'date': 'YYYY-MM-DD',
            'datetime': 'YYYY-MM-DDTHH:MM:SS[.ffffff][Z]'
        },
        'defaults': {
            'limit': 100,
            'priority_range': [1, 5],
        },
        'attrs_standards': {
            'goal': {
                'description': 'Progress tracking enabled with baseline and target',
                'required': ['baseline', 'target'],
                'schema': {
                    'baseline': {'value': 'string or number', 'date': 'YYYY-MM-DD', 'notes': 'string (optional)'},
                    'target': {'value': 'string or number', 'date': 'YYYY-MM-DD'}
                },
                'example': {'baseline': {'value': '185lbs', 'date': '2025-09-01'}, 'target': {'value': '225lbs', 'date': '2026-03-01'}}
            },
            'plan': {
                'description': 'Temporal context (current week, progress %) enabled with start_date and duration_weeks',
                'recommended': ['start_date', 'duration_weeks'],
                'schema': {
                    'start_date': 'YYYY-MM-DD (enables temporal context)',
                    'duration_weeks': 'number (enables temporal context)',
                    'deload_week': 'number (optional)',
                    'focus': 'string (optional)'
                },
                'example': {'start_date': '2025-10-01', 'duration_weeks': 6, 'deload_week': 4, 'focus': 'hypertrophy'}
            },
            'plan-step': {
                'description': 'Weekly training prescriptions',
                'recommended': ['week', 'volume_target', 'intensity_target'],
                'schema': {
                    'week': 'number (week number in plan)',
                    'volume_target': 'string or number',
                    'intensity_target': 'string or number',
                    'notes': 'string (optional)'
                },
                'example': {'week': 3, 'volume_target': '25km', 'intensity_target': 'RPE 7-8'}
            },
            'workout': {
                'description': 'Logged training sessions - put rich data in attrs',
                'recommended': ['exercises', 'duration_min', 'rpe'],
                'schema': {
                    'exercises': 'array of {name, sets, reps, weight, rpe} objects',
                    'duration_min': 'number',
                    'rpe': 'number (1-10)',
                    'distance_km': 'number (for cardio)',
                    'avg_hr': 'number (for cardio)',
                    'notes': 'string (optional)'
                },
                'example': {
                    'exercises': [{'name': 'Squat', 'sets': 5, 'reps': 5, 'weight_lbs': 245, 'rpe': 8}],
                    'duration_min': 45,
                    'rpe': 8,
                    'notes': 'Felt strong today'
                }
            },
            'current': {
                'description': 'Current state metrics',
                'recommended': ['numeric_value', 'unit', 'tested_date'],
                'schema': {
                    'numeric_value': 'number',
                    'unit': 'string',
                    'tested_date': 'YYYY-MM-DD (optional)'
                },
                'example': {'numeric_value': 180.5, 'unit': 'lbs', 'tested_date': '2025-10-09'}
            },
            'knowledge': {
                'description': 'User-specific observations and contraindications',
                'optional': ['affected_exercises', 'safe_alternatives', 'retest_date', 'severity'],
                'schema': {
                    'affected_exercises': 'array of strings (for contraindications)',
                    'safe_alternatives': 'array of strings (for contraindications)',
                    'retest_date': 'YYYY-MM-DD (for injury tracking)',
                    'severity': 'string (for contraindications)',
                    'source': 'string (optional - book, coach, etc.)'
                },
                'example': {'affected_exercises': ['squat', 'lunge'], 'safe_alternatives': ['leg press', 'step-ups'], 'severity': 'moderate'}
            },
            'preference': {
                'description': 'User preferences - keep attrs minimal, details in content',
                'optional': ['priority_level'],
                'example': {'priority_level': 'high'}
            },
            'metric': {
                'description': 'Measurements and assessments',
                'recommended': ['value', 'unit'],
                'schema': {
                    'value': 'number',
                    'unit': 'string',
                    'context': 'string (optional - e.g., "morning weigh-in")'
                },
                'example': {'value': 180.5, 'unit': 'lbs', 'context': 'morning weigh-in'}
            }
        },
        'attrs_principles': {
            'use_for_structured_data': 'Numbers, dates, arrays - data that needs programmatic access',
            'use_content_for_rich_text': 'Narratives, explanations, detailed instructions go in content field',
            'keep_simple': 'Flat structures preferred - avoid deep nesting',
            'merge_on_display': 'Overview merges attrs into main dict for easy access',
            'examples_of_good_attrs': [
                {'target_weight_kg': 100, 'current_weight_kg': 90},  # Good: simple numbers
                {'exercises': [{'name': 'Squat', 'sets': 5}]},  # Good: structured array
                {'start_date': '2025-10-01', 'duration_weeks': 6}  # Good: enables temporal features
            ],
            'examples_of_bad_attrs': [
                {'description': 'Long narrative text that should be in content field instead...'},  # Bad: rich text in attrs
                {'config': {'nested': {'deeply': {'bad': 'value'}}}},  # Bad: deep nesting
                {'stringified_json': '{"key": "value"}'}  # Bad: stringified JSON
            ]
        },
        'temporal_context': {
            'description': 'Plans with start_date and duration_weeks in attrs will show computed temporal context in overview',
            'computed_fields': ['current_week', 'total_weeks', 'weeks_remaining', 'progress_pct', 'temporal_status'],
            'example': 'If plan has start_date="2025-09-15" and duration_weeks=5, overview shows current_week=3, progress_pct=60, etc.'
        },
        'progress_tracking': {
            'description': 'Goals with baseline and target in attrs enable progress tracking',
            'baseline_format': {'value': 'starting performance', 'date': 'when established'},
            'target_format': {'value': 'goal performance', 'date': 'target date'},
            'current_progress': 'Derived from recent workout/metric logs, not stored in goal attrs'
        },
        'contraindications': {
            'description': 'Use tags and attrs for injury/limitation tracking',
            'required_tag': 'contraindication',
            'status_tags': ['injury-active', 'injury-resolved'],
            'recommended_attrs': ['affected_exercises (array)', 'safe_alternatives (array)', 'retest_date', 'severity']
        },
        'notes': {
            'issue_kind': 'Developer-only kind for tracking backend issues. Excluded from get_overview() and general fitness workflows. Use report_issue() and list_issues() tools.'
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
        logfire.info('starting fitness memory mcp server', tools=['upsert_item','get_item','delete_item','archive_items','list_items','log_event','list_events','update_event','delete_event','search_entries','report_issue','list_issues','get_overview','get_current_date','get_started','describe_conventions'])
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
