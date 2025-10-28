"""Tests for get_overview with context filtering."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Tuple

import pytest
from sqlalchemy.orm import Session

from src.memory.crud import get_overview, upsert_item, log_event


@pytest.fixture
def sample_data(session_and_user: Tuple[Session, str]) -> Tuple[Session, str]:
    """Create sample data for overview testing."""
    session, user_id = session_and_user

    # Create goals with different priorities
    upsert_item(
        session, user_id,
        kind='goal', key='bench-225',
        content='Bench 225x5 by June. Priority: High. Why: Rugby strength.'
    )
    upsert_item(
        session, user_id,
        kind='goal', key='run-sub20',
        content='5K under 20min. Priority: Low. Why: General fitness.'
    )
    upsert_item(
        session, user_id,
        kind='goal', key='squat-315',
        content='Squat 315x5. Priority: Medium. Why: Lower body strength.'
    )
    upsert_item(
        session, user_id,
        kind='goal', key='mobility',
        content='Full ATG squat. Why: Hip health.'  # No priority
    )

    # Create program
    upsert_item(
        session, user_id,
        kind='program', key='current-program',
        content='As of Oct 2025: Strength 4x/week, running 3x/week. Why: Rugby season April.'
    )

    # Create week
    upsert_item(
        session, user_id,
        kind='week', key='2025-week-43',
        content='Mon: Upper. Tue: Run. Wed: Lower. Thu: OFF. Fri: Upper. Sat: Run. Sun: Long run.'
    )

    # Create 7 plans (more than limit of 5)
    for i in range(7):
        day = 20 + i
        upsert_item(
            session, user_id,
            kind='plan', key=f'2025-10-{day:02d}-upper',
            content=f'Day {i+1}: Bench, OHP, rows.'
        )

    # Create preferences
    upsert_item(
        session, user_id,
        kind='preference', key='training-style',
        content='Morning 6am, upper/lower split. Why: Energy best AM.'
    )
    upsert_item(
        session, user_id,
        kind='preference', key='equipment',
        content='Home gym: barbell, rack, dumbbells. No leg press.'
    )

    # Create knowledge
    upsert_item(
        session, user_id,
        kind='knowledge', key='knee-health',
        content='Wider stance eliminates pain. Why: Activates glute med.'
    )
    upsert_item(
        session, user_id,
        kind='knowledge', key='shoulder-issue',
        content='Avoid dips. Why: Anterior shoulder pain.'
    )

    # Create 12 logs (more than limit of 10)
    base_date = datetime.now() - timedelta(days=20)
    for i in range(12):
        log_event(
            session, user_id,
            kind='log',
            content=f'Workout {i+1}: Squats, bench, rows.',
            occurred_at=base_date + timedelta(days=i*2)
        )

    # Create metrics
    for i in range(5):
        log_event(
            session, user_id,
            kind='metric',
            content=f'Weight: {70 + i}kg',
            occurred_at=base_date + timedelta(days=i*5)
        )

    # Create note
    log_event(
        session, user_id,
        kind='note',
        content='Knee felt tight during warmup.',
        occurred_at=datetime.now()
    )

    return session, user_id


def test_overview_planning_context(sample_data: Tuple[Session, str]):
    """Test planning context returns correct data with limits."""
    session, user_id = sample_data

    overview = get_overview(session, user_id, context='planning')

    # Should include goals
    assert 'goals' in overview
    assert 'active' in overview['goals']
    goals = overview['goals']['active']
    assert len(goals) == 4

    # Goals should be priority sorted (High, Medium, Low, None)
    assert 'bench-225' in goals[0]['key']  # High priority first
    assert 'squat-315' in goals[1]['key']  # Medium second
    assert 'run-sub20' in goals[2]['key']  # Low third
    assert 'mobility' in goals[3]['key']   # No priority last

    # Should include program
    assert 'program' in overview
    assert len(overview['program']) == 1
    assert overview['program'][0]['key'] == 'current-program'

    # Should include week
    assert 'week' in overview
    assert len(overview['week']) == 1
    assert overview['week'][0]['key'] == '2025-week-43'

    # Should include recent plans (limit 5)
    assert 'recent_plans' in overview
    assert len(overview['recent_plans']) == 5
    # Should be sorted by date descending (most recent first)
    assert overview['recent_plans'][0]['key'] == '2025-10-26-upper'
    assert overview['recent_plans'][4]['key'] == '2025-10-22-upper'

    # Should include all preferences
    assert 'preferences' in overview
    assert len(overview['preferences']) == 2

    # Should include all knowledge
    assert 'knowledge' in overview
    assert len(overview['knowledge']) == 2

    # Should include recent logs (limit 10)
    assert 'recent_logs' in overview
    assert len(overview['recent_logs']) == 10
    # Should be sorted by occurred_at descending (most recent first)
    # (can't check exact content without parsing, but count is correct)

    # Should NOT include metrics in planning context
    assert 'recent_metrics' not in overview


def test_overview_upcoming_context(sample_data: Tuple[Session, str]):
    """Test upcoming context returns limited subset."""
    session, user_id = sample_data

    overview = get_overview(session, user_id, context='upcoming')

    # Should include goals
    assert 'goals' in overview

    # Should include week
    assert 'week' in overview

    # Should include recent plans
    assert 'recent_plans' in overview
    assert len(overview['recent_plans']) == 5

    # Should include recent logs (limit 7 for upcoming)
    assert 'recent_logs' in overview
    assert len(overview['recent_logs']) == 7

    # Should NOT include program, preferences, knowledge, metrics
    assert 'program' not in overview
    assert 'preferences' not in overview
    assert 'knowledge' not in overview
    assert 'recent_metrics' not in overview


def test_overview_knowledge_context(sample_data: Tuple[Session, str]):
    """Test knowledge context returns constraints/preferences."""
    session, user_id = sample_data

    overview = get_overview(session, user_id, context='knowledge')

    # Should include goals, program, preferences, knowledge
    assert 'goals' in overview
    assert 'program' in overview
    assert 'preferences' in overview
    assert 'knowledge' in overview

    # Should NOT include plans, logs, metrics
    assert 'recent_plans' not in overview
    assert 'recent_logs' not in overview
    assert 'recent_metrics' not in overview


def test_overview_history_context(sample_data: Tuple[Session, str]):
    """Test history context returns all logs and metrics."""
    session, user_id = sample_data

    overview = get_overview(session, user_id, context='history')

    # Should include goals
    assert 'goals' in overview

    # Should include all logs (no limit, up to 500)
    assert 'recent_logs' in overview
    assert len(overview['recent_logs']) == 12  # All 12 logs

    # Should include metrics
    assert 'recent_metrics' in overview
    assert len(overview['recent_metrics']) == 5

    # Should NOT include program, week, plans, preferences, knowledge
    assert 'program' not in overview
    assert 'week' not in overview
    assert 'recent_plans' not in overview
    assert 'preferences' not in overview
    assert 'knowledge' not in overview


def test_overview_no_context(sample_data: Tuple[Session, str]):
    """Test default context returns everything."""
    session, user_id = sample_data

    overview = get_overview(session, user_id)

    # Should include everything
    assert 'goals' in overview
    assert 'program' in overview
    assert 'week' in overview
    assert 'preferences' in overview
    assert 'knowledge' in overview
    assert 'recent_metrics' in overview
    assert 'recent_notes' in overview

    # Plans and logs still limited by default
    assert 'recent_plans' in overview
    assert len(overview['recent_plans']) <= 5
    assert 'recent_logs' in overview
    assert len(overview['recent_logs']) <= 10


def test_overview_empty(session_and_user: Tuple[Session, str]):
    """Test overview with no data returns empty sections."""
    session, user_id = session_and_user

    overview = get_overview(session, user_id, context='planning')

    # Should return empty dict (no sections created when no data)
    assert overview == {}


def test_overview_truncation(session_and_user: Tuple[Session, str]):
    """Test content truncation for verbose kinds."""
    session, user_id = session_and_user

    # Create knowledge with long content
    long_content = ' '.join(['word'] * 300)  # 300 words
    upsert_item(
        session, user_id,
        kind='knowledge', key='test-long',
        content=long_content
    )

    overview = get_overview(session, user_id, truncate_words=50)

    assert 'knowledge' in overview
    assert len(overview['knowledge']) == 1

    # Content should be truncated
    returned_content = overview['knowledge'][0]['content']
    word_count = len(returned_content.split())
    assert word_count <= 55  # 50 + some buffer for truncation marker


def test_overview_excludes_archived(session_and_user: Tuple[Session, str]):
    """Test that archived entries are excluded from overview."""
    session, user_id = session_and_user

    # Create active and archived goals
    upsert_item(
        session, user_id,
        kind='goal', key='active-goal',
        content='Active goal. Priority: High.',
        status='active'
    )
    upsert_item(
        session, user_id,
        kind='goal', key='archived-goal',
        content='Archived goal. Priority: High.',
        status='archived'
    )

    overview = get_overview(session, user_id, context='planning')

    # Should only include active goal
    assert 'goals' in overview
    assert len(overview['goals']['active']) == 1
    assert overview['goals']['active'][0]['key'] == 'active-goal'
    assert 'archived' not in overview['goals']
