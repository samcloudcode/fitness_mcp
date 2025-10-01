"""Integration tests exercising MCP tools via stdio transport."""

from __future__ import annotations

import asyncio
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Awaitable, Callable

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _call_json(session, tool: str, **arguments):
    result = await session.call_tool(tool, arguments=arguments)
    if not result.content:
        return None
    text = result.content[0].text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _run_with_session(user_id: str, scenario: Callable[[ClientSession], Awaitable[None]]) -> None:
    async def runner() -> None:
        env = dict(os.environ)
        env["FITNESS_USER_ID"] = user_id
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "python", "-m", "src.mcp_server"],
            env=env,
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                await scenario(session)

    asyncio.run(runner())


def test_mcp_workflow(cleanup_entries) -> None:
    user_id = f"mcp-test-{uuid.uuid4()}"
    cleanup_entries(user_id)

    async def scenario(session: ClientSession) -> None:
        created = await _call_json(
            session,
            "upsert_item",
            kind="knowledge",
            key="mcp-knee-health",
            content="Track knees over toes; progressive load",
        )
        assert created["user_id"] == user_id

        fetched = await _call_json(session, "get_item", kind="knowledge", key="mcp-knee-health")
        assert fetched["content"].startswith("Track knees")

        updated = await _call_json(
            session,
            "upsert_item",
            kind="knowledge",
            key="mcp-knee-health",
            content="Updated knee guidance",
            priority=2,
        )
        assert updated["priority"] == 2

        listed = await _call_json(session, "list_items", kind="knowledge")
        assert isinstance(listed, list) and len(listed) == 1

        search = await _call_json(session, "search_entries", query="knee", kind="knowledge")
        assert search and search[0]["key"] == "mcp-knee-health"

        await _call_json(
            session,
            "upsert_item",
            kind="plan",
            key="mcp-base-block",
            content="Base mileage plan",
            status="active",
        )
        await _call_json(
            session,
            "log_event",
            kind="workout",
            content="Easy run 6km",
            occurred_at=datetime.now(timezone.utc).isoformat(),
            attrs={"distance_km": 6.0},
        )

        events = await _call_json(session, "list_events", kind="workout")
        assert events and events[0]["attrs"].get("distance_km") == 6.0

        overview = await _call_json(session, "get_overview")
        assert overview["user_id"] == user_id
        assert overview["counts_by_kind"]["plan"] == 1
        assert overview["workouts"]["recent"]

        conventions = await _call_json(session, "describe_conventions")
        assert "goal" in conventions["kinds"]

        deleted = await _call_json(session, "delete_item", kind="knowledge", key="mcp-knee-health")
        assert deleted is True

        post_list = await _call_json(session, "list_items", kind="knowledge")
        assert not post_list

    _run_with_session(user_id, scenario)
    cleanup_entries(user_id)
