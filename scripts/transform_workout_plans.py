#!/usr/bin/env python3
"""
Transform workout-plan entries to session entries with type suffix.

Based on content analysis:
- 2025-10-20: Strength session
- 2025-10-21: VO2/Running session
- 2025-10-22: Mobility/recovery session
- 2025-10-23: Optional zone2/calisthenics (should be session, not workout-plan for optional)
- 2025-10-24: Sailing/active (multi-day event, could archive or keep as note)

Run with: source .env && uv run python scripts/transform_workout_plans.py
"""

import os
import sys

# Database connection - check env first
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Convert to psycopg driver
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)

engine = create_engine(DATABASE_URL)
USER_ID = os.getenv('FITNESS_USER_ID', '1')


def transform_workout_plan_to_session(session: Session, date: str, new_type: str):
    """Transform workout-plan to session with type suffix."""
    old_key = date
    new_key = f"{date}-{new_type}"

    # Get existing entry
    result = session.execute(
        text("SELECT id, content FROM public.entries WHERE user_id = :user_id AND kind = 'workout-plan' AND key = :key AND status = 'active'"),
        {"user_id": USER_ID, "key": old_key}
    )
    row = result.fetchone()

    if not row:
        print(f"⚠ Not found: workout-plan::{old_key}")
        return False

    old_id, content = row

    # Create new session entry
    session.execute(
        text("""
            INSERT INTO public.entries (user_id, kind, key, content, status, created_at, updated_at)
            VALUES (:user_id, :kind, :key, :content, 'active', NOW(), NOW())
        """),
        {"user_id": USER_ID, "kind": "session", "key": new_key, "content": content}
    )

    # Archive old entry
    session.execute(
        text("UPDATE public.entries SET status = 'archived' WHERE id = :id"),
        {"id": old_id}
    )

    print(f"✓ Transformed workout-plan::{old_key} → session::{new_key}")
    return True


def main():
    print("=" * 80)
    print("MIGRATION: Transform workout-plan to session")
    print("=" * 80)
    print()

    with Session(engine) as session:
        # Transform each workout-plan based on content analysis
        transformations = [
            ('2025-10-20', 'strength'),
            ('2025-10-21', 'run'),
            ('2025-10-22', 'mobility'),
            ('2025-10-23', 'optional'),  # Optional session
            ('2025-10-24', 'sailing'),   # Multi-day event
        ]

        transformed_count = 0
        for date, session_type in transformations:
            if transform_workout_plan_to_session(session, date, session_type):
                transformed_count += 1

        # Commit changes
        print()
        print("=" * 80)
        print("Committing changes...")
        session.commit()
        print(f"✓ Transformed {transformed_count}/5 workout-plan entries to session")
        print("=" * 80)
        print()
        print("Summary:")
        print("  - 2025-10-20 → 2025-10-20-strength")
        print("  - 2025-10-21 → 2025-10-21-run")
        print("  - 2025-10-22 → 2025-10-22-mobility")
        print("  - 2025-10-23 → 2025-10-23-optional")
        print("  - 2025-10-24 → 2025-10-24-sailing")
        print()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
