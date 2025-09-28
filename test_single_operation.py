#!/usr/bin/env python3
"""Simple test to debug database connection performance."""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import time

async def test_single_save():
    """Test a single save operation to see connection pool behavior."""

    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "src.mcp_server"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\n🔍 Testing single save operation with timing...")

            start = time.time()
            result = await session.call_tool(
                "save_memory",
                arguments={
                    "user_id": "test_user",
                    "content": "Test memory for debugging",
                    "topic": "debug"
                }
            )
            end = time.time()

            print(f"✅ Save completed in {end - start:.2f} seconds")
            print(f"Result: {result.content[0].text[:100]}...")

            # Do another save to see if connection is reused
            print("\n🔍 Second save (should reuse connection)...")
            start = time.time()
            result = await session.call_tool(
                "save_memory",
                arguments={
                    "user_id": "test_user",
                    "content": "Second test memory",
                    "topic": "debug"
                }
            )
            end = time.time()

            print(f"✅ Second save completed in {end - start:.2f} seconds")

            print("\n⚠️  Check the server console for pool debugging output!")

if __name__ == "__main__":
    asyncio.run(test_single_save())