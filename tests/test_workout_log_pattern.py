"""Test the recommended workout logging pattern using upsert with date keys."""
import pytest
from datetime import datetime
from src.memory import crud
from tests.conftest import session_and_user


def test_workout_log_upsert_pattern(session_and_user):
    """Test using upsert() for workout logs with date-based keys."""
    session, user_id = session_and_user

    # First part of workout
    result1 = crud.upsert_item(
        session, user_id,
        kind='log',
        key='2025-10-29-upper',
        content='Upper: Bench 3x10 @ 185lbs'
    )

    assert result1['kind'] == 'log'
    assert result1['key'] == '2025-10-29-upper'
    assert 'Bench 3x10' in result1['content']
    first_id = result1['id']

    # Add more to same workout (should update, not create new)
    result2 = crud.upsert_item(
        session, user_id,
        kind='log',
        key='2025-10-29-upper',
        content='Upper: Bench 3x10 @ 185lbs, OHP 3x8 @ 115lbs, Pull-ups 4x8'
    )

    assert result2['id'] == first_id  # Same entry was updated
    assert 'Pull-ups' in result2['content']
    assert result2['key'] == '2025-10-29-upper'

    # Different workout on different day (should create new)
    result3 = crud.upsert_item(
        session, user_id,
        kind='log',
        key='2025-10-30-lower',
        content='Lower: Squats 5x5 @ 225lbs'
    )

    assert result3['id'] != first_id  # Different entry
    assert result3['key'] == '2025-10-30-lower'
    assert 'Squats' in result3['content']


def test_metrics_use_log_without_key(session_and_user):
    """Test that metrics still use log() without keys."""
    session, user_id = session_and_user

    # Log metrics without keys
    metric1 = crud.log_event(
        session, user_id,
        kind='metric',
        content='Weight: 71kg'
    )

    assert metric1['kind'] == 'metric'
    assert metric1['key'] is None  # No key for metrics

    metric2 = crud.log_event(
        session, user_id,
        kind='metric',
        content='Body fat: 9%'
    )

    assert metric2['id'] != metric1['id']  # Different entries
    assert metric2['key'] is None


def test_notes_use_log_without_key(session_and_user):
    """Test that notes use log() without keys."""
    session, user_id = session_and_user

    note = crud.log_event(
        session, user_id,
        kind='note',
        content='Knee felt tight during warmup'
    )

    assert note['kind'] == 'note'
    assert note['key'] is None  # No key for notes