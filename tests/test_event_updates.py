"""Test event update and delete functionality"""
import pytest
from datetime import datetime, timezone
from src.memory import crud
from src.memory.db import SessionLocal


@pytest.fixture
def session():
    """Create a test database session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_update_event(session):
    """Test updating an existing event"""
    user_id = "test_user_update"

    # Create an event
    event = crud.log_event(
        session,
        user_id,
        kind='workout',
        content='Initial workout log',
        occurred_at=datetime(2025, 10, 5, 7, 0, 0, tzinfo=timezone.utc)
    )

    event_id = event['id']

    # Update the event
    updated = crud.update_event(
        session,
        user_id,
        event_id=event_id,
        content='Updated workout log with more details'
    )

    assert updated is not None
    assert updated['content'] == 'Updated workout log with more details'

    # Verify occurred_at wasn't changed (we didn't update it)
    assert updated['occurred_at'] == event['occurred_at']


def test_update_event_partial(session):
    """Test updating only some fields of an event"""
    user_id = "test_user_partial"

    # Create an event
    event = crud.log_event(
        session,
        user_id,
        kind='metric',
        content='Bodyweight: 180 lbs'
    )

    # Update content
    updated = crud.update_event(
        session,
        user_id,
        event_id=event['id'],
        content='Bodyweight: 180 lbs, 15% bodyfat'
    )

    assert updated['content'] == 'Bodyweight: 180 lbs, 15% bodyfat'


def test_update_nonexistent_event(session):
    """Test updating an event that doesn't exist"""
    user_id = "test_user_nonexistent"
    fake_id = "00000000-0000-0000-0000-000000000000"

    result = crud.update_event(
        session,
        user_id,
        event_id=fake_id,
        content='This should not work'
    )

    assert result is None


def test_delete_event(session):
    """Test deleting an event"""
    user_id = "test_user_delete"

    # Create an event
    event = crud.log_event(
        session,
        user_id,
        kind='note',
        content='Test note to delete'
    )

    event_id = event['id']

    # Delete it
    deleted = crud.delete_event(session, user_id, event_id=event_id)
    assert deleted is True

    # Verify it's gone
    events = crud.list_events(session, user_id, kind='note')
    assert not any(e['id'] == event_id for e in events)


def test_delete_nonexistent_event(session):
    """Test deleting an event that doesn't exist"""
    user_id = "test_user_delete_nonexistent"
    fake_id = "00000000-0000-0000-0000-000000000000"

    result = crud.delete_event(session, user_id, event_id=fake_id)
    assert result is False


def test_update_event_workflow(session):
    """Test a realistic workflow of logging and updating a workout"""
    user_id = "test_user_workflow"

    # User logs workout initially with basic info
    workout = crud.log_event(
        session,
        user_id,
        kind='workout',
        content='Lower body session',
        occurred_at=datetime(2025, 10, 5, 18, 30, 0, tzinfo=timezone.utc)
    )

    workout_id = workout['id']

    # User remembers the exercises
    workout = crud.update_event(
        session,
        user_id,
        event_id=workout_id,
        content='Lower body session: Squat 5x5 @ 245lbs RPE 8. Bar speed good.'
    )

    # Final verification
    assert 'Squat 5x5 @ 245lbs' in workout['content']
    assert 'RPE 8' in workout['content']
    assert 'Bar speed good' in workout['content']
