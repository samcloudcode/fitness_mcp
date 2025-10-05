"""Tests for temporal context computation in plans."""
import pytest
from datetime import date, timedelta
from src.memory.crud import _compute_plan_temporal_context, get_overview
from src.memory.db import Entry


class TestTemporalContextComputation:
    """Test temporal context calculation for plans."""

    def test_active_plan_midway(self):
        """Test plan that's currently active and halfway through."""
        today = date(2025, 10, 5)
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={
                'start_date': '2025-09-15',  # 20 days ago (week 3)
                'duration_weeks': 6
            }
        )

        result = _compute_plan_temporal_context(plan, today)

        assert result['current_week'] == 3  # 20 days = week 3
        assert result['total_weeks'] == 6
        assert result['weeks_remaining'] == 4  # 6 - 3 + 1 = 4
        assert result['progress_pct'] == 50  # 3/6 * 100
        assert result['temporal_status'] == 'active'
        assert result['days_elapsed'] == 20

    def test_plan_just_started(self):
        """Test plan in first week."""
        today = date(2025, 10, 5)
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={
                'start_date': '2025-10-01',  # 4 days ago (week 1)
                'duration_weeks': 8
            }
        )

        result = _compute_plan_temporal_context(plan, today)

        assert result['current_week'] == 1
        assert result['total_weeks'] == 8
        assert result['weeks_remaining'] == 8
        assert result['progress_pct'] == 12  # 1/8 * 100 = 12.5, int = 12
        assert result['temporal_status'] == 'active'

    def test_plan_completed(self):
        """Test plan that has passed its duration."""
        today = date(2025, 10, 5)
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={
                'start_date': '2025-08-01',  # 65 days ago (week 10)
                'duration_weeks': 8
            }
        )

        result = _compute_plan_temporal_context(plan, today)

        assert result['current_week'] == 10  # 65 days = week 10
        assert result['total_weeks'] == 8
        assert result['weeks_remaining'] == 0
        assert result['progress_pct'] == 100  # Capped at 100
        assert result['temporal_status'] == 'completed'

    def test_plan_pending(self):
        """Test plan that hasn't started yet."""
        today = date(2025, 10, 5)
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={
                'start_date': '2025-10-15',  # 10 days in future
                'duration_weeks': 6
            }
        )

        result = _compute_plan_temporal_context(plan, today)

        assert result['current_week'] == 0  # Not started
        assert result['temporal_status'] == 'pending'

    def test_plan_without_temporal_attrs(self):
        """Test plan without start_date or duration_weeks."""
        today = date(2025, 10, 5)
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={'other_field': 'value'}
        )

        result = _compute_plan_temporal_context(plan, today)

        assert result == {}  # No temporal context

    def test_plan_with_only_start_date(self):
        """Test plan with start_date but no duration_weeks."""
        today = date(2025, 10, 5)
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={'start_date': '2025-09-15'}
        )

        result = _compute_plan_temporal_context(plan, today)

        assert result == {}  # Both fields required

    def test_plan_with_only_duration(self):
        """Test plan with duration_weeks but no start_date."""
        today = date(2025, 10, 5)
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={'duration_weeks': 6}
        )

        result = _compute_plan_temporal_context(plan, today)

        assert result == {}  # Both fields required

    def test_invalid_date_format(self):
        """Test plan with invalid date format."""
        today = date(2025, 10, 5)
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={
                'start_date': 'invalid-date',
                'duration_weeks': 6
            }
        )

        result = _compute_plan_temporal_context(plan, today)

        assert result == {}  # Returns empty on error

    def test_week_boundary_calculations(self):
        """Test that week boundaries are calculated correctly."""
        plan = Entry(
            kind='plan',
            key='test-plan',
            content='Test plan',
            attrs={
                'start_date': '2025-10-01',
                'duration_weeks': 4
            }
        )

        # Day 0 (start date)
        result = _compute_plan_temporal_context(plan, date(2025, 10, 1))
        assert result['current_week'] == 1

        # Day 6 (last day of week 1)
        result = _compute_plan_temporal_context(plan, date(2025, 10, 7))
        assert result['current_week'] == 1

        # Day 7 (first day of week 2)
        result = _compute_plan_temporal_context(plan, date(2025, 10, 8))
        assert result['current_week'] == 2

        # Day 13 (last day of week 2)
        result = _compute_plan_temporal_context(plan, date(2025, 10, 14))
        assert result['current_week'] == 2

        # Day 14 (first day of week 3)
        result = _compute_plan_temporal_context(plan, date(2025, 10, 15))
        assert result['current_week'] == 3


class TestOverviewTemporalIntegration:
    """Test temporal context integration in get_overview."""

    def test_overview_includes_temporal_context(self, session_and_user):
        """Test that overview includes computed temporal context for plans."""
        from src.memory.crud import upsert_item

        session, user_id = session_and_user
        today = date.today()
        start_date = (today - timedelta(days=14)).isoformat()  # 2 weeks ago

        # Create plan with temporal attrs
        upsert_item(
            session,
            user_id,
            kind='plan',
            key='temporal-test-plan',
            content='Test plan with temporal context',
            status='active',
            attrs={
                'start_date': start_date,
                'duration_weeks': 6
            }
        )

        # Get overview
        overview = get_overview(session, user_id)

        # Verify plan appears with temporal context
        assert 'plans' in overview
        assert 'active' in overview['plans']

        plan = next(p for p in overview['plans']['active'] if p['key'] == 'temporal-test-plan')

        # Check temporal fields are present
        assert 'current_week' in plan
        assert 'total_weeks' in plan
        assert 'weeks_remaining' in plan
        assert 'progress_pct' in plan
        assert 'temporal_status' in plan

        # Verify values
        assert plan['current_week'] == 3  # 14 days = week 3
        assert plan['total_weeks'] == 6
        assert plan['temporal_status'] == 'active'

    def test_overview_without_temporal_attrs(self, session_and_user):
        """Test that plans without temporal attrs work normally."""
        from src.memory.crud import upsert_item

        session, user_id = session_and_user

        # Create plan without temporal attrs
        upsert_item(
            session,
            user_id,
            kind='plan',
            key='normal-plan',
            content='Plan without temporal context',
            status='active',
            attrs={'other_field': 'value'}
        )

        # Get overview
        overview = get_overview(session, user_id)

        # Verify plan appears without temporal fields
        assert 'plans' in overview
        plan = next(p for p in overview['plans']['active'] if p['key'] == 'normal-plan')

        # Temporal fields should not be present
        assert 'current_week' not in plan
        assert 'total_weeks' not in plan
        assert 'temporal_status' not in plan
