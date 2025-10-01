#!/usr/bin/env python3
"""Quick smoke test for the Fitness Memory MCP server.

Creates a few items and events, then fetches get_overview().
This uses the MCP Python client to spawn the server over stdio.
"""

import asyncio
import json
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    # Point to the server module; the parent shell should provide FITNESS_USER_ID in env
    server = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "src.mcp_server"],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\n🚀 Smoke testing Fitness Memory MCP tools\n")

            # Upsert some durable items
            print("🧠 Upsert knowledge item...")
            res = await session.call_tool(
                "upsert_item",
                arguments={
                    "kind": "knowledge",
                    "key": "knee-health-best-practices",
                    "content": "Keep knees tracking over toes; progressive load; quad/ham balance; gradual plyometrics.",
                },
            )
            print("  ✅", res.content[0].text)

            print("📃 Upsert plan + step...")
            await session.call_tool(
                "upsert_item",
                arguments={
                    "kind": "plan",
                    "key": "running-progression",
                    "content": "12-week base → build → peak",
                    "status": "active",
                },
            )
            await session.call_tool(
                "upsert_item",
                arguments={
                    "kind": "plan-step",
                    "key": "wk1-base",
                    "parent_key": "running-progression",
                    "content": "3x easy 30m; strides x6",
                },
            )
            print("  ✅ plan + step saved")

            print("⚙️  Upsert preference + current metric...")
            await session.call_tool(
                "upsert_item",
                arguments={
                    "kind": "preference",
                    "key": "supersets",
                    "content": "Prefer supersets for accessories",
                },
            )
            await session.call_tool(
                "upsert_item",
                arguments={
                    "kind": "current",
                    "key": "bench-working-weight",
                    "content": "100kg x5x3",
                    "attrs": {"numeric_value": 100, "unit": "kg"},
                },
            )
            print("  ✅ preference + current saved")

            print("🏃 Log workout event...")
            await session.call_tool(
                "log_event",
                arguments={
                    "kind": "workout",
                    "content": "5k in 25:00, easy pace",
                    "occurred_at": "2025-10-01T07:30:00",
                    "attrs": {"distance_km": 5.0, "duration_min": 25},
                },
            )
            print("  ✅ workout logged")

            print("🧩 Fetch overview...")
            overview = await session.call_tool("get_overview", arguments={})
            parsed = json.loads(overview.content[0].text)
            print("  🧾 counts_by_kind:", parsed.get("counts_by_kind"))
            print("  🎯 goals active:", len(parsed.get("goals", {}).get("active", [])))
            print("  📦 plans:", len(parsed.get("plans", {}).get("all", [])))
            print("  🏷️ preferences:", len(parsed.get("preferences", [])))
            print("  🏃 recent workouts:", len(parsed.get("workouts", {}).get("recent", [])))


if __name__ == "__main__":
    asyncio.run(main())

