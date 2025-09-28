#!/usr/bin/env python3
"""Test script to measure latency when deployed to FastMCP Cloud."""

import time
import requests
import json
from typing import Dict, Any

def test_mcp_latency(server_url: str) -> Dict[str, Any]:
    """Test latency to deployed MCP server."""

    # Prepare MCP request
    headers = {
        "Content-Type": "application/json"
    }

    # Test save_memory operation
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "save_memory",
            "arguments": {
                "user_id": "latency_test",
                "content": "Testing deployment latency",
                "topic": "performance"
            }
        },
        "id": 1
    }

    print(f"🚀 Testing latency to {server_url}")
    print("-" * 50)

    # Perform multiple tests
    latencies = []
    for i in range(5):
        start = time.time()
        response = requests.post(server_url, json=payload, headers=headers)
        end = time.time()

        latency = (end - start) * 1000  # Convert to milliseconds
        latencies.append(latency)

        print(f"Test {i+1}: {latency:.2f}ms - Status: {response.status_code}")
        time.sleep(1)

    # Calculate statistics
    avg_latency = sum(latencies) / len(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)

    print("-" * 50)
    print(f"📊 Statistics:")
    print(f"  Average: {avg_latency:.2f}ms")
    print(f"  Min: {min_latency:.2f}ms")
    print(f"  Max: {max_latency:.2f}ms")

    # Check server region (if available in headers)
    if response.headers:
        print(f"\n📍 Response Headers (for region clues):")
        for key, value in response.headers.items():
            if any(k in key.lower() for k in ['region', 'location', 'server', 'cf-', 'x-amz']):
                print(f"  {key}: {value}")

    return {
        "average_ms": avg_latency,
        "min_ms": min_latency,
        "max_ms": max_latency,
        "samples": latencies
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python test_deployment_latency.py <fastmcp_server_url>")
        print("Example: python test_deployment_latency.py https://your-project.fastmcp.app/mcp")
        sys.exit(1)

    server_url = sys.argv[1]
    results = test_mcp_latency(server_url)

    print("\n💡 Recommendations:")
    if results["average_ms"] > 100:
        print("  ⚠️  High latency detected. Consider:")
        print("     - Checking if FastMCP Cloud and Supabase are in the same region")
        print("     - Using Supabase's direct connection instead of pooler")
        print("     - Implementing caching for frequently accessed data")
    else:
        print("  ✅ Latency is good! Your server and database are likely in the same region.")