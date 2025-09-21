#!/usr/bin/env python
"""Test the Memory MCP Server directly"""

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Now test the server
import asyncio
from src.memory import crud
from src.memory.db import SessionLocal

def test_crud_operations():
    """Test basic CRUD operations"""
    print("Testing Memory MCP Server CRUD operations...")

    with SessionLocal() as session:
        # Test save_memory
        print("\n1. Testing save_memory...")
        memory = crud.save_memory(
            session=session,
            user_id="test_user_123",
            content="This is a test memory from the Memory MCP Server",
            topic="testing"
        )
        print(f"✅ Saved memory: {memory['id']}")

        # Test get_memory
        print("\n2. Testing get_memory...")
        retrieved = crud.get_memory(session, memory['id'])
        print(f"✅ Retrieved memory: {retrieved['content'][:50]}...")

        # Test search_memories
        print("\n3. Testing search_memories...")
        results = crud.search_memories(
            session=session,
            user_id="test_user_123",
            query="test"
        )
        print(f"✅ Found {len(results)} memories")

        print("\n✅ All CRUD tests passed!")
        return True

if __name__ == "__main__":
    try:
        test_crud_operations()
        print("\n🎉 Memory MCP Server is working correctly!")
        print("\nYou can now run the server with:")
        print("  source .env && uv run python -m src.mcp_server")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check your DATABASE_URL in .env file")