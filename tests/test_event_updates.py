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
        occurred_at=datetime(2025, 10, 5, 7, 0, 0, tzinfo=timezone.utc),
        tags='test',
        attrs={'reps': 10, 'weight': 100}
    )

    event_id = event['id']

    # Update the event
    updated = crud.update_event(
        session,
        user_id,
        event_id=event_id,
        content='Updated workout log',
        tags='test,updated',
        attrs={'reps': 10, 'weight': 100, 'rpe': 8}
    )

    assert updated is not None
    assert updated['content'] == 'Updated workout log'
    assert updated['tags'] == 'test,updated'
    assert updated['attrs']['rpe'] == 8
    assert updated['attrs']['weight'] == 100

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
        content='Bodyweight: 180 lbs',
        attrs={'weight_lbs': 180}
    )

    # Update only attrs
    updated = crud.update_event(
        session,
        user_id,
        event_id=event['id'],
        attrs={'weight_lbs': 180, 'body_fat_pct': 15}
    )

    assert updated['content'] == 'Bodyweight: 180 lbs'  # Unchanged
    assert updated['attrs']['body_fat_pct'] == 15  # New field added


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
        occurred_at=datetime(2025, 10, 5, 18, 30, 0, tzinfo=timezone.utc),
        tags='strength,lower-body'
    )

    workout_id = workout['id']

    # User remembers the exercises
    workout = crud.update_event(
        session,
        user_id,
        event_id=workout_id,
        content='Lower body session: Squat 5x5@245lbs',
        attrs={'exercises': [{'name': 'Squat', 'sets': 5, 'reps': 5, 'weight_lbs': 245}]}
    )

    # User adds RPE later
    existing_attrs = workout['attrs']
    workout = crud.update_event(
        session,
        user_id,
        event_id=workout_id,
        attrs={
            **existing_attrs,
            'rpe': 8,
            'notes': 'Bar speed good'
        }
    )

    # Final verification
    assert workout['content'] == 'Lower body session: Squat 5x5@245lbs'
    assert workout['attrs']['rpe'] == 8
    assert workout['attrs']['notes'] == 'Bar speed good'
    assert workout['attrs']['exercises'][0]['weight_lbs'] == 245
