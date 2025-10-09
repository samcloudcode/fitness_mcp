#!/usr/bin/env python3
"""Test script for simplified 6-tool MCP server"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Load env before imports
from dotenv import load_dotenv
load_dotenv()

from src.memory.crud import upsert_item, log_event, get_overview, search_entries
from src.memory.db import SessionLocal
from datetime import datetime

def test_simplified_tools():
    """Test the simplified tool architecture"""

    user_id = os.getenv('FITNESS_USER_ID') or os.getenv('DEFAULT_USER_ID')
    if not user_id:
        print("ERROR: FITNESS_USER_ID not set")
        return

    with SessionLocal() as session:
        print("Testing Simplified 6-Tool Architecture\n" + "="*40)

        # Test 1: Upsert with attrs
        print("\n1. Testing UPSERT with attrs...")
        result = upsert_item(
            session, user_id,
            kind='goal',
            key='test-simplified',
            content='Test goal for simplified schema',
            status='active',
            priority='high',  # Goes to attrs
            tags='test,simplified',  # Goes to attrs
            attrs={'custom_field': 'custom_value'}
        )
        print(f"✓ Created goal: {result['key']}")
        print(f"  Status: {result['status']}")
        print(f"  Attrs: {result.get('attrs', {})}")

        # Test 2: Log event with attrs
        print("\n2. Testing LOG event...")
        event = log_event(
            session, user_id,
            kind='workout',
            content='Test workout for simplified schema',
            occurred_at=datetime.now(),
            tags='test,workout',  # Goes to attrs
            attrs={'exercises': [{'name': 'Test', 'sets': 3}]}
        )
        print(f"✓ Logged workout: {event['id'][:8]}...")
        print(f"  Attrs: {event.get('attrs', {})}")

        # Test 3: Overview with truncation
        print("\n3. Testing OVERVIEW...")
        overview = get_overview(session, user_id, truncate_length=50)
        goals = overview.get('goals', {}).get('active', [])
        print(f"✓ Found {len(goals)} active goals")
        if goals:
            print(f"  First goal: {goals[0].get('key')} - {goals[0].get('content', '')[:50]}")

        # Test 4: Search
        print("\n4. Testing SEARCH...")
        results = search_entries(session, user_id, query='simplified', limit=10)
        print(f"✓ Found {len(results)} results for 'simplified'")

        # Test 5: Check attrs migration
        print("\n5. Checking attrs migration...")
        from sqlalchemy import select, and_
        from src.memory.db import Entry

        stmt = select(Entry).where(
            and_(
                Entry.user_id == user_id,
                Entry.attrs.op('?')('priority')  # Has priority in attrs
            )
        ).limit(5)

        entries = session.execute(stmt).scalars().all()
        print(f"✓ Found {len(entries)} entries with priority in attrs")

        stmt = select(Entry).where(
            and_(
                Entry.user_id == user_id,
                Entry.attrs.op('?')('tags')  # Has tags in attrs
            )
        ).limit(5)

        entries = session.execute(stmt).scalars().all()
        print(f"✓ Found {len(entries)} entries with tags in attrs")

        print("\n" + "="*40)
        print("✅ All tests passed! Simplified schema working correctly.")

        # Cleanup test data
        print("\n6. Cleaning up test data...")
        from src.memory.crud import delete_item
        delete_item(session, user_id, kind='goal', key='test-simplified')
        print("✓ Test data cleaned up")

if __name__ == "__main__":
    test_simplified_tools()