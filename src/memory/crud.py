from sqlalchemy.orm import Session
from sqlalchemy import select, and_, update, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.sql import func
from typing import Optional, Any
from .db import Entry
import uuid
import logfire
from datetime import datetime, date, timezone
import json


def _serialize(entry: Entry) -> dict:
    return {
        "id": str(entry.id),
        "user_id": entry.user_id,
        "kind": entry.kind,
        "key": entry.key,
        "parent_key": entry.parent_key,
        "content": entry.content,
        "status": entry.status,
        "priority": entry.priority,
        "tags": entry.tags,
        "occurred_at": entry.occurred_at.isoformat() if entry.occurred_at else None,
        "due_date": entry.due_date.isoformat() if entry.due_date else None,
        "attrs": entry.attrs or {},
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
        "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
    }


def upsert_item(
    session: Session,
    user_id: str,
    *,
    kind: str,
    key: str,
    content: str,
    priority: Optional[int] = None,
    status: Optional[str] = None,
    tags: Optional[str] = None,
    parent_key: Optional[str] = None,
    due_date: Optional[date] = None,
    attrs: Optional[dict[str, Any]] = None,
) -> dict:
    """Upsert a durable keyed item by (user_id, kind, key)."""
    with logfire.span('upsert item', user_id=user_id, kind=kind, key=key):
        stmt = pg_insert(Entry).values(
            user_id=user_id,
            kind=kind,
            key=key,
            parent_key=parent_key,
            content=content,
            status=status,
            priority=priority,
            tags=tags,
            due_date=due_date,
            attrs=attrs or {},
        ).on_conflict_do_update(
            index_elements=[Entry.user_id, Entry.kind, Entry.key],
            set_={
                "parent_key": parent_key,
                "content": content,
                "status": status,
                "priority": priority,
                "tags": tags,
                "due_date": due_date,
                "attrs": attrs or {},
                "updated_at": func.now(),
            },
        )

        session.execute(stmt)
        session.commit()
        entry = session.execute(
            select(Entry).where(and_(Entry.user_id == user_id, Entry.kind == kind, Entry.key == key))
        ).scalar_one()
        return _serialize(entry)


def get_item(session: Session, user_id: str, *, kind: str, key: str) -> Optional[dict]:
    with logfire.span('get item', user_id=user_id, kind=kind, key=key):
        stmt = select(Entry).where(
            and_(Entry.user_id == user_id, Entry.kind == kind, Entry.key == key)
        )
        entry = session.execute(stmt).scalar_one_or_none()
        return _serialize(entry) if entry else None


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
        if parent_key:
            stmt = stmt.where(Entry.parent_key == parent_key)
        if tag_contains:
            stmt = stmt.where(Entry.tags.ilike(f"%{tag_contains}%"))
        stmt = stmt.order_by(Entry.priority.asc().nulls_last(), Entry.updated_at.desc().nulls_last(), Entry.created_at.desc()).limit(limit)
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
    attrs: Optional[dict[str, Any]] = None,
) -> dict:
    with logfire.span('log event', user_id=user_id, kind=kind):
        entry = Entry(
            user_id=user_id,
            kind=kind,
            key=None,
            parent_key=parent_key,
            content=content,
            status=None,
            priority=None,
            tags=tags,
            occurred_at=occurred_at,
            due_date=None,
            attrs=attrs or {},
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


def get_overview(session: Session, user_id: str) -> dict:
    """Return organized, LLM-friendly overview of all data for the user."""
    with logfire.span('get overview', user_id=user_id):
        stmt = select(Entry).where(Entry.user_id == user_id)
        entries = session.execute(stmt).scalars().all()

        by_kind: dict[str, list[Entry]] = {}
        for e in entries:
            by_kind.setdefault(e.kind, []).append(e)

        def _sorted(items: list[Entry]):
            return sorted(items, key=lambda x: (
                (x.priority if x.priority is not None else 99),
                (x.updated_at or x.created_at or datetime.min),
            ), reverse=True)

        # Goals grouped by status
        goals = by_kind.get('goal', [])
        goals_grouped = {
            'active': [_serialize(g) for g in _sorted([g for g in goals if (g.status or '').lower() == 'active'])],
            'paused': [_serialize(g) for g in _sorted([g for g in goals if (g.status or '').lower() == 'paused'])],
            'achieved': [_serialize(g) for g in _sorted([g for g in goals if (g.status or '').lower() in ('achieved','completed')])],
            'archived': [_serialize(g) for g in _sorted([g for g in goals if (g.status or '').lower() == 'archived'])],
            'all': [_serialize(g) for g in _sorted(goals)],
        }

        # Plans and steps
        plans = by_kind.get('plan', [])
        plan_steps = by_kind.get('plan-step', [])
        steps_by_plan: dict[str, list[dict]] = {}
        for s in plan_steps:
            if s.parent_key:
                steps_by_plan.setdefault(s.parent_key, []).append(_serialize(s))
        for k in steps_by_plan:
            steps_by_plan[k] = sorted(steps_by_plan[k], key=lambda x: (x.get('priority') or 99, x.get('key') or ''))

        strategies = by_kind.get('strategy', [])
        strategies_map = { (s.key or '').lower(): _serialize(s) for s in strategies }

        preferences = [_serialize(p) for p in _sorted(by_kind.get('preference', []))]
        knowledge = [_serialize(k) for k in _sorted(by_kind.get('knowledge', []))]
        principles = [_serialize(p) for p in _sorted(by_kind.get('principle', []))]
        current = [_serialize(c) for c in _sorted(by_kind.get('current', []))]

        workouts = by_kind.get('workout', [])
        recent_workouts = [_serialize(w) for w in sorted(workouts, key=lambda w: (w.occurred_at or w.created_at or datetime.min), reverse=True)[:25]]

        counts_by_kind = {k: len(v) for k, v in by_kind.items()}

        return {
            'user_id': user_id,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'counts_by_kind': counts_by_kind,
            'goals': goals_grouped,
            'plans': {
                'active': [_serialize(p) for p in _sorted([p for p in plans if (p.status or '').lower() == 'active'])],
                'archived': [_serialize(p) for p in _sorted([p for p in plans if (p.status or '').lower() == 'archived'])],
                'all': [_serialize(p) for p in _sorted(plans)],
                'steps_by_plan': steps_by_plan,
            },
            'strategies': {
                'short_term': strategies_map.get('short_term') or strategies_map.get('short-term'),
                'long_term': strategies_map.get('long_term') or strategies_map.get('long-term'),
                'all': [_serialize(s) for s in _sorted(strategies)],
            },
            'preferences': preferences,
            'knowledge': knowledge,
            'principles': principles,
            'current': current,
            'workouts': {
                'recent': recent_workouts
            },
            'others': {
                k: [_serialize(e) for e in _sorted(v)]
                for k, v in by_kind.items()
                if k not in {'goal','plan','plan-step','strategy','preference','knowledge','principle','current','workout'}
            }
        }
