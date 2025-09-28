#!/usr/bin/env python3
"""Test client to exercise all MCP server tools and generate observability data."""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import time
from typing import Optional

async def test_memory_operations():
    """Run through all memory operations to generate logs and spans."""

    # Connect to the MCP server
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "src.mcp_server"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\n🚀 Starting MCP Memory Server Testing\n")
            print("=" * 60)

            # Test 1: Save multiple memories
            print("\n📝 TEST 1: Saving memories...")
            memories = []

            test_data = [
                ("user123", "My workout routine: 3x10 squats, 3x8 bench press", "workout"),
                ("user123", "Ran 5k in 25 minutes today, feeling great!", "cardio"),
                ("user456", "Started intermittent fasting 16:8 schedule", "diet"),
                ("user123", "Weight: 180lbs, Body fat: 15%", "measurements"),
                ("user456", "Completed 100 pushups challenge!", "achievement"),
            ]

            for user_id, content, topic in test_data:
                print(f"  Saving: {content[:50]}... (user: {user_id}, topic: {topic})")
                result = await session.call_tool(
                    "save_memory",
                    arguments={"user_id": user_id, "content": content, "topic": topic}
                )
                memories.append(result.content)
                print(f"  ✅ Saved with ID: {result.content[0].text}")
                await asyncio.sleep(0.5)  # Small delay to make logs easier to follow

            # Test 2: Get specific memories
            print("\n🔍 TEST 2: Retrieving specific memories...")
            if memories:
                # Parse the first memory ID
                first_memory = json.loads(memories[0][0].text)
                memory_id = first_memory['id']

                print(f"  Getting memory ID: {memory_id}")
                result = await session.call_tool(
                    "get_memory",
                    arguments={"memory_id": memory_id}
                )
                print(f"  ✅ Retrieved: {json.loads(result.content[0].text)['content'][:50]}...")

                # Test non-existent memory
                print(f"  Getting non-existent memory ID: 00000000-0000-0000-0000-000000000000")
                result = await session.call_tool(
                    "get_memory",
                    arguments={"memory_id": "00000000-0000-0000-0000-000000000000"}
                )
                if result.content:
                    print(f"  ✅ Result: {result.content[0].text}")
                else:
                    print(f"  ✅ Result: null (memory not found)")
                await asyncio.sleep(0.5)

            # Test 3: Search memories with different parameters
            print("\n🔎 TEST 3: Searching memories...")

            search_tests = [
                ("user123", "workout squats", None, "Full-text search for 'workout squats'"),
                ("user123", None, "cardio", "Topic filter for 'cardio'"),
                ("user456", "fasting", None, "Search user456 for 'fasting'"),
                ("user123", None, None, "All memories for user123"),
                ("user456", "challenge", "achievement", "Combined query and topic filter"),
            ]

            for user_id, query, topic, description in search_tests:
                print(f"\n  {description}")
                print(f"    User: {user_id}, Query: {query}, Topic: {topic}")

                args = {"user_id": user_id}
                if query:
                    args["query"] = query
                if topic:
                    args["topic"] = topic

                result = await session.call_tool("search_memories", arguments=args)
                results = json.loads(result.content[0].text)
                print(f"    ✅ Found {len(results)} results")

                for r in results[:2]:  # Show first 2 results
                    print(f"      - {r['content'][:60]}...")
                await asyncio.sleep(0.5)

            # Test 4: Error handling
            print("\n⚠️  TEST 4: Testing error scenarios...")

            try:
                print("  Testing invalid UUID format...")
                result = await session.call_tool(
                    "get_memory",
                    arguments={"memory_id": "not-a-valid-uuid"}
                )
                print(f"  Result: {result.content[0].text}")
            except Exception as e:
                print(f"  ✅ Caught expected error: {str(e)[:100]}...")

            print("\n" + "=" * 60)
            print("✅ All tests completed! Check your Logfire logs for spans and metrics.")
            print("\nYou should see:")
            print("  - Spans for each save_memory, get_memory, and search_memories call")
            print("  - Nested spans for database operations")
            print("  - Structured logs with user IDs, topics, and result counts")
            print("  - Performance metrics for each operation")

if __name__ == "__main__":
    print("🔥 MCP Memory Server Test Client")
    print("This will exercise all server tools to generate Logfire observability data.\n")
    asyncio.run(test_memory_operations())