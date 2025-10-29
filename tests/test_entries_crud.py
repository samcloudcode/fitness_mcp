"""Tests for basic CRUD operations on entries."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Tuple

import pytest
from sqlalchemy.orm import Session

from src.memory.crud import (
    upsert_item,
    get_item,
    get_items_by_keys,
    list_items,
    delete_item,
    log_event,
    list_events,
    search_entries,
)


def test_upsert_item_create(session_and_user: Tuple[Session, str]):
    """Test creating a new item with upsert."""
    session, user_id = session_and_user

    result = upsert_item(
        session, user_id,
        kind='goal',
        key='bench-225',
        content='Bench 225x5 by June. Priority: High.'
    )

    assert result['kind'] == 'goal'
    assert result['key'] == 'bench-225'
    assert 'Bench 225x5' in result['content']
    assert result['status'] == 'active'
    assert 'id' in result
    assert 'created_at' in result


def test_upsert_item_update(session_and_user: Tuple[Session, str]):
    """Test updating an existing item with upsert (same key)."""
    session, user_id = session_and_user

    # Create initial item
    result1 = upsert_item(
        session, user_id,
        kind='goal',
        key='bench-225',
        content='Bench 225x5 by June.'
    )
    created_at = result1['created_at']
    item_id = result1['id']

    # Update same item
    result2 = upsert_item(
        session, user_id,
        kind='goal',
        key='bench-225',
        content='Bench 225x5 by March. Priority: High.'
    )

    # Should be same ID
    assert result2['id'] == item_id
    # Created_at should not change
    assert result2['created_at'] == created_at
    # Content should be updated
    assert 'March' in result2['content']
    assert 'Priority: High' in result2['content']
    # Updated_at should be newer
    assert result2['updated_at'] > result2['created_at']


def test_upsert_item_rename(session_and_user: Tuple[Session, str]):
    """Test renaming an item with old_key parameter."""
    session, user_id = session_and_user

    # Create initial item
    upsert_item(
        session, user_id,
        kind='goal',
        key='bench-old',
        content='Bench 225x5.'
    )

    # Rename to new key
    result = upsert_item(
        session, user_id,
        kind='goal',
        key='bench-225',
        old_key='bench-old',
        content='Bench 225x5 by June.'
    )

    assert result['key'] == 'bench-225'
    assert 'June' in result['content']

    # Old key should no longer exist
    old_item = get_item(session, user_id, kind='goal', key='bench-old')
    assert old_item is None


def test_get_item(session_and_user: Tuple[Session, str]):
    """Test retrieving a specific item by kind and key."""
    session, user_id = session_and_user

    # Create item
    upsert_item(
        session, user_id,
        kind='knowledge',
        key='knee-health',
        content='Wider stance eliminates pain.'
    )

    # Get item
    result = get_item(session, user_id, kind='knowledge', key='knee-health')

    assert result is not None
    assert result['key'] == 'knee-health'
    assert 'Wider stance' in result['content']


def test_get_item_not_found(session_and_user: Tuple[Session, str]):
    """Test getting non-existent item returns None."""
    session, user_id = session_and_user

    result = get_item(session, user_id, kind='goal', key='nonexistent')

    assert result is None


def test_get_items_by_keys(session_and_user: Tuple[Session, str]):
    """Test retrieving multiple items by keys."""
    session, user_id = session_and_user

    # Create multiple items
    upsert_item(session, user_id, kind='goal', key='bench-225', content='Bench goal')
    upsert_item(session, user_id, kind='goal', key='squat-315', content='Squat goal')
    upsert_item(session, user_id, kind='knowledge', key='knee-health', content='Knee info')

    # Get multiple items
    results = get_items_by_keys(
        session, user_id,
        keys=[
            ('goal', 'bench-225'),
            ('knowledge', 'knee-health'),
        ]
    )

    assert len(results) == 2
    keys = [r['key'] for r in results]
    assert 'bench-225' in keys
    assert 'knee-health' in keys


def test_list_items_by_kind(session_and_user: Tuple[Session, str]):
    """Test listing items filtered by kind."""
    session, user_id = session_and_user

    # Create items of different kinds
    upsert_item(session, user_id, kind='goal', key='bench-225', content='Bench')
    upsert_item(session, user_id, kind='goal', key='squat-315', content='Squat')
    upsert_item(session, user_id, kind='knowledge', key='knee-health', content='Knee')

    # List goals only
    results = list_items(session, user_id, kind='goal')

    assert len(results) == 2
    assert all(r['kind'] == 'goal' for r in results)


def test_list_items_by_status(session_and_user: Tuple[Session, str]):
    """Test listing items filtered by status."""
    session, user_id = session_and_user

    # Create active and archived items
    upsert_item(session, user_id, kind='goal', key='active-goal', content='Active', status='active')
    upsert_item(session, user_id, kind='goal', key='archived-goal', content='Archived', status='archived')

    # List active only
    results = list_items(session, user_id, kind='goal', status='active')

    assert len(results) == 1
    assert results[0]['key'] == 'active-goal'


def test_list_items_limit(session_and_user: Tuple[Session, str]):
    """Test limiting results."""
    session, user_id = session_and_user

    # Create 5 items
    for i in range(5):
        upsert_item(session, user_id, kind='goal', key=f'goal-{i}', content=f'Goal {i}')

    # List with limit of 3
    results = list_items(session, user_id, kind='goal', limit=3)

    assert len(results) == 3


def test_delete_item(session_and_user: Tuple[Session, str]):
    """Test deleting an item."""
    session, user_id = session_and_user

    # Create item
    upsert_item(session, user_id, kind='goal', key='temp-goal', content='Temp')

    # Delete item
    deleted = delete_item(session, user_id, kind='goal', key='temp-goal')

    assert deleted is True

    # Verify it's gone
    result = get_item(session, user_id, kind='goal', key='temp-goal')
    assert result is None


def test_delete_item_not_found(session_and_user: Tuple[Session, str]):
    """Test deleting non-existent item returns False."""
    session, user_id = session_and_user

    deleted = delete_item(session, user_id, kind='goal', key='nonexistent')

    assert deleted is False


def test_log_event(session_and_user: Tuple[Session, str]):
    """Test creating an event (no key)."""
    session, user_id = session_and_user

    occurred_at = datetime.now() - timedelta(hours=2)
    result = log_event(
        session, user_id,
        kind='log',
        content='Upper: Bench 5x5 @ 185, OHP 3x12.',
        occurred_at=occurred_at
    )

    assert result['kind'] == 'log'
    assert result['key'] is None  # Events have no key
    assert 'Bench 5x5' in result['content']
    assert 'occurred_at' in result
    assert 'id' in result


def test_log_event_default_occurred_at(session_and_user: Tuple[Session, str]):
    """Test log_event defaults to now() if occurred_at not provided."""
    session, user_id = session_and_user

    result = log_event(
        session, user_id,
        kind='log',
        content='Workout completed.'
    )

    assert result['occurred_at'] is not None
    # Should be very recent
    occurred = datetime.fromisoformat(result['occurred_at'].replace('Z', '+00:00'))
    assert (datetime.now() - occurred.replace(tzinfo=None)).total_seconds() < 30


def test_list_events(session_and_user: Tuple[Session, str]):
    """Test listing events with date filtering."""
    session, user_id = session_and_user

    base_date = datetime.now() - timedelta(days=10)

    # Create events over time
    for i in range(5):
        log_event(
            session, user_id,
            kind='log',
            content=f'Workout {i}',
            occurred_at=base_date + timedelta(days=i*2)
        )

    # List all logs
    results = list_events(session, user_id, kind='log')

    assert len(results) == 5
    # Should be sorted by occurred_at descending (most recent first)
    assert 'Workout 4' in results[0]['content']


def test_list_events_date_filter(session_and_user: Tuple[Session, str]):
    """Test listing events with start/end date filters."""
    session, user_id = session_and_user

    base_date = datetime.now() - timedelta(days=10)

    # Create events
    for i in range(5):
        log_event(
            session, user_id,
            kind='log',
            content=f'Workout {i}',
            occurred_at=base_date + timedelta(days=i*2)
        )

    # Filter by date range
    start_date = base_date + timedelta(days=2)
    end_date = base_date + timedelta(days=6)

    results = list_events(
        session, user_id,
        kind='log',
        start=start_date,
        end=end_date
    )

    # Should only get workouts 1, 2, 3 (days 2, 4, 6)
    assert len(results) == 3


def test_search_entries(session_and_user: Tuple[Session, str]):
    """Test full-text search across entries."""
    session, user_id = session_and_user

    # Create items with searchable content
    upsert_item(session, user_id, kind='knowledge', key='knee-health', content='Wider stance eliminates knee pain.')
    upsert_item(session, user_id, kind='knowledge', key='shoulder-issue', content='Avoid dips due to shoulder pain.')
    upsert_item(session, user_id, kind='goal', key='bench-225', content='Bench 225x5.')

    # Search for "pain"
    results = search_entries(session, user_id, query='pain')

    assert len(results) == 2
    keys = [r['key'] for r in results]
    assert 'knee-health' in keys
    assert 'shoulder-issue' in keys
    assert 'bench-225' not in keys


def test_search_entries_by_kind(session_and_user: Tuple[Session, str]):
    """Test searching within specific kind."""
    session, user_id = session_and_user

    # Create items
    upsert_item(session, user_id, kind='knowledge', key='knee-health', content='Knee pain wider stance.')
    upsert_item(session, user_id, kind='goal', key='mobility', content='Pain-free squat.')

    # Search only in knowledge
    results = search_entries(session, user_id, query='pain', kind='knowledge')

    assert len(results) == 1
    assert results[0]['key'] == 'knee-health'


def test_search_entries_by_status(session_and_user: Tuple[Session, str]):
    """Test searching with status filter."""
    session, user_id = session_and_user

    # Create active and archived
    upsert_item(session, user_id, kind='goal', key='active-goal', content='Active bench goal', status='active')
    upsert_item(session, user_id, kind='goal', key='archived-goal', content='Old bench goal', status='archived')

    # Search includes both active and archived
    results = search_entries(session, user_id, query='bench')

    assert len(results) == 2
    keys = [r['key'] for r in results]
    assert 'active-goal' in keys
    assert 'archived-goal' in keys


def test_search_entries_no_results(session_and_user: Tuple[Session, str]):
    """Test search with no matching results."""
    session, user_id = session_and_user

    upsert_item(session, user_id, kind='goal', key='bench-225', content='Bench 225x5.')

    results = search_entries(session, user_id, query='nonexistent')

    assert len(results) == 0


def test_upsert_different_users_isolated(session_and_user: Tuple[Session, str]):
    """Test that different users' data is isolated."""
    session, user_id = session_and_user

    # Create item for user1
    upsert_item(session, user_id, kind='goal', key='bench-225', content='User 1 goal')

    # Create item for different user
    other_user_id = f'{user_id}-other'
    upsert_item(session, other_user_id, kind='goal', key='bench-225', content='User 2 goal')

    # Each user should only see their own data
    result1 = get_item(session, user_id, kind='goal', key='bench-225')
    result2 = get_item(session, other_user_id, kind='goal', key='bench-225')

    assert 'User 1' in result1['content']
    assert 'User 2' in result2['content']

    # Clean up other user
    from sqlalchemy import delete
    from src.memory.db import Entry
    session.execute(delete(Entry).where(Entry.user_id == other_user_id))
    session.commit()
