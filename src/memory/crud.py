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
    """Serialize entry to dict, with attrs data promoted to top level."""
    result = {
        "id": str(entry.id),
        "user_id": entry.user_id,
        "kind": entry.kind,
        "key": entry.key,
        "content": entry.content,
        "status": entry.status or 'active',
        "occurred_at": entry.occurred_at.isoformat() if entry.occurred_at else None,
        "attrs": entry.attrs or {},
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
        "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
    }

    # Extract common attrs fields to top level for compatibility
    attrs = entry.attrs or {}
    if 'priority' in attrs:
        result['priority'] = attrs['priority']
    if 'tags' in attrs:
        result['tags'] = attrs['tags'] if isinstance(attrs['tags'], str) else ','.join(attrs['tags'])
    if 'parent_key' in attrs:
        result['parent_key'] = attrs['parent_key']
    if 'due_date' in attrs:
        result['due_date'] = attrs['due_date']

    return result


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


def _clean_entry(entry: Entry, *, drop_parent: bool = False, for_overview: bool = False, truncate_content: int = 0) -> dict[str, Any]:
    """Clean and format entry for output.

    Args:
        entry: The database entry to clean
        drop_parent: Remove parent_key field
        for_overview: Use minimal format for overview (drops timestamps, keeps only essential fields)
        truncate_content: If > 0, truncate content to this many characters (adds '...' if truncated)
    """
    attrs = entry.attrs or {}

    if for_overview:
        # Minimal format for overview: just key and content (+ attrs merged in)
        content = entry.content
        if truncate_content > 0 and len(content) > truncate_content:
            content = content[:truncate_content].rstrip() + "..."

        data: dict[str, Any] = {
            "key": entry.key,
            "content": content,
        }

        # Add optional fields from attrs or direct fields
        if entry.status and entry.status != 'active':
            data["status"] = entry.status

        # Pull from attrs
        if 'priority' in attrs:
            data["priority"] = attrs['priority']
        if 'tags' in attrs:
            tags = attrs['tags']
            data["tags"] = tags if isinstance(tags, str) else ','.join(tags)
        if 'due_date' in attrs:
            data["due_date"] = attrs['due_date']
        if 'parent_key' in attrs and not drop_parent:
            data["parent_key"] = attrs['parent_key']

        # Merge other attrs into main dict
        for key, value in attrs.items():
            if key not in data and key not in ['priority', 'tags', 'due_date', 'parent_key']:
                data[key] = value

        # For events without keys, don't include key field at all
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

    # Extract common fields from attrs
    if 'priority' in attrs:
        data['priority'] = attrs['priority']
    if 'tags' in attrs:
        tags = attrs['tags']
        data['tags'] = tags if isinstance(tags, str) else ','.join(tags)
    if 'due_date' in attrs:
        data['due_date'] = attrs['due_date']
    if 'parent_key' in attrs:
        data['parent_key'] = attrs['parent_key']

    # Merge other attrs into main dict
    for key, value in attrs.items():
        if key not in data and key not in ['priority', 'tags', 'due_date', 'parent_key']:
            data[key] = value

    if drop_parent:
        data.pop("parent_key", None)

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
    priority: Optional[int | str] = None,
    status: Optional[str] = None,
    tags: Optional[str] = None,
    parent_key: Optional[str] = None,
    due_date: Optional[date | str] = None,
    attrs: Optional[dict[str, Any]] = None,
) -> dict:
    """Upsert a durable keyed item by (user_id, kind, key). Variable fields go in attrs."""
    with logfire.span('upsert item', user_id=user_id, kind=kind, key=key):
        # Build attrs dict with optional fields
        final_attrs = dict(attrs) if attrs else {}

        # Move optional fields to attrs
        if priority is not None:
            final_attrs['priority'] = priority
        if tags is not None:
            # Convert to list if CSV string
            if isinstance(tags, str) and ',' in tags:
                final_attrs['tags'] = [t.strip() for t in tags.split(',') if t.strip()]
            else:
                final_attrs['tags'] = tags
        if parent_key is not None:
            final_attrs['parent_key'] = parent_key
        if due_date is not None:
            final_attrs['due_date'] = due_date.isoformat() if hasattr(due_date, 'isoformat') else due_date

        # Simplify status to binary
        if status is None:
            status = 'active'
        elif status not in ('active', 'archived'):
            # Store original status in attrs and normalize
            final_attrs['original_status'] = status
            status = 'archived' if status in ('archived', 'deleted', 'inactive') else 'active'

        stmt = pg_insert(Entry).values(
            user_id=user_id,
            kind=kind,
            key=key,
            content=content,
            status=status,
            attrs=final_attrs,
        ).on_conflict_do_update(
            index_elements=[Entry.user_id, Entry.kind, Entry.key],
            set_={
                "content": content,
                "status": status,
                "attrs": final_attrs,
                "updated_at": func.now(),
            },
        )

        session.execute(stmt)
        session.commit()
        entry = session.execute(
            select(Entry).where(and_(Entry.user_id == user_id, Entry.kind == kind, Entry.key == key))
        ).scalar_one()
        return _serialize(entry)


def bulk_upsert_items(
    session: Session,
    user_id: str,
    items: Iterable[dict[str, Any]],
) -> list[dict]:
    """Upsert multiple keyed items in a single statement."""
    items = list(items)
    with logfire.span('bulk upsert items', user_id=user_id, count=len(items)):
        if not items:
            return []

        values: list[dict[str, Any]] = []
        for idx, item in enumerate(items):
            try:
                kind = item["kind"]
                key = item["key"]
                content = item["content"]
            except KeyError as exc:  # pragma: no cover - defensive
                missing = exc.args[0]
                raise ValueError(f"bulk upsert item at position {idx} missing required field '{missing}'") from exc

            values.append({
                "user_id": user_id,
                "kind": kind,
                "key": key,
                "parent_key": item.get("parent_key"),
                "content": content,
                "status": item.get("status"),
                "priority": item.get("priority"),
                "tags": item.get("tags"),
                "due_date": item.get("due_date"),
                "attrs": item.get("attrs") or {},
            })

        insert_stmt = pg_insert(Entry).values(values)
        update_cols = {
            "parent_key": insert_stmt.excluded.parent_key,
            "content": insert_stmt.excluded.content,
            "status": insert_stmt.excluded.status,
            "priority": insert_stmt.excluded.priority,
            "tags": insert_stmt.excluded.tags,
            "due_date": insert_stmt.excluded.due_date,
            "attrs": insert_stmt.excluded.attrs,
            "updated_at": func.now(),
        }

        stmt = insert_stmt.on_conflict_do_update(
            index_elements=[Entry.user_id, Entry.kind, Entry.key],
            set_=update_cols,
        ).returning(Entry)

        result = session.execute(stmt)
        session.commit()
        entries = result.scalars().all()
        return [_serialize(entry) for entry in entries]


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
    tag_contains: Optional[str] = None,
    parent_key: Optional[str] = None,
    limit: int = 100,
) -> list[dict]:
    with logfire.span('list items', user_id=user_id, kind=kind):
        stmt = select(Entry).where(and_(Entry.user_id == user_id, Entry.kind == kind, Entry.key.isnot(None)))
        if status:
            stmt = stmt.where(Entry.status == status)

        # Filter by parent_key in attrs
        if parent_key:
            stmt = stmt.where(Entry.attrs['parent_key'].astext == parent_key)

        # Filter by tags in attrs (could be array or string)
        if tag_contains:
            # Check both string tags and array tags in attrs
            from sqlalchemy import or_
            stmt = stmt.where(
                or_(
                    Entry.attrs['tags'].astext.ilike(f"%{tag_contains}%"),
                    Entry.attrs.op('?')('tags')  # Has tags key
                )
            )

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
    tags: Optional[str] = None,
    parent_key: Optional[str] = None,
    attrs: Optional[dict[str, Any] | str] = None,
) -> dict:
    with logfire.span('log event', user_id=user_id, kind=kind):
        # Build attrs dict with optional fields
        final_attrs = {}

        # Parse attrs if JSON string
        if attrs is not None:
            if isinstance(attrs, str):
                try:
                    final_attrs = json.loads(attrs)
                except json.JSONDecodeError:
                    logfire.warn('failed to parse attrs as JSON in log_event')
                    final_attrs = {'raw_attrs': attrs}
            else:
                final_attrs = dict(attrs)

        # Move optional fields to attrs
        if tags is not None:
            # Convert to list if CSV string
            if isinstance(tags, str) and ',' in tags:
                final_attrs['tags'] = [t.strip() for t in tags.split(',') if t.strip()]
            else:
                final_attrs['tags'] = tags
        if parent_key is not None:
            final_attrs['parent_key'] = parent_key

        entry = Entry(
            user_id=user_id,
            kind=kind,
            key=None,  # Events don't have keys
            content=content,
            status='active',  # Events are always active initially
            occurred_at=occurred_at,
            attrs=final_attrs,
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
    tag_contains: Optional[str] = None,
    parent_key: Optional[str] = None,
    limit: int = 100,
) -> list[dict]:
    with logfire.span('list events', user_id=user_id):
        stmt = select(Entry).where(and_(Entry.user_id == user_id, Entry.key.is_(None)))
        if kind:
            stmt = stmt.where(Entry.kind == kind)
        if start:
            stmt = stmt.where(Entry.occurred_at >= start)
        if end:
            stmt = stmt.where(Entry.occurred_at <= end)
        if parent_key:
            stmt = stmt.where(Entry.parent_key == parent_key)
        if tag_contains:
            stmt = stmt.where(Entry.tags.ilike(f"%{tag_contains}%"))
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
    tags: Optional[str] = None,
    parent_key: Optional[str] = None,
    attrs: Optional[dict[str, Any]] = None,
    replace_attrs: bool = False,
) -> Optional[dict]:
    """Update an existing event by ID. Only provided fields will be updated.

    Args:
        replace_attrs: If False (default), merges attrs with existing. If True, replaces entirely.
    """
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

        # Update only provided fields
        if content is not None:
            entry.content = content
        if occurred_at is not None:
            entry.occurred_at = occurred_at
        if tags is not None:
            entry.tags = tags
        if parent_key is not None:
            entry.parent_key = parent_key
        if attrs is not None:
            if replace_attrs:
                entry.attrs = attrs
            else:
                # Merge attrs by default (safer, consistent with upsert behavior)
                existing_attrs = entry.attrs or {}
                entry.attrs = {**existing_attrs, **attrs}

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


def _compute_plan_temporal_context(plan: Entry, today: date) -> dict[str, Any]:
    """Compute temporal context for a plan based on start_date and duration_weeks."""
    attrs = plan.attrs or {}
    start_date_str = attrs.get('start_date')
    duration_weeks = attrs.get('duration_weeks')

    if not start_date_str or not duration_weeks:
        return {}

    try:
        start_date = date.fromisoformat(start_date_str) if isinstance(start_date_str, str) else start_date_str
        duration_weeks = int(duration_weeks)

        # Calculate days into plan
        days_elapsed = (today - start_date).days

        # Week numbering: 0-6 days = week 1, 7-13 days = week 2, etc.
        current_week = (days_elapsed // 7) + 1 if days_elapsed >= 0 else 0

        # Calculate progress
        total_weeks = duration_weeks
        weeks_remaining = max(0, total_weeks - current_week + 1)
        progress_pct = min(100, int((current_week / total_weeks) * 100)) if total_weeks > 0 else 0

        # Determine status
        if current_week < 1:
            status = 'pending'
        elif current_week > total_weeks:
            status = 'completed'
        else:
            status = 'active'

        return {
            'current_week': current_week,
            'total_weeks': total_weeks,
            'weeks_remaining': weeks_remaining,
            'progress_pct': progress_pct,
            'days_elapsed': days_elapsed,
            'temporal_status': status,
        }
    except (ValueError, TypeError):
        return {}


def get_overview(session: Session, user_id: str, truncate_length: int = 100) -> dict:
    """Return clean, organized overview with truncated content for scanning.

    Args:
        truncate_length: Max chars for verbose content before truncation (default 100).
                        Use get_items_detail() to fetch full content for specific keys.
    """
    with logfire.span('get overview', user_id=user_id, truncate_length=truncate_length):
        stmt = select(Entry).where(and_(Entry.user_id == user_id, Entry.kind != 'issue'))
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

        # Truncate content for verbose kinds (knowledge, principle, preference)
        # Keep full content for concise kinds (goals, plans, current)
        TRUNCATE_KINDS = {'knowledge', 'principle', 'preference', 'plan-step'}
        TRUNCATE_LENGTH = truncate_length

        # Strategies (long-term and short-term)
        strategies = by_kind.get("strategy", [])
        if strategies:
            key_map = {(s.key or "").lower(): s for s in strategies}
            long_term = key_map.get("long_term") or key_map.get("long-term")
            short_term = key_map.get("short_term") or key_map.get("short-term")

            strategy_section: dict[str, Any] = {}
            if long_term:
                strategy_section["long_term"] = _clean_entry(long_term, for_overview=True, truncate_content=TRUNCATE_LENGTH)
            if short_term:
                strategy_section["short_term"] = _clean_entry(short_term, for_overview=True, truncate_content=TRUNCATE_LENGTH)

            if strategy_section:
                overview["strategies"] = strategy_section

        # Goals (grouped by status) - full content
        goals = by_kind.get("goal", [])
        if goals:
            goal_groups = _group_by_status(goals, default_key="active")
            goals_section: dict[str, list[dict[str, Any]]] = {}
            for status, items in goal_groups.items():
                cleaned = [_clean_entry(item, for_overview=True) for item in _sorted(items)]
                if cleaned:
                    goals_section[status] = cleaned
            if goals_section:
                overview["goals"] = goals_section

        # Plans (grouped by status, with nested steps and temporal context)
        plans = by_kind.get("plan", [])
        if plans:
            plan_groups = _group_by_status(plans, default_key="active")
            plans_section: dict[str, Any] = {}
            today = date.today()

            for status, items in plan_groups.items():
                cleaned_plans = []
                for plan in _sorted(items):
                    plan_data = _clean_entry(plan, for_overview=True)
                    # Add computed temporal context if plan has start_date and duration_weeks
                    temporal_ctx = _compute_plan_temporal_context(plan, today)
                    if temporal_ctx:
                        plan_data.update(temporal_ctx)
                    cleaned_plans.append(plan_data)
                if cleaned_plans:
                    plans_section[status] = cleaned_plans

            # Add plan steps nested by parent - TRUNCATED
            plan_steps = by_kind.get("plan-step", [])
            if plan_steps:
                steps_by_plan: dict[str, list[dict[str, Any]]] = defaultdict(list)
                for step in plan_steps:
                    # parent_key is now in attrs
                    parent_key = (step.attrs or {}).get('parent_key') if step.attrs else None
                    if not parent_key or (step.status or "").strip().lower() == "archived":
                        continue
                    steps_by_plan[parent_key].append(_clean_entry(step, drop_parent=True, for_overview=True, truncate_content=TRUNCATE_LENGTH))

                if steps_by_plan:
                    sorted_steps: dict[str, list[dict[str, Any]]] = {}
                    for parent_key, step_items in steps_by_plan.items():
                        # Sort by key only, since priority could be string or int
                        sorted_steps[parent_key] = sorted(
                            step_items,
                            key=lambda item: item.get("key", ""),
                        )
                    plans_section["steps"] = sorted_steps

            if plans_section:
                overview["plans"] = plans_section

        # Current state (simple list) - full content
        current = by_kind.get("current", [])
        if current:
            overview["current"] = [_clean_entry(item, for_overview=True) for item in _sorted(current)]

        # Preferences (simple list) - TRUNCATED
        preferences = by_kind.get("preference", [])
        if preferences:
            overview["preferences"] = [_clean_entry(item, for_overview=True, truncate_content=TRUNCATE_LENGTH) for item in _sorted(preferences)]

        # Knowledge (simple list) - TRUNCATED
        knowledge = by_kind.get("knowledge", [])
        if knowledge:
            overview["knowledge"] = [_clean_entry(item, for_overview=True, truncate_content=TRUNCATE_LENGTH) for item in _sorted(knowledge)]

        # Principles (simple list) - TRUNCATED
        principles = by_kind.get("principle", [])
        if principles:
            overview["principles"] = [_clean_entry(item, for_overview=True, truncate_content=TRUNCATE_LENGTH) for item in _sorted(principles)]

        # Recent workouts (last 10 only) - TRUNCATED
        workouts = by_kind.get("workout", [])
        if workouts:
            recent = sorted(
                workouts,
                key=lambda item: (item.occurred_at or item.created_at or datetime.min),
                reverse=True,
            )[:10]
            overview["recent_workouts"] = [_clean_entry(item, for_overview=True, truncate_content=TRUNCATE_LENGTH) for item in recent]

        # Recent metrics (last 10 only) - full content (already short)
        metrics = by_kind.get("metric", [])
        if metrics:
            recent = sorted(
                metrics,
                key=lambda item: (item.occurred_at or item.created_at or datetime.min),
                reverse=True,
            )[:10]
            overview["recent_metrics"] = [_clean_entry(item, for_overview=True) for item in recent]

        # Notes (last 5 only) - TRUNCATED
        notes = by_kind.get("note", [])
        if notes:
            recent = sorted(
                notes,
                key=lambda item: (item.occurred_at or item.created_at or datetime.min),
                reverse=True,
            )[:5]
            overview["recent_notes"] = [_clean_entry(item, for_overview=True, truncate_content=TRUNCATE_LENGTH) for item in recent]

        return overview
