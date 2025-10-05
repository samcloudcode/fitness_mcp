"""Unit-style tests for the Entry CRUD helpers."""

from __future__ import annotations

from datetime import datetime, timezone

from src.memory import crud


def test_upsert_get_list_delete(session_and_user) -> None:
    session, user_id = session_and_user

    created = crud.upsert_item(
        session,
        user_id,
        kind="knowledge",
        key="knee-health",
        content="Track knees over toes; progressive loading.",
        tags="mobility,knee",
    )

    assert created["user_id"] == user_id
    assert created["key"] == "knee-health"

    fetched = crud.get_item(session, user_id, kind="knowledge", key="knee-health")
    assert fetched is not None
    assert fetched["content"].startswith("Track knees")

    updated = crud.upsert_item(
        session,
        user_id,
        kind="knowledge",
        key="knee-health",
        content="Updated guidance",
        status="active",
        priority=2,
    )
    assert updated["content"] == "Updated guidance"
    assert updated["status"] == "active"

    items = crud.list_items(session, user_id, kind="knowledge")
    assert len(items) == 1
    assert items[0]["priority"] == 2

    deleted = crud.delete_item(session, user_id, kind="knowledge", key="knee-health")
    assert deleted is True
    assert crud.get_item(session, user_id, kind="knowledge", key="knee-health") is None


def test_log_list_search_events(session_and_user) -> None:
    session, user_id = session_and_user

    now = datetime.now(timezone.utc)
    logged = crud.log_event(
        session,
        user_id,
        kind="workout",
        content="5k tempo run in 22:30",
        occurred_at=now,
        attrs={"distance_km": 5.0, "duration_min": 22.5},
        tags="tempo,run",
    )

    assert logged["occurred_at"] is not None
    events = crud.list_events(session, user_id, kind="workout")
    assert len(events) == 1
    assert events[0]["attrs"]["distance_km"] == 5.0

    search = crud.search_entries(session, user_id, query="tempo", kind="workout")
    assert len(search) == 1
    assert search[0]["content"].startswith("5k tempo")


def test_get_overview_groups_data(session_and_user) -> None:
    session, user_id = session_and_user

    crud.upsert_item(
        session,
        user_id,
        kind="goal",
        key="5k-pr",
        content="Run 5k under 20 minutes",
        status="active",
        priority=1,
    )
    crud.upsert_item(
        session,
        user_id,
        kind="plan",
        key="base-build",
        content="Base mileage block",
        status="active",
    )
    crud.upsert_item(
        session,
        user_id,
        kind="plan-step",
        key="week-1",
        parent_key="base-build",
        content="Easy runs + strides",
    )
    crud.log_event(
        session,
        user_id,
        kind="workout",
        content="Long run 14km",
        occurred_at=datetime.now(timezone.utc),
    )

    overview = crud.get_overview(session, user_id)

    # Test new clean format
    assert overview["goals"]["active"][0]["key"] == "5k-pr"
    assert overview["plans"]["active"][0]["key"] == "base-build"
    assert overview["plans"]["steps"]["base-build"][0]["key"] == "week-1"
    assert overview["recent_workouts"]
    assert len(overview["recent_workouts"]) == 1


def test_bulk_upsert_items(session_and_user) -> None:
    session, user_id = session_and_user

    created = crud.bulk_upsert_items(
        session,
        user_id,
        [
            {
                "kind": "goal",
                "key": "bulk-goal",
                "content": "Improve squat technique",
                "status": "active",
                "priority": 1,
                "attrs": {"focus": "mobility"},
            },
            {
                "kind": "plan",
                "key": "bulk-plan",
                "content": "Weekly strength split",
                "tags": "strength",
            },
        ],
    )

    assert {item["key"] for item in created} == {"bulk-goal", "bulk-plan"}

    updated = crud.bulk_upsert_items(
        session,
        user_id,
        [
            {
                "kind": "goal",
                "key": "bulk-goal",
                "content": "Refine squat depth",
                "status": "paused",
            },
            {
                "kind": "plan",
                "key": "bulk-plan",
                "content": "Weekly strength split",
                "priority": 3,
            },
        ],
    )

    goal = next(item for item in updated if item["key"] == "bulk-goal")
    plan = next(item for item in updated if item["key"] == "bulk-plan")

    assert goal["status"] == "paused"
    assert plan["priority"] == 3

    goals = crud.list_items(session, user_id, kind="goal")
    assert goals and goals[0]["status"] == "paused"
