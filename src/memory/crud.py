from sqlalchemy.orm import Session
from sqlalchemy import select, and_, update, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.sql import func
from typing import Optional, Any, Iterable
from .db import Entry
import uuid
import logfire
from datetime import datetime, date, timezone
import json
from collections import defaultdict


def _serialize(entry: Entry) -> dict:
    """Serialize entry to dict."""
    return {
        "id": str(entry.id),
        "user_id": entry.user_id,
        "kind": entry.kind,
        "key": entry.key,
        "content": entry.content,
        "status": entry.status or 'active',
        "occurred_at": entry.occurred_at.isoformat() if entry.occurred_at else None,
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
        "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
    }


def _format_timestamp(value: Optional[datetime]) -> Optional[str]:
    if not value:
        return None
    ts = value
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    else:
        ts = ts.astimezone(timezone.utc)
    has_seconds = bool(ts.second or ts.microsecond)
    fmt = "%Y-%m-%d %H:%M:%S" if has_seconds else "%Y-%m-%d %H:%M"
    return f"{ts.strftime(fmt)}Z"


def _short_ref(entry_id: uuid.UUID) -> str:
    return entry_id.hex[:8]


def _clean_entry(entry: Entry, *, for_overview: bool = False, truncate_content: int = 0, truncate_words: int = 0) -> dict[str, Any]:
    """Clean and format entry for output.

    Args:
        entry: The database entry to clean
        for_overview: Use minimal format for overview (drops timestamps, keeps only essential fields)
        truncate_content: If > 0, truncate content to this many characters (adds '...' if truncated)
        truncate_words: If > 0, truncate content to this many words (takes precedence over truncate_content)
    """
    if for_overview:
        # Minimal format for overview: just key and content
        content = entry.content
        truncated = False

        if truncate_words > 0:
            # Word-based truncation (more natural)
            words = content.split()
            if len(words) > truncate_words:
                content = ' '.join(words[:truncate_words])
                truncated = True
        elif truncate_content > 0 and len(content) > truncate_content:
            # Character-based truncation (fallback)
            content = content[:truncate_content].rstrip()
            truncated = True

        if truncated:
            content = content.rstrip() + "... [truncated - use get() for full content]"

        data: dict[str, Any] = {
            "key": entry.key,
            "content": content,
        }

        # Add status if not active
        if entry.status and entry.status != 'active':
            data["status"] = entry.status

        # For events without keys, don't include key field
        if entry.key is None:
            data.pop("key", None)
            data["occurred_at"] = _format_timestamp(entry.occurred_at)

        return {k: v for k, v in data.items() if v is not None and (not isinstance(v, str) or v.strip())}

    # Full format for other operations
    data: dict[str, Any] = {
        "kind": entry.kind,
        "key": entry.key,
        "content": entry.content,
        "status": entry.status or 'active',
        "occurred_at": _format_timestamp(entry.occurred_at),
        "created_at": _format_timestamp(entry.created_at),
        "updated_at": _format_timestamp(entry.updated_at),
    }

    if entry.key is None:
        data.pop("key", None)
        data["ref"] = _short_ref(entry.id)

    cleaned: dict[str, Any] = {}
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        cleaned[key] = value

    return cleaned


def _group_by_status(entries: list[Entry], *, default_key: str = "other") -> dict[str, list[Entry]]:
    groups: dict[str, list[Entry]] = defaultdict(list)
    for entry in entries:
        status = (entry.status or "").strip().lower()
        if status == "archived":
            continue
        if status in {"completed"}:
            status = "achieved"
        key = status or default_key
        groups[key].append(entry)
    return groups


def upsert_item(
    session: Session,
    user_id: str,
    *,
    kind: str,
    key: str,
    content: str,
    status: Optional[str] = None,
    old_key: Optional[str] = None,
) -> dict:
    """Upsert a durable keyed item by (user_id, kind, key). Everything goes in content.

    Args:
        old_key: If provided, attempts to rename an existing entry from old_key to key.
                If old_key doesn't exist, performs regular upsert with key.
                If both old_key and key exist, raises ValueError.
    """
    with logfire.span('upsert item', user_id=user_id, kind=kind, key=key, old_key=old_key):
        # Normalize status to binary
        if status is None:
            status = 'active'
        elif status not in ('active', 'archived'):
            status = 'archived' if status in ('archived', 'deleted', 'inactive') else 'active'

        # Handle rename case
        if old_key is not None and old_key != key:
            # Check if old entry exists
            old_entry = session.execute(
                select(Entry).where(and_(
                    Entry.user_id == user_id,
                    Entry.kind == kind,
                    Entry.key == old_key
                ))
            ).scalar_one_or_none()

            if old_entry:
                # Check if new key already exists (conflict)
                new_entry_exists = session.execute(
                    select(Entry).where(and_(
                        Entry.user_id == user_id,
                        Entry.kind == kind,
                        Entry.key == key
                    ))
                ).scalar_one_or_none()

                if new_entry_exists:
                    raise ValueError(f"Cannot rename: entry with key '{key}' already exists")

                # Rename: update the old entry with new key and content
                old_entry.key = key
                old_entry.content = content
                old_entry.status = status
                old_entry.updated_at = func.now()
                session.commit()
                session.refresh(old_entry)
                return _serialize(old_entry)
            # If old entry doesn't exist, fall through to regular upsert

        # Regular upsert (no rename or old_key doesn't exist)
        stmt = pg_insert(Entry).values(
            user_id=user_id,
            kind=kind,
            key=key,
            content=content,
            status=status,
        ).on_conflict_do_update(
            index_elements=[Entry.user_id, Entry.kind, Entry.key],
            set_={
                "content": content,
                "status": status,
                "updated_at": func.now(),
            },
        )

        session.execute(stmt)
        session.commit()
        entry = session.execute(
            select(Entry).where(and_(Entry.user_id == user_id, Entry.kind == kind, Entry.key == key))
        ).scalar_one()
        return _serialize(entry)


# bulk_upsert_items removed - use individual upsert calls instead
# The simplified architecture emphasizes clarity over batch optimization


def get_item(session: Session, user_id: str, *, kind: str, key: str) -> Optional[dict]:
    with logfire.span('get item', user_id=user_id, kind=kind, key=key):
        stmt = select(Entry).where(
            and_(Entry.user_id == user_id, Entry.kind == kind, Entry.key == key)
        )
        entry = session.execute(stmt).scalar_one_or_none()
        return _serialize(entry) if entry else None


def get_items_by_keys(
    session: Session,
    user_id: str,
    *,
    keys: list[tuple[str, str]],  # [(kind, key), ...]
) -> list[dict]:
    """Fetch full content for multiple items by their (kind, key) tuples."""
    with logfire.span('get items by keys', user_id=user_id, count=len(keys)):
        if not keys:
            return []

        # Build OR conditions for each (kind, key) pair
        conditions = [
            and_(Entry.kind == kind, Entry.key == key)
            for kind, key in keys
        ]

        stmt = select(Entry).where(
            and_(Entry.user_id == user_id, *conditions) if len(conditions) == 1
            else and_(Entry.user_id == user_id, *[c for c in [Entry.kind.in_([k[0] for k in keys]), Entry.key.in_([k[1] for k in keys])] if c is not None])
        )

        # Simpler approach: query all matching keys
        from sqlalchemy import or_
        or_conditions = [and_(Entry.kind == kind, Entry.key == key) for kind, key in keys]
        stmt = select(Entry).where(
            and_(Entry.user_id == user_id, or_(*or_conditions))
        )

        entries = session.execute(stmt).scalars().all()
        return [_serialize(e) for e in entries]


def delete_item(session: Session, user_id: str, *, kind: str, key: str) -> bool:
    with logfire.span('delete item', user_id=user_id, kind=kind, key=key):
        stmt = delete(Entry).where(
            and_(Entry.user_id == user_id, Entry.kind == kind, Entry.key == key)
        )
        res = session.execute(stmt)
        session.commit()
        return res.rowcount > 0


def list_items(
    session: Session,
    user_id: str,
    *,
    kind: str,
    status: Optional[str] = None,
    limit: int = 100,
) -> list[dict]:
    """List items of a given kind."""
    with logfire.span('list items', user_id=user_id, kind=kind):
        stmt = select(Entry).where(and_(Entry.user_id == user_id, Entry.kind == kind, Entry.key.isnot(None)))
        if status:
            stmt = stmt.where(Entry.status == status)

        # Sort by updated_at desc (most recent first)
        stmt = stmt.order_by(Entry.updated_at.desc().nulls_last(), Entry.created_at.desc()).limit(limit)
        results = session.execute(stmt).scalars().all()
        return [_serialize(e) for e in results]


def log_event(
    session: Session,
    user_id: str,
    *,
    kind: str,
    content: str,
    occurred_at: Optional[datetime] = None,
) -> dict:
    """Log a timestamped event. Everything goes in content."""
    with logfire.span('log event', user_id=user_id, kind=kind):
        entry = Entry(
            user_id=user_id,
            kind=kind,
            key=None,  # Events don't have keys
            content=content,
            status='active',  # Events are always active initially
            occurred_at=occurred_at,
        )
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return _serialize(entry)


def list_events(
    session: Session,
    user_id: str,
    *,
    kind: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = 100,
) -> list[dict]:
    """List timestamped events."""
    with logfire.span('list events', user_id=user_id):
        stmt = select(Entry).where(and_(Entry.user_id == user_id, Entry.key.is_(None)))
        if kind:
            stmt = stmt.where(Entry.kind == kind)
        if start:
            stmt = stmt.where(Entry.occurred_at >= start)
        if end:
            stmt = stmt.where(Entry.occurred_at <= end)
        stmt = stmt.order_by(Entry.occurred_at.desc().nulls_last(), Entry.created_at.desc()).limit(limit)
        results = session.execute(stmt).scalars().all()
        return [_serialize(e) for e in results]


def update_event(
    session: Session,
    user_id: str,
    *,
    event_id: str,
    content: Optional[str] = None,
    occurred_at: Optional[datetime] = None,
) -> Optional[dict]:
    """Update an existing event by ID. Only provided fields will be updated."""
    with logfire.span('update event', user_id=user_id, event_id=event_id):
        try:
            event_uuid = uuid.UUID(event_id)
        except ValueError:
            return None

        stmt = select(Entry).where(
            and_(Entry.user_id == user_id, Entry.id == event_uuid, Entry.key.is_(None))
        )
        entry = session.execute(stmt).scalar_one_or_none()

        if not entry:
            return None

        # Update fields
        if content is not None:
            entry.content = content
        if occurred_at is not None:
            entry.occurred_at = occurred_at

        entry.updated_at = func.now()
        session.commit()
        session.refresh(entry)
        return _serialize(entry)


def delete_event(
    session: Session,
    user_id: str,
    *,
    event_id: str,
) -> bool:
    """Delete an event by ID."""
    with logfire.span('delete event', user_id=user_id, event_id=event_id):
        try:
            event_uuid = uuid.UUID(event_id)
        except ValueError:
            return False

        stmt = delete(Entry).where(
            and_(Entry.user_id == user_id, Entry.id == event_uuid, Entry.key.is_(None))
        )
        res = session.execute(stmt)
        session.commit()
        return res.rowcount > 0


def search_entries(
    session: Session,
    user_id: str,
    *,
    query: str,
    kind: Optional[str] = None,
    limit: int = 100,
) -> list[dict]:
    with logfire.span('search entries in database', user_id=user_id, has_kind=kind is not None):
        stmt = select(Entry).where(Entry.user_id == user_id)
        if kind:
            stmt = stmt.where(Entry.kind == kind)
        if query:
            stmt = stmt.where(
                func.to_tsvector('english', func.concat(func.coalesce(Entry.key, ''), ' ', Entry.content)).bool_op('@@')(
                    func.plainto_tsquery('english', query)
                )
            )
        stmt = stmt.order_by(Entry.updated_at.desc().nulls_last(), Entry.created_at.desc()).limit(limit)
        results = session.execute(stmt).scalars().all()
        return [_serialize(e) for e in results]


# Temporal context removed - put date/week info directly in content


def get_overview(
    session: Session,
    user_id: str,
    truncate_words: int = 200,
    context: Optional[str] = None
) -> dict:
    """Return clean, organized overview with truncated content for scanning.

    Args:
        truncate_words: Max words for verbose content before truncation (default 200).
                       Use get() to fetch full content for specific items.
        context: Optional context for filtering relevant data:
                - 'planning': Goals (priority order), program, week, plans (recent 5/2wks), preferences, knowledge, logs (recent 10/2wks)
                - 'upcoming': Goals, week, plans, recent logs (1 week)
                - 'knowledge': Goals, program, preferences, knowledge
                - 'history': Goals, all logs, metrics (for progress review)
                - None: All data (default behavior)
    """
    with logfire.span('get overview', user_id=user_id, truncate_words=truncate_words, context=context):
        # Define context-based kind filters
        context_filters = {
            'planning': {'goal', 'program', 'week', 'plan', 'preference', 'knowledge', 'log'},
            'upcoming': {'goal', 'week', 'plan', 'log'},
            'knowledge': {'goal', 'program', 'preference', 'knowledge'},
            'history': {'goal', 'log', 'metric'},
        }

        # Exclude archived entries and issues from overview
        conditions = [
            Entry.user_id == user_id,
            Entry.kind != 'issue',
            Entry.status != 'archived'
        ]

        # Add context-based kind filtering
        if context and context in context_filters:
            conditions.append(Entry.kind.in_(context_filters[context]))

        stmt = select(Entry).where(and_(*conditions))
        entries = session.execute(stmt).scalars().all()

        by_kind: dict[str, list[Entry]] = defaultdict(list)
        for entry in entries:
            by_kind[entry.kind].append(entry)

        def _sorted(items: list[Entry]) -> list[Entry]:
            # Sort by updated_at descending (most recent first)
            # Priority is now in attrs and could be string or int, so skip it
            return sorted(
                items,
                key=lambda x: -(x.updated_at or x.created_at or datetime.min).timestamp(),
            )

        overview: dict[str, Any] = {}

        # Determine log limit based on context
        log_limit = 10  # default (10 logs or ~2 weeks)
        plan_limit = 5  # default (5 plans or ~2 weeks)
        if context == 'planning':
            log_limit = 10  # most recent 10 or ~2 weeks
            plan_limit = 5  # most recent 5 or ~2 weeks
        elif context == 'upcoming':
            log_limit = 7   # ~1 week
            plan_limit = 5  # ~1 week
        elif context == 'history':
            log_limit = 500  # All history (large limit)
            plan_limit = 500  # All history

        # Strategies (long-term and short-term) - TRUNCATED
        strategies = by_kind.get("strategy", [])
        if strategies:
            key_map = {(s.key or "").lower(): s for s in strategies}
            long_term = key_map.get("long_term") or key_map.get("long-term")
            short_term = key_map.get("short_term") or key_map.get("short-term")

            strategy_section: dict[str, Any] = {}
            if long_term:
                strategy_section["long_term"] = _clean_entry(long_term, for_overview=True, truncate_words=truncate_words)
            if short_term:
                strategy_section["short_term"] = _clean_entry(short_term, for_overview=True, truncate_words=truncate_words)

            if strategy_section:
                overview["strategies"] = strategy_section

        # Goals (grouped by status) - full content, ordered by priority
        goals = by_kind.get("goal", [])
        if goals:
            def _priority_sort_key(item: Entry) -> tuple:
                # Extract priority from content (High > Medium > Low > none)
                content_lower = (item.content or "").lower()
                if "priority: high" in content_lower or "priority:high" in content_lower:
                    priority_rank = 0
                elif "priority: medium" in content_lower or "priority:medium" in content_lower:
                    priority_rank = 1
                elif "priority: low" in content_lower or "priority:low" in content_lower:
                    priority_rank = 2
                else:
                    priority_rank = 3  # No priority specified
                # Secondary sort by updated_at (recent first)
                timestamp = -(item.updated_at or item.created_at or datetime.min).timestamp()
                return (priority_rank, timestamp)

            goal_groups = _group_by_status(goals, default_key="active")
            goals_section: dict[str, list[dict[str, Any]]] = {}
            for status, items in goal_groups.items():
                sorted_items = sorted(items, key=_priority_sort_key)
                cleaned = [_clean_entry(item, for_overview=True) for item in sorted_items]
                if cleaned:
                    goals_section[status] = cleaned
            if goals_section:
                overview["goals"] = goals_section

        # Plans - recent plans only, sorted by date (recent first)
        plans = by_kind.get("plan", [])
        if plans:
            # Sort by key (which contains date YYYY-MM-DD) descending (recent first)
            recent_plans = sorted(
                plans,
                key=lambda item: item.key or "",
                reverse=True,
            )[:plan_limit]
            overview["recent_plans"] = [_clean_entry(item, for_overview=True) for item in recent_plans]

        # Current state (simple list) - full content
        current = by_kind.get("current", [])
        if current:
            overview["current"] = [_clean_entry(item, for_overview=True) for item in _sorted(current)]

        # Program (current program) - TRUNCATED
        programs = by_kind.get("program", [])
        if programs:
            overview["program"] = [_clean_entry(item, for_overview=True, truncate_words=truncate_words) for item in _sorted(programs)]

        # Week (current week plan) - full content
        weeks = by_kind.get("week", [])
        if weeks:
            overview["week"] = [_clean_entry(item, for_overview=True) for item in _sorted(weeks)]

        # Preferences (simple list) - TRUNCATED
        preferences = by_kind.get("preference", [])
        if preferences:
            overview["preferences"] = [_clean_entry(item, for_overview=True, truncate_words=truncate_words) for item in _sorted(preferences)]

        # Knowledge (simple list) - TRUNCATED
        knowledge = by_kind.get("knowledge", [])
        if knowledge:
            overview["knowledge"] = [_clean_entry(item, for_overview=True, truncate_words=truncate_words) for item in _sorted(knowledge)]

        # Principles (simple list) - TRUNCATED
        principles = by_kind.get("principle", [])
        if principles:
            overview["principles"] = [_clean_entry(item, for_overview=True, truncate_words=truncate_words) for item in _sorted(principles)]

        # Recent logs (context-aware limit) - TRUNCATED
        logs = by_kind.get("log", [])
        if logs:
            recent = sorted(
                logs,
                key=lambda item: (item.occurred_at or item.created_at or datetime.min),
                reverse=True,
            )[:log_limit]
            overview["recent_logs"] = [_clean_entry(item, for_overview=True, truncate_words=truncate_words) for item in recent]

        # Recent metrics - full content (already short)
        # Limit based on context: history mode shows all, default shows last 10
        metrics = by_kind.get("metric", [])
        if metrics:
            metric_limit = 500 if context == 'history' else 10
            recent = sorted(
                metrics,
                key=lambda item: (item.occurred_at or item.created_at or datetime.min),
                reverse=True,
            )[:metric_limit]
            overview["recent_metrics"] = [_clean_entry(item, for_overview=True) for item in recent]

        # Notes (last 5 only) - TRUNCATED
        notes = by_kind.get("note", [])
        if notes:
            recent = sorted(
                notes,
                key=lambda item: (item.occurred_at or item.created_at or datetime.min),
                reverse=True,
            )[:5]
            overview["recent_notes"] = [_clean_entry(item, for_overview=True, truncate_words=truncate_words) for item in recent]

        return overview
